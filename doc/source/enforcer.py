import importlib
import itertools
import os

from bs4 import BeautifulSoup
from sphinx import errors

# NOTE: We do this because I can't find any way to pass "-v"
# into sphinx-build through pbr...
DEBUG = True if os.getenv("ENFORCER_DEBUG") else False

WRITTEN_METHODS = set()

# NOTE: This is temporary! These methods currently exist on the base
# Proxy class as public methods, but they're deprecated in favor of
# subclasses actually exposing them if necessary. However, as they're
# public and purposely undocumented, they cause spurious warnings.
# Ignore these methods until they're actually removed from the API,
# and then we can take this special case out.
IGNORED_METHODS = ("wait_for_delete", "wait_for_status")

class EnforcementError(errors.SphinxError):
    """A mismatch between what exists and what's documented"""
    category = "Enforcer"


def get_proxy_methods():
    """Return a set of public names on all proxies"""
    names = ["openstack.bare_metal.v1._proxy",
             "openstack.block_store.v2._proxy",
             "openstack.cluster.v1._proxy",
             "openstack.compute.v2._proxy",
             "openstack.database.v1._proxy",
             "openstack.identity.v2._proxy",
             "openstack.identity.v3._proxy",
             "openstack.image.v1._proxy",
             "openstack.image.v2._proxy",
             "openstack.key_manager.v1._proxy",
             "openstack.message.v1._proxy",
             "openstack.message.v2._proxy",
             "openstack.metric.v1._proxy",
             "openstack.network.v2._proxy",
             "openstack.object_store.v1._proxy",
             "openstack.orchestration.v1._proxy",
             "openstack.telemetry.v2._proxy",
             "openstack.telemetry.alarm.v2._proxy",
             "openstack.workflow.v2._proxy"]

    modules = (importlib.import_module(name) for name in names)

    methods = set()
    for module in modules:
        # We're not going to use the Proxy for anything other than a `dir`
        # so just pass a dummy value so we can create the instance.
        instance = module.Proxy("")
        # We only document public names
        names = [name for name in dir(instance) if not name.startswith("_")]

        # Remove the wait_for_* names temporarily.
        for name in IGNORED_METHODS:
            names.remove(name)

        good_names = [module.__name__ + ".Proxy." + name for name in names]
        methods.update(good_names)

    return methods


def page_context(app, pagename, templatename, context, doctree):
    """Handle html-page-context-event

    This event is emitted once the builder has the contents to create
    an HTML page, but before the template is rendered. This is the point
    where we'll know what documentation is going to be written, so
    gather all of the method names that are about to be included
    so we can check which ones were or were not processed earlier
    by autodoc.
    """
    if "users/proxies" in pagename:
        soup = BeautifulSoup(context["body"], "html.parser")
        dts = soup.find_all("dt")
        ids = [dt.get("id") for dt in dts]

        written = 0
        for id in ids:
            if id is not None and "_proxy.Proxy" in id:
                WRITTEN_METHODS.add(id)
                written += 1

        if DEBUG:
            app.info("ENFORCER: Wrote %d proxy methods for %s" % (
                     written, pagename))


def build_finished(app, exception):
    """Handle build-finished event

    This event is emitted once the builder has written all of the output.
    At this point we just compare what we know was written to what we know
    exists within the modules and share the results.

    When enforcer_warnings_as_errors=True in conf.py, this method
    will raise EnforcementError on any failures in order to signal failure.
    """
    all_methods = get_proxy_methods()

    app.info("ENFORCER: %d proxy methods exist" % len(all_methods))
    app.info("ENFORCER: %d proxy methods written" % len(WRITTEN_METHODS))
    missing = all_methods - WRITTEN_METHODS

    def is_ignored(name):
        for ignored_name in IGNORED_METHODS:
            if ignored_name in name:
                return True
        return False
    # this function is added for python2.x and python3.x compatible
    # replace the itertools.filterfalse in python3 and itertools.ifilterfalse in python2

    def customfilterfalse(predicate, iterable):
        # ifilterfalse(lambda x: x%2, range(10)) --> 0 2 4 6 8
        if predicate is None:
            predicate = bool
        for x in iterable:
            if not predicate(x):
                yield x
    # TEMPORARY: Ignore the wait_for names when determining what is missing.
    app.info("ENFORCER: Ignoring wait_for_* names...")
    #missing = set(itertools.filterfalse(is_ignored, missing))
    missing = set(customfilterfalse(is_ignored, missing))

    missing_count = len(missing)
    app.info("ENFORCER: Found %d missing proxy methods "
             "in the output" % missing_count)

    for name in sorted(missing):
        app.warn("ENFORCER: %s was not included in the output" % name)

    if app.config.enforcer_warnings_as_errors and missing_count > 0:
        raise EnforcementError(
            "There are %d undocumented proxy methods" % missing_count)


def setup(app):
    app.add_config_value("enforcer_warnings_as_errors", False, "env")

    app.connect("html-page-context", page_context)
    app.connect("build-finished", build_finished)
