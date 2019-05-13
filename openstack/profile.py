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
:class:`~openstack.profile.Profile` is the class that is used to
define the various preferences for different services.  The preferences that
are currently supported are service name, region, version and interface.
The :class:`~openstack.profile.Profile` and the
:class:`~openstack.connection.Connection` classes are the most important
user facing classes.

Examples
--------

The :class:`~openstack.profile.Profile` class is constructed
with no arguments.

Set Methods
~~~~~~~~~~~

A user's preferences are set based on the service type.  Service type would
normally be something like 'compute', 'identity', 'object-store', etc.::

    from openstack import profile
    prof = profile.Profile()
    prof.set_name('compute', 'matrix')
    prof.set_region(prof.ALL, 'zion')
    prof.set_version('identity', 'v3')
    prof.set_interface('object-store', 'internal')
    for service in prof.get_services():
        print(prof.get_filter(service.service_type)

The resulting preference print out would look something like::

    service_type=compute,region=zion,service_name=matrix
    service_type=network,region=zion
    service_type=database,region=zion
    service_type=image,region=zion
    service_type=metering,region=zion
    service_type=orchestration,region=zion
    service_type=object-store,interface=internal,region=zion
    service_type=identity,region=zion,version=v3
"""

import copy
import logging

import six

from openstack import exceptions
from openstack import module_loader
from openstack.anti_ddos import anti_ddos_service
from openstack.auto_scaling import auto_scaling_service
from openstack.block_store import block_store_service
from openstack.cdn import cdn_service
from openstack.cloud_eye import cloud_eye_service
from openstack.compute import compute_service
from openstack.cts import cts_service
from openstack.dms import dms_service
from openstack.dns import dns_service
from openstack.ecs import ecs_service
from openstack.evs import evs_service
from openstack.identity import identity_service
from openstack.image import image_service
from openstack.kms import kms_service
from openstack.load_balancer import load_balancer_service as lb_service
from openstack.maas import maas_service
from openstack.map_reduce import map_reduce_service
from openstack.network import network_service
from openstack.orchestration import orchestration_service
from openstack.smn import smn_service
from openstack.volume_backup import volume_backup_service
from openstack.vpc import vpc_service
from openstack.bms import bms_service
from openstack.deh import deh_service
from openstack.csbs import csbs_service
from openstack.ims import ims_service
from openstack.nat import nat_service
# from openstack.key_manager import key_manager_service
# from openstack.bare_metal import bare_metal_service
# from openstack.cluster import cluster_service
# from openstack.database import database_service
# from openstack.message import message_service
# from openstack.object_store import object_store_service
from openstack.rds import rds_service
# from openstack.rds_os import rds_os_service
# from openstack.telemetry.alarm import alarm_service
# from openstack.telemetry import telemetry_service
# from openstack.workflow import workflow_service
from openstack.iam import iam_service

_logger = logging.getLogger(__name__)


class Profile(object):

    ALL = "*"
    """Wildcard service identifier representing all services."""

    def __init__(self, plugins=None):
        """User preference for each service.

        :param plugins: List of entry point namespaces to load.

        Create a new :class:`~openstack.profile.Profile`
        object with no preferences defined, but knowledge of the services.
        Services are identified by their service type, e.g.: 'identity',
        'compute', etc.
        """
        self._services = {}

        self._add_service(anti_ddos_service.AntiDDosService(version="v1"))
        self._add_service(block_store_service.BlockStoreService(version="v2"))
        self._add_service(compute_service.ComputeService(version="v2"))
        self._add_service(cts_service.CTSService(version="v1"))
        self._add_service(dms_service.DMSService(version="v1"))
        self._add_service(identity_service.IdentityService(version="v3"))
        self._add_service(image_service.ImageService(version="v2"))
        self._add_service(kms_service.KMSService(version="v1"))
        self._add_service(maas_service.MaaSService(version="v1"))
        self._add_service(network_service.NetworkService(version="v2.0"))
        self._add_service(orchestration_service.OrchestrationService(version="v1"))
        self._add_service(smn_service.SMNService(version="v2"))
        # QianBiao.NG HuaWei Services
        self._add_service(dns_service.DNSService(version="v2"))
        self._add_service(cloud_eye_service.CloudEyeService(version="v1"))
        ass = auto_scaling_service.AutoScalingService(version="v1")
        self._add_service(ass)
        vbs_v2 = volume_backup_service.VolumeBackupService(version="v2")
        self._add_service(vbs_v2)
        self._add_service(map_reduce_service.MapReduceService(version="v1"))
        self._add_service(evs_service.EvsServiceV2_1(version='v2.1'))
        self._add_service(evs_service.EvsService(version='v2'))
        self._add_service(ecs_service.EcsService(version='v1'))
        self._add_service(ecs_service.EcsServiceV1_1(version='v1.1'))
        self._add_service(vpc_service.VpcService(version='v2.0'))
        self._add_service(vpc_service.VpcServiceV1(version='v1'))
        self._add_service(bms_service.BmsService(version='v1'))
        self._add_service(deh_service.DehService(version='v1.0'))
        self._add_service(csbs_service.CsbsService(version='v1'))
        self._add_service(ims_service.ImsService(version='v2'))
        self._add_service(nat_service.NatService(version='v2.0'))
        self._add_service(lb_service.LoadBalancerService(version='v1'))
        # not support below service
        # self._add_service(message_service.MessageService(version="v1"))
        # self._add_service(cluster_service.ClusterService(version="v1"))
        # self._add_service(database_service.DatabaseService(version="v1"))
        # self._add_service(alarm_service.AlarmService(version="v2"))
        # self._add_service(bare_metal_service.BareMetalService(version="v1"))
        # self._add_service(key_manager_service.KeyManagerService(version="v1"))
        # self._add_service(
            # object_store_service.ObjectStoreService(version="v1"))

        self._add_service(rds_service.RDSService(version="v1"))
        self._add_service(cdn_service.CDNService(version='v1'))
        self._add_service(iam_service.IamService(version='v3.0'))

        # self._add_service(rds_os_service.RDSService(version="v1"))
        # self._add_service(telemetry_service.TelemetryService(version="v2"))
        # self._add_service(workflow_service.WorkflowService(version="v2"))
        if plugins:
            for plugin in plugins:
                self._load_plugin(plugin)
        self.service_keys = sorted(self._services.keys())

    def __repr__(self):
        return repr(self._services)

    def _add_service(self, serv):
        serv.interface = None
        self._services[serv.service_type] = serv

    def _load_plugin(self, namespace):
        """Load a service plugin.

        :param str namespace: Entry point namespace
        """
        services = module_loader.load_service_plugins(namespace)
        for service_type in services:
            if service_type in self._services:
                _logger.debug("Overriding %s with %s", service_type,
                              services[service_type])
            self._add_service(services[service_type])

    def get_filter(self, service):
        """Get a service preference.

        :param str service: Desired service type.
        """
        return copy.copy(self._get_filter(service))

    def _get_filter(self, service):
        """Get a service preference.

        :param str service: Desired service type.
        """
        serv = self._services.get(service, None)
        if serv is not None:
            return serv
        msg = ("Service %s not in list of valid services: %s" %
               (service, self.service_keys))
        raise exceptions.SDKException(msg)

    def _get_services(self, service):
        return self.service_keys if service == self.ALL else [service]

    def _setter(self, service, attr, value):
        for service in self._get_services(service):
            setattr(self._get_filter(service), attr, value)

    def get_services(self):
        """Get a list of all the known services."""
        services = []
        for name, service in six.iteritems(self._services):
            services.append(service)
        return services

    def set_name(self, service, name):
        """Set the desired name for the specified service.

        :param str service: Service type.
        :param str name: Desired service name.
        """
        self._setter(service, "service_name", name)

    def set_region(self, service, region):
        """Set the desired region for the specified service.

        :param str service: Service type.
        :param str region: Desired service region.
        """
        self._setter(service, "region", region)

    def set_version(self, service, version):
        """Set the desired version for the specified service.

        :param str service: Service type.
        :param str version: Desired service version.
        """
        self._get_filter(service).version = version

    def set_api_version(self, service, api_version):
        """Set the desired API micro-version for the specified service.

        :param str service: Service type.
        :param str api_version: Desired service API micro-version.
        """
        self._setter(service, "api_version", api_version)

    def set_interface(self, service, interface):
        """Set the desired interface for the specified service.

        :param str service: Service type.
        :param str interface: Desired service interface.
        """
        self._setter(service, "interface", interface)
