# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
#      Huawei has modified this source file.
#     
#         Copyright 2018 Huawei Technologies Co., Ltd.
#         
#         Licensed under the Apache License, Version 2.0 (the "License"); you may not
#         use this file except in compliance with the License. You may obtain a copy of
#         the License at
#         
#             http://www.apache.org/licenses/LICENSE-2.0
#         
#         Unless required by applicable law or agreed to in writing, software
#         distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#         WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#         License for the specific language governing permissions and limitations under
#         the License.

"""
The :class:`~openstack.resource.Resource` class is a base
class that represent a remote resource. The attributes that
comprise a request or response for this resource are specified
as class members on the Resource subclass where their values
are of a component type, including :class:`~openstack.resource2.Body`,
:class:`~openstack.resource2.Header`, and :class:`~openstack.resource2.URI`.

For update management, :class:`~openstack.resource2.Resource` employs
a series of :class:`~openstack.resource2._ComponentManager` instances
to look after the attributes of that particular component type. This is
particularly useful for Body and Header types, so that only the values
necessary are sent in requests to the server.

When making requests, each of the managers are looked at to gather the
necessary URI, body, and header data to build a request to be sent
via keystoneauth's sessions. Responses from keystoneauth are then
converted into this Resource class' appropriate components and types
and then returned to the caller.
"""

import collections
import itertools
import time

from openstack import exceptions
from openstack import format
from openstack import utils


class _BaseComponent(object):
    # The name this component is being tracked as in the Resource
    key = None

    def __init__(self, name, type=None, default=None, alternate_id=False):
        """A typed descriptor for a component that makes up a Resource

        :param name: The name this component exists as on the server
        :param type: The type this component is expected to be by the server.
                     By default this is None, meaning any value you specify
                     will work. If you specify type=dict and then set a
                     component to a string, __set__ will fail, for example.
        :param default: Typically None, but any other default can be set.
        :param alternate_id: When `True`, this property is known
                             internally as a value that can be sent
                             with requests that require an ID but
                             when `id` is not a name the Resource has.
                             This is a relatively uncommon case, and this
                             setting should only be used once per Resource.
        """
        self.name = name
        self.type = type
        self.default = default
        self.alternate_id = alternate_id

    def __get__(self, instance, owner):
        if instance is None:
            return None

        attributes = getattr(instance, self.key)

        try:
            value = attributes[self.name]
        except KeyError:
            value = self.default

        # self.type() should not be called on None objects.
        if value is None:
            return None

        if self.type and not isinstance(value, self.type):
            if issubclass(self.type, format.Formatter):
                value = self.type.deserialize(value)
            elif issubclass(self.type, Resource):
                value = self.type.new(**value)
            else:
                value = self.type(value)

        return value

    def __set__(self, instance, value):
        if self.type:
            if not isinstance(value, self.type) and value != self.default:
                if issubclass(self.type, format.Formatter):
                    value = self.type.serialize(value)
                elif issubclass(self.type, Resource):
                    value = self.type.new(**value)
                else:
                    value = str(self.type(value))  # validate to fail fast

        attributes = getattr(instance, self.key)
        attributes[self.name] = value

    def __delete__(self, instance):
        try:
            attributes = getattr(instance, self.key)
            del attributes[self.name]
        except KeyError:
            print("Key Error")

class Body(_BaseComponent):
    """Body attributes"""

    key = "_body"


class Header(_BaseComponent):
    """Header attributes"""

    key = "_header"


class URI(_BaseComponent):
    """URI attributes"""

    key = "_uri"


class _ComponentManager(collections.MutableMapping):
    """Storage of a component type"""

    def __init__(self, attributes=None, synchronized=False):
        self.attributes = dict() if attributes is None else attributes.copy()
        self._dirty = set() if synchronized else set(self.attributes.keys())

    def __getitem__(self, key):
        return self.attributes[key]

    def __setitem__(self, key, value):
        try:
            orig = self.attributes[key]
        except KeyError:
            changed = True
        else:
            changed = orig != value

        if changed:
            self.attributes[key] = value
            self._dirty.add(key)

    def __delitem__(self, key):
        del self.attributes[key]
        self._dirty.add(key)

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)

    @property
    def dirty(self):
        """Return a dict of modified attributes"""
        plain = {}
        for key in self._dirty:
            value = self.attributes.get(key, None)
            if isinstance(value, Resource):
                value = value._body.dirty
            # get type
            plain[key] = value
        return plain

    def clean(self):
        """Signal that the resource no longer has modified attributes"""
        self._dirty = set()


class _Request(object):
    """Prepared components that go into a KSA request"""

    def __init__(self, uri, body, headers):
        self.uri = uri
        self.body = body
        self.headers = headers


class QueryParameters(object):
    def __init__(self, *names, **mappings):
        """Create a dict of accepted query parameters

        :param names: List of strings containing client-side query parameter
                      names. Each name in the list maps directly to the name
                      expected by the server.

        :param mappings: Key-value pairs where the key is the client-side
                         name we'll accept here and the value is the name
                         the server expects, e.g, changes_since=changes-since

        By default, both limit and marker are included in the initial mapping
        as they're the most common query parameters used for listing resources.
        """
        self._mapping = {"limit": "limit", "marker": "marker"}
        self._mapping.update(dict({name: name for name in names}, **mappings))

    def _transpose(self, query):
        """Transpose the keys in query based on the mapping

        :param dict query: Collection of key-value pairs where each key is the
                           client-side parameter name to be transposed to its
                           server side name.
        """
        result = {}
        for key, value in self._mapping.items():
            if key in query:
                result[value] = query[key]
            if value in query:
                result[value] = query[value]
        return result


class Resource(object):
    #: Singular form of key for resource.
    resource_key = None
    #: Plural form of key for resource.
    resources_key = None
    #: dotted json path to get next marker
    next_marker_path = None
    #: marker key in query, default is `marker`
    query_marker_key = "marker"
    query_limit_key = "limit"

    #: The ID of this resource.
    id = Body("id")
    #: The name of this resource.
    name = Body("name")
    #: The location of this resource.
    location = Header("Location")

    #: Mapping of accepted query parameter names.
    _query_mapping = QueryParameters(marker=query_marker_key)

    #: The base part of the URI for this resource.
    base_path = ""

    #: The service associated with this resource to find the service URL.
    service = None

    #: Allow create operation for this resource.
    allow_create = False
    #: Allow get operation for this resource.
    allow_get = False
    #: Allow update operation for this resource.
    allow_update = False
    #: Allow delete operation for this resource.
    allow_delete = False
    #: Allow list operation for this resource.
    allow_list = False
    #: Allow head operation for this resource.
    allow_head = False
    #: Use PATCH for update operations on this resource.
    patch_update = False
    #: Use PUT for create operations on this resource.
    put_create = False

    @staticmethod
    def get_service_filter(resource, session):
        """
        :param sess: ~openstack.session.Session.
        :param resource: ~openstack.resource2.Resource
        :return: ~openstack.service_filter.ServiceFilter
        """
        service = session.profile.get_filter(resource.service.service_type)
        if service:
            return service
        else:
            return resource.service

    def __init__(self, _synchronized=False, **attrs):
        """The base resource

        :param bool _synchronized: This is not intended to be used directly.
                    See :meth:`~openstack.resource2.Resource.new` and
                    :meth:`~openstack.resource2.Resource.existing`.
        """

        # NOTE: _collect_attrs modifies **attrs in place, removing
        # items as they match up with any of the body, header,
        # or uri mappings.
        body, header, uri = self._collect_attrs(attrs)
        # TODO(briancurtin): at this point if attrs has anything left
        # they're not being set anywhere. Log this? Raise exception?
        # How strict should we be here? Should strict be an option?

        self._body = _ComponentManager(attributes=body,
                                       synchronized=_synchronized)
        self._header = _ComponentManager(attributes=header,
                                         synchronized=_synchronized)
        self._uri = _ComponentManager(attributes=uri,
                                      synchronized=_synchronized)

    def __repr__(self):
        pairs = ["%s=%s" % (k, v) for k, v in dict(itertools.chain(
            self._body.attributes.items(),
            self._header.attributes.items(),
            self._uri.attributes.items())).items()]
        args = ", ".join(pairs)

        return "%s.%s(%s)" % (
            self.__module__, self.__class__.__name__, args)

    def __eq__(self, comparand):
        """Return True if another resource has the same contents"""
        return all([self._body.attributes == comparand._body.attributes,
                    self._header.attributes == comparand._header.attributes,
                    self._uri.attributes == comparand._uri.attributes])

    def __getattribute__(self, name):
        """Return an attribute on this instance

        This is mostly a pass-through except for a specialization on
        the 'id' name, as this can exist under a different name via the
        `alternate_id` argument to resource.Body.
        """
        if name == "id":
            if name in self._body:
                return self._body[name]

            real_id_name = self._body_mapping()[name]
            if real_id_name in self._body:
                return self._body[real_id_name]
            else:
                try:
                    return self._body[self._alternate_id()]
                except KeyError:
                    return None
        else:
            return object.__getattribute__(self, name)

    def _update(self, **attrs):
        """Given attributes, update them on this instance

        This is intended to be used from within the proxy
        layer when updating instances that may have already
        been created.
        """
        body, header, uri = self._collect_attrs(attrs)

        self._body.update(body)
        self._header.update(header)
        self._uri.update(uri)

    def _collect_attrs(self, attrs):
        """Given attributes, return a dict per type of attribute

        This method splits up **attrs into separate dictionaries
        that correspond to the relevant body, header, and uri
        attributes that exist on this class.
        """
        body = self._consume_attrs(Body, attrs)
        header = self._consume_attrs(Header, attrs)
        uri = self._consume_attrs(URI, attrs)

        return body, header, uri

    @classmethod
    def _consume_attrs(cls, component_type, attrs):
        """Given a mapping and attributes, return relevant matches

        This method finds keys in attrs that exist in the mapping, then
        both transposes them to their server-side equivalent key name
        to be returned, and finally pops them out of attrs. This allows
        us to only calculate their place and existence in a particular
        type of Resource component one time, rather than looking at the
        same source dict several times.
        """

        fields = {}
        for klass in cls.__mro__:
            for key, component in klass.__dict__.items():
                if isinstance(component, component_type):
                    # Make sure base classes don't end up overwriting
                    # mappings we've found previously in subclasses.
                    if key not in fields:
                        fields[key] = component
                        fields[component.name] = component

        relevant_attrs = {}
        attr_keys = list(attrs.keys())
        for key in attr_keys:
            if key in fields:
                field = fields[key]
                value = attrs.pop(key)
                server_side_key = field.name
                # Convert client-side key names into server-side.
                if value and field.type and not isinstance(value, field.type):
                    if issubclass(field.type, format.Formatter):
                        value = field.type.serialize(value)
                    elif issubclass(field.type, Resource):
                        value = field.type.new(**value)
                    else:
                        value = field.type(value)
                relevant_attrs[server_side_key] = value

        return relevant_attrs

    # def _consume_attrs(self, mapping, attrs):
    #     """Given a mapping and attributes, return relevant matches
    #
    #     This method finds keys in attrs that exist in the mapping, then
    #     both transposes them to their server-side equivalent key name
    #     to be returned, and finally pops them out of attrs. This allows
    #     us to only calculate their place and existence in a particular
    #     type of Resource component one time, rather than looking at the
    #     same source dict several times.
    #     """
    #     relevant_attrs = {}
    #     consumed_keys = []
    #     for key in attrs:
    #         if key in mapping:
    #             # Convert client-side key names into server-side.
    #             relevant_attrs[mapping[key]] = attrs[key]
    #             consumed_keys.append(key)
    #         elif key in mapping.values():
    #             # Server-side names can be stored directly.
    #             relevant_attrs[key] = attrs[key]
    #             consumed_keys.append(key)
    #
    #     for key in consumed_keys:
    #         attrs.pop(key)
    #
    #     return relevant_attrs

    @classmethod
    def _get_mapping(cls, component):
        """Return a dict of attributes of a given component on the class

        """
        mapping = {}
        # Since we're looking at class definitions we need to include
        # subclasses, so check the whole MRO.
        for klass in cls.__mro__:
            for key, value in klass.__dict__.items():
                if isinstance(value, component):
                    # Make sure base classes don't end up overwriting
                    # mappings we've found previously in subclasses.
                    if key not in mapping:
                        mapping[key] = value.name
        return mapping

    @classmethod
    def _body_mapping(cls):
        """Return all Body members of this class"""
        return cls._get_mapping(Body)

    @classmethod
    def _header_mapping(cls):
        """Return all Header members of this class"""
        return cls._get_mapping(Header)

    @classmethod
    def _uri_mapping(cls):
        """Return all URI members of this class"""
        return cls._get_mapping(URI)

    @classmethod
    def _alternate_id(cls):
        """Return the name of any value known as an alternate_id

        NOTE: This will only ever return the first such alternate_id.
        Only one alternate_id should be specified.

        Returns an empty string if no name exists, as this method is
        consumed by _get_id and passed to getattr.
        """
        for value in cls.__dict__.values():
            if isinstance(value, Body):
                if value.alternate_id:
                    return value.name
        return ""

    @staticmethod
    def _get_id(value):
        """If a value is a Resource, return the canonical ID

        This will return either the value specified by `id` or
        `alternate_id` in that order if `value` is a Resource.
        If `value` is anything other than a Resource, likely to
        be a string already representing an ID, it is returned.
        """
        if isinstance(value, Resource):
            return value.id
        else:
            return value

    @classmethod
    def new(cls, **kwargs):
        """Create a new instance of this resource.

        When creating the instance set the ``_synchronized`` parameter
        of :class:`Resource` to ``False`` to indicate that the resource does
        not yet exist on the server side. This marks all attributes passed
        in ``**kwargs`` as "dirty" on the resource, and thusly tracked
        as necessary in subsequent calls such as :meth:`update`.

        :param dict kwargs: Each of the named arguments will be set as
                            attributes on the resulting Resource object.
        """
        return cls(_synchronized=False, **kwargs)

    @classmethod
    def existing(cls, **kwargs):
        """Create an instance of an existing remote resource.

        When creating the instance set the ``_synchronized`` parameter
        of :class:`Resource` to ``True`` to indicate that it represents the
        state of an existing server-side resource. As such, all attributes
        passed in ``**kwargs`` are considered "clean", such that an immediate
        :meth:`update` call would not generate a body of attributes to be
        modified on the server.

        :param dict kwargs: Each of the named arguments will be set as
                            attributes on the resulting Resource object.
        """
        return cls(_synchronized=True, **kwargs)

    def to_dict(self, body=True, headers=True, ignore_none=False):
        """Return a dictionary of this resource's contents

        :param bool body: Include the :class:`~openstack.resource2.Body`
                          attributes in the returned dictionary.
        :param bool headers: Include the :class:`~openstack.resource2.Header`
                             attributes in the returned dictionary.
        :param bool ignore_none: When True, exclude key/value pairs where
                                 the value is None. This will exclude
                                 attributes that the server hasn't returned.

        :return: A dictionary of key/value pairs where keys are named
                 as they exist as attributes of this class.
        """
        mapping = {}

        components = []
        if body:
            components.append(Body)
        if headers:
            components.append(Header)
        if not components:
            raise ValueError(
                "At least one of `body` or `headers` must be True")

        # isinstance stricly requires this to be a tuple
        components = tuple(components)

        # NOTE: This is similar to the implementation in _get_mapping
        # but is slightly different in that we're looking at an instance
        # and we're mapping names on this class to their actual stored
        # values.
        # Since we're looking at class definitions we need to include
        # subclasses, so check the whole MRO.
        for klass in self.__class__.__mro__:
            for key, value in klass.__dict__.items():
                if isinstance(value, components):
                    # Make sure base classes don't end up overwriting
                    # mappings we've found previously in subclasses.
                    if key not in mapping:
                        value = getattr(self, key, None)
                        if ignore_none and value is None:
                            continue
                        mapping[key] = value

        return mapping

    def _prepare_request(self, requires_id=True, prepend_key=False):
        """Prepare a request to be sent to the server

        Create operations don't require an ID, but all others do,
        so only try to append an ID when it's needed with
        requires_id. Create and update operations sometimes require
        their bodies to be contained within an dict -- if the
        instance contains a resource_key and prepend_key=True,
        the body will be wrapped in a dict with that key.

        Return a _Request object that contains the constructed URI
        as well a body and headers that are ready to send.
        Only dirty body and header contents will be returned.
        """
        body = self._body.dirty
        if prepend_key and self.resource_key is not None:
            body = {self.resource_key: body}

        headers = self._header.dirty

        uri = self.base_path % self._uri.attributes
        if requires_id:
            if self.id is None:
                raise exceptions.InvalidRequest(
                    "Request requires an ID but none was found")

            uri = utils.urljoin(uri, self.id)

        return _Request(uri, body, headers)

    def _filter_component(self, component, mapping):
        """Filter the keys in component based on a mapping

        This method converts a dict of server-side data to contain
        only the appropriate keys for attributes on this instance.
        """
        return {k: v for k, v in component.items() if k in mapping.values()}

    def _translate_response(self, response, has_body=True):
        """Given a KSA response, inflate this instance with its data

        DELETE operations don't return a body, so only try to work
        with a body when has_body is True.

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body:
            body = response.json()
            if self.resource_key and self.resource_key in body:
                body = body[self.resource_key]

            body = self._filter_component(body, self._body_mapping())
            self._body.attributes.update(body)
            self._body.clean()

        headers = self._filter_component(response.headers,
                                         self._header_mapping())
        self._header.attributes.update(headers)
        self._header.clean()

    def create(self, session, prepend_key=True):
        """Create a remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~openstack.session.Session`
        :param prepend_key: A boolean indicating whether the resource_key
                            should be prepended in a resource creation
                            request. Default to True.

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_create` is not set to ``True``.
        """
        if not self.allow_create:
            raise exceptions.MethodNotSupported(self, "create")

        endpoint_override = self.service.get_endpoint_override()
        service = self.get_service_filter(self, session)
        if self.put_create:
            request = self._prepare_request(requires_id=True,
                                            prepend_key=prepend_key)
            response = session.put(request.uri, endpoint_filter=self.service,
                                   endpoint_override=endpoint_override,
                                   json=request.body, headers=request.headers,
                                   microversion = service.microversion)
        else:
            request = self._prepare_request(requires_id=False,
                                            prepend_key=prepend_key)
            response = session.post(request.uri, endpoint_filter=self.service,
                                    endpoint_override=endpoint_override,
                                    json=request.body, headers=request.headers,
                                    microversion=service.microversion)

        self._translate_response(response)
        return self

    def get(self, session, requires_id=True):
        """Get a remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~openstack.session.Session`
        :param boolean requires_id: A boolean indicating whether resource ID
                                    should be part of the requested URI.
        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_get` is not set to ``True``.
        """
        if not self.allow_get:
            raise exceptions.MethodNotSupported(self, "get")

        request = self._prepare_request(requires_id=requires_id)
        endpoint_override = self.service.get_endpoint_override()
        service = self.get_service_filter(self, session)
        response = session.get(request.uri, endpoint_filter = self.service,
                               microversion = service.microversion,
                               endpoint_override=endpoint_override)
        self._translate_response(response)
        return self

    def head(self, session):
        """Get headers from a remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~openstack.session.Session`

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_head` is not set to ``True``.
        """
        if not self.allow_head:
            raise exceptions.MethodNotSupported(self, "head")

        request = self._prepare_request()
        endpoint_override = self.service.get_endpoint_override()
        service = self.get_service_filter(self, session)
        response = session.head(request.uri, endpoint_filter=self.service,
                                microversion=service.microversion,
                                endpoint_override=endpoint_override,
                                headers={"Accept": ""})

        self._translate_response(response)
        return self

    def update(self, session, prepend_key=True, has_body=True):
        """Update the remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~openstack.session.Session`
        :param prepend_key: A boolean indicating whether the resource_key
                            should be prepended in a resource update request.
                            Default to True.

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_update` is not set to ``True``.
        """
        # The id cannot be dirty for an update
        self._body._dirty.discard("id")
        id_mapping_name = self._body_mapping()["id"]
        self._body._dirty.discard(id_mapping_name)

        # Only try to update if we actually have anything to update.
        if not any([self._body.dirty, self._header.dirty]):
            return self

        if not self.allow_update:
            raise exceptions.MethodNotSupported(self, "update")

        request = self._prepare_request(prepend_key=prepend_key)
        service = self.get_service_filter(self, session)
        endpoint_override = self.service.get_endpoint_override()
        if self.patch_update:
            response = session.patch(request.uri, endpoint_filter=self.service,
                                     microversion = service.microversion,
                                     endpoint_override=endpoint_override,
                                     json=request.body,
                                     headers=request.headers)
        else:
            response = session.put(request.uri, endpoint_filter=self.service,
                                   microversion=service.microversion,
                                   endpoint_override=endpoint_override,
                                   json=request.body, headers=request.headers)

        self._translate_response(response, has_body=has_body)
        return self

    def delete(self, session, params=None, has_body=False):
        """Delete the remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~openstack.session.Session`
        :param params: http params to be sent
        :param bool has_body: should mapping response body to resource

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_update` is not set to ``True``.
        """
        if not self.allow_delete:
            raise exceptions.MethodNotSupported(self, "delete")

        request = self._prepare_request()
        service = self.get_service_filter(self, session)
        endpoint_override = self.service.get_endpoint_override()
        response = session.delete(request.uri, endpoint_filter=self.service,
                                  microversion = service.microversion,
                                  endpoint_override=endpoint_override,
                                  headers={"Accept": ""},
                                  params=params)

        self._translate_response(response, has_body=has_body)
        return self

    @classmethod
    def get_next_marker(cls, response_json, yielded, query_params):
        if cls.next_marker_path:
            return cls.find_value_by_accessor(response_json,
                                              cls.next_marker_path)
        return None

    @staticmethod
    def find_value_by_accessor(input_dict, accessor):
        """Gets value from a dictionary using a dotted accessor"""
        current_data = input_dict
        for chunk in accessor.split('.'):
            if isinstance(current_data, dict):
                current_data = current_data.get(chunk, {})
            else:
                return None
        return current_data

    @classmethod
    def get_list_uri(cls, params):
        return cls.base_path % params

    @classmethod
    def list(cls, session, paginated=False, **params):
        """This method is a generator which yields resource objects.

        This resource object list generator handles pagination and takes query
        params for response filtering.

        :param session: The session to use for making this request.
        :type session: :class:`~openstack.session.Session`
        :param bool paginated: ``True`` if a GET to this resource returns
                               a paginated series of responses, or ``False``
                               if a GET returns only one page of data.
                               **When paginated is False only one
                               page of data will be returned regardless
                               of the API's support of pagination.**
        :param dict params: These keyword arguments are passed through the
            :meth:`~openstack.resource2.QueryParamter._transpose` method
            to find if any of them match expected query parameters to be
            sent in the *params* argument to
            :meth:`~openstack.session.Session.get`. They are additionally
            checked against the
            :data:`~openstack.resource2.Resource.base_path` format string
            to see if any path fragments need to be filled in by the contents
            of this argument.

        :return: A generator of :class:`Resource` objects.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_list` is not set to ``True``.
        """
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        more_data = True
        query_params = cls._query_mapping._transpose(params)
        uri = cls.get_list_uri(params)
        service = cls.get_service_filter(cls, session)
        while more_data:
            endpoint_override = cls.service.get_endpoint_override()
            resp = session.get(uri, endpoint_filter=cls.service,
                               microversion=service.microversion,
                               endpoint_override=endpoint_override,
                               headers={"Accept": "application/json"},
                               params=query_params)
            response_json = resp.json()
            if cls.resources_key:
                resources = cls.find_value_by_accessor(response_json,
                                                       cls.resources_key)
            else:
                resources = response_json

            if not resources:
                more_data = False

            # Keep track of how many items we've yielded. If we yielded
            # less than our limit, we don't need to do an extra request
            # to get back an empty data set, which acts as a sentinel.
            yielded = 0
            new_marker = None
            for data in resources:
                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                data.pop("self", None)

                value = cls.existing(**data)
                new_marker = value.id
                yielded += 1
                yield value

            query_params = dict(query_params)
            # if `next marker path` is explicit specified, use it as marker
            next_marker = cls.get_next_marker(response_json,
                                              yielded,
                                              query_params)
            if next_marker:
                new_marker = next_marker if next_marker != -1 else None

            # if cls.next_marker_path:
            #     if isinstance(cls.next_marker_path, six.string_types):
            #         new_marker = cls.find_value_by_accessor(response_json,
            #                                                 cls.next_marker_path)
            #     elif callable(cls.next_marker_path):
            #         new_marker = cls.next_marker_path(response_json, yielded)

            if not new_marker:
                return
            if not paginated:
                return
            if cls.query_limit_key in query_params:
                if yielded < query_params["limit"]:
                    return
            query_params[cls.query_limit_key] = yielded
            query_params[cls.query_marker_key] = new_marker

    @classmethod
    def list_by_offset(cls, session, paginated=False, **params):
        """This method is a generator which yields resource objects.

        This resource object list generator handles pagination and takes query
        params for response filtering.

        :param session: The session to use for making this request.
        :type session: :class:`~openstack.session.Session`
        :param bool paginated: ``True`` if a GET to this resource returns
                               a paginated series of responses, or ``False``
                               if a GET returns only one page of data.
                               **When paginated is False only one
                               page of data will be returned regardless
                               of the API's support of pagination.**
        :param dict params: These keyword arguments are passed through the
            :meth:`~openstack.resource2.QueryParamter._transpose` method
            to find if any of them match expected query parameters to be
            sent in the *params* argument to
            :meth:`~openstack.session.Session.get`. They are additionally
            checked against the
            :data:`~openstack.resource2.Resource.base_path` format string
            to see if any path fragments need to be filled in by the contents
            of this argument.

        :return: A generator of :class:`Resource` objects.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_list` is not set to ``True``.
        """
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        more_data = True
        query_params = cls._query_mapping._transpose(params)
        uri = cls.get_list_uri(params)
        offset = query_params.get("offset")
        limit = query_params.get("limit")

        while more_data:
            endpoint_override = cls.service.get_endpoint_override()
            resp = session.get(uri, endpoint_filter=cls.service,
                               endpoint_override=endpoint_override,
                               headers={"Accept": "application/json"},
                               params=query_params)
            response_json = resp.json()
            resources = response_json

            if not resources:
                return

            resources.pop("self", None)
            value = cls.existing(**resources)
            yield value

            if not paginated:
                return

            if offset is None:
                return

            if limit is None:
                return

            resource_list = resources[cls.resources_key]
            current_page_size = len(resource_list)

            # Check if you need to continue sending requests.
            if current_page_size < int(limit):
                return
            else:
                if int(query_params.get("offset")) == 0:
                    query_params["offset"] = 2
                else:
                    query_params["offset"] = int(query_params.get("offset")) + 1

    @classmethod
    def _get_one_match(cls, name_or_id, results):
        """Given a list of results, return the match"""
        the_result = None
        for maybe_result in results:
            id_value = cls._get_id(maybe_result)
            name_value = maybe_result.name

            if (id_value == name_or_id) or (name_value == name_or_id):
                # Only allow one resource to be found. If we already
                # found a match, raise an exception to show it.
                if the_result is None:
                    the_result = maybe_result
                else:
                    msg = "More than one %s exists with the name '%s'."
                    msg = (msg % (cls.__name__, name_or_id))
                    raise exceptions.DuplicateResource(msg)

        return the_result

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True, **params):
        """Find a resource by its name or id.

        :param session: The session to use for making this request.
        :type session: :class:`~openstack.session.Session`
        :param name_or_id: This resource's identifier, if needed by
                           the request. The default is ``None``.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :param dict params: Any additional parameters to be passed into
                            underlying methods, such as to
                            :meth:`~openstack.resource2.Resource.existing`
                            in order to pass on URI parameters.

        :return: The :class:`Resource` object matching the given name or id
                 or None if nothing matches.
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
                 than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
                 is found and ignore_missing is ``False``.
        """
        # Try to short-circuit by looking directly for a matching ID.
        try:
            match = cls.existing(id=name_or_id, **params)
            return match.get(session)
        except exceptions.NotFoundException:
            print("Resource Not Found")

        data = cls.list(session, **params)

        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))


def wait_for_status(session, resource, status,
                    failures=[], interval=5, wait=120):
    """Wait for the resource to be in a particular status.

    :param session: The session to use for making this request.
    :type session: :class:`~openstack.session.Session`
    :param resource: The resource to wait on to reach the status. The resource
                     must have a status attribute.
    :type resource: :class:`~openstack.resource.Resource`
    :param status: Desired status of the resource.
    :param list failures: Statuses that would indicate the transition
                          failed such as 'ERROR'.
    :param interval: Number of seconds to wait between checks.
    :param wait: Maximum number of seconds to wait for transition.

    :return: Method returns self on success.
    :raises: :class:`~openstack.exceptions.ResourceTimeout` transition
             to status failed to occur in wait seconds.
    :raises: :class:`~openstack.exceptions.ResourceFailure` resource
             transitioned to one of the failure states.
    :raises: :class:`~AttributeError` if the resource does not have a status
             attribute
    """
    if resource.status == status:
        return resource

    total_sleep = 0
    if failures is None:
        failures = []

    while total_sleep < wait:
        resource.get(session)
        if resource.status == status:
            return resource
        if resource.status in failures:
            msg = ("Resource %s transitioned to failure state %s" %
                   (resource.id, resource.status))
            raise exceptions.ResourceFailure(msg)
        time.sleep(interval)
        total_sleep += interval
    msg = "Timeout waiting for %s to transition to %s" % (resource.id, status)
    raise exceptions.ResourceTimeout(msg)


def wait_for_delete(session, resource, interval, wait):
    """Wait for the resource to be deleted.

    :param session: The session to use for making this request.
    :type session: :class:`~openstack.session.Session`
    :param resource: The resource to wait on to be deleted.
    :type resource: :class:`~openstack.resource.Resource`
    :param interval: Number of seconds to wait between checks.
    :param wait: Maximum number of seconds to wait for the delete.

    :return: Method returns self on success.
    :raises: :class:`~openstack.exceptions.ResourceTimeout` transition
             to status failed to occur in wait seconds.
    """
    total_sleep = 0
    while total_sleep < wait:
        try:
            resource.get(session)
        except exceptions.NotFoundException:
            return resource
        time.sleep(interval)
        total_sleep += interval
    msg = "Timeout waiting for %s delete" % (resource.id)
    raise exceptions.ResourceTimeout(msg)
