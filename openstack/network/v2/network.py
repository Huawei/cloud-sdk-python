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

from openstack.network import network_service
from openstack import resource2 as resource


class Network(resource.Resource):
    resource_key = 'network'
    resources_key = 'networks'
    base_path = '/networks'
    service = network_service.NetworkService()

    # capabilities
    allow_create = True
    allow_get = True
    allow_update = True
    allow_delete = True
    allow_list = True

    # NOTE: We don't support query on list or datetime fields yet
    _query_mapping = resource.QueryParameters(
        'description', 'name', 'project_id', 'status',
        'page_reverse', 'id', 'tenant_id',
        ipv4_address_scope_id='ipv4_address_scope',
        ipv6_address_scope_id='ipv6_address_scope',
        is_admin_state_up='admin_state_up',
        is_port_security_enabled='port_security_enabled',
        is_router_external='router:external',
        is_shared='shared',
        provider_network_type='provider:network_type',
        provider_physical_network='provider:physical_network',
        provider_segmentation_id='provider:segmentation_id',
    )

    # Properties
    #: Availability zone hints to use when scheduling the network.
    #: *Type: list of availability zone names*
    availability_zone_hints = resource.Body('availability_zone_hints')
    #: Availability zones for the network.
    #: *Type: list of availability zone names*
    availability_zones = resource.Body('availability_zones')
    #: Timestamp when the network was created.
    created_at = resource.Body('created_at')
    #: The network description.
    description = resource.Body('description')
    #: The DNS domain associated.
    dns_domain = resource.Body('dns_domain')
    #: The ID of the IPv4 address scope for the network.
    ipv4_address_scope_id = resource.Body('ipv4_address_scope')
    #: The ID of the IPv6 address scope for the network.
    ipv6_address_scope_id = resource.Body('ipv6_address_scope')
    #: The administrative state of the network, which is up ``True`` or
    #: down ``False``. *Type: bool*
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Whether or not this is the default external network.
    #: *Type: bool*
    is_default = resource.Body('is_default', type=bool)
    #: The port security status, which is enabled ``True`` or disabled
    #: ``False``. *Type: bool* *Default: False*
    #: Available for multiple provider extensions.
    is_port_security_enabled = resource.Body('port_security_enabled',
                                             type=bool,
                                             default=False)
    #: Whether or not the router is external.
    #: *Type: bool* *Default: False*
    is_router_external = resource.Body('router:external', type=bool,
                                       default=False)
    #: Indicates whether this network is shared across all tenants.
    #: By default, only administrative users can change this value.
    #: *Type: bool*
    is_shared = resource.Body('shared', type=bool)
    #: Read-only. The maximum transmission unit (MTU) of the network resource.
    mtu = resource.Body('mtu', type=int)
    #: The network name.
    name = resource.Body('name')
    #: The ID of the project this network is associated with.
    project_id = resource.Body('project_id')
    #: The type of physical network that maps to this network resource.
    #: For example, ``flat``, ``vlan``, ``vxlan``, or ``gre``.
    #: Available for multiple provider extensions.
    provider_network_type = resource.Body('provider:network_type')
    #: The physical network where this network object is implemented.
    #: Available for multiple provider extensions.
    provider_physical_network = resource.Body('provider:physical_network')
    #: An isolated segment ID on the physical network. The provider
    #: network type defines the segmentation model.
    #: Available for multiple provider extensions.
    provider_segmentation_id = resource.Body('provider:segmentation_id')
    #: The ID of the QoS policy attached to the port.
    qos_policy_id = resource.Body('qos_policy_id')
    #: Revision number of the network. *Type: int*
    revision_number = resource.Body('revision_number', type=int)
    #: A list of provider segment objects.
    #: Available for multiple provider extensions.
    segments = resource.Body('segments')
    #: The network status.
    status = resource.Body('status')
    #: The associated subnet IDs.
    #: *Type: list of strs of the subnet IDs*
    subnet_ids = resource.Body('subnets', type=list)
    #: Timestamp when the network was last updated.
    updated_at = resource.Body('updated_at')
    #: Indicates the VLAN transparency mode of the network
    is_vlan_transparent = resource.Body('vlan_transparent', type=bool)
    #: The ID of the project this network is associated with.
    tenant_id = resource.Body('tenant_id')


class DHCPAgentHostingNetwork(Network):
    resource_key = 'network'
    resources_key = 'networks'
    base_path = '/agents/%(agent_id)s/dhcp-networks'
    resource_name = 'dhcp-network'
    service = network_service.NetworkService()

    # capabilities
    allow_create = False
    allow_get = True
    allow_update = False
    allow_delete = False
    allow_list = True

    # NOTE: No query parameter is supported
