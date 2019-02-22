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


class Quota(resource.Resource):
    resource_key = 'quota'
    resources_key = 'quotas'
    base_path = '/quotas'
    service = network_service.NetworkService()

    # capabilities
    allow_get = True
    allow_update = True
    allow_delete = True
    allow_list = True

    # Properties
    #: The maximum amount of floating IPs you can have. *Type: int*
    floating_ips = resource.Body('floatingip', type=int)
    #: The maximum amount of health monitors you can create. *Type: int*
    health_monitors = resource.Body('healthmonitor', type=int)
    #: The maximum amount of listeners you can create. *Type: int*
    listeners = resource.Body('listener', type=int)
    #: The maximum amount of load balancers you can create. *Type: int*
    load_balancers = resource.Body('loadbalancer', type=int)
    #: The maximum amount of L7 policies you can create. *Type: int*
    l7_policies = resource.Body('l7policy', type=int)
    #: The maximum amount of networks you can create. *Type: int*
    networks = resource.Body('network', type=int)
    #: The maximum amount of pools you can create. *Type: int*
    pools = resource.Body('pool', type=int)
    #: The maximum amount of ports you can create. *Type: int*
    ports = resource.Body('port', type=int)
    #: The ID of the project these quota values are for.
    project_id = resource.Body('tenant_id', alternate_id=True)
    #: The maximum amount of RBAC policies you can create. *Type: int*
    rbac_policies = resource.Body('rbac_policy', type=int)
    #: The maximum amount of routers you can create. *Type: int*
    routers = resource.Body('router', type=int)
    #: The maximum amount of subnets you can create. *Type: int*
    subnets = resource.Body('subnet', type=int)
    #: The maximum amount of subnet pools you can create. *Type: int*
    subnet_pools = resource.Body('subnetpool', type=int)
    #: The maximum amount of security group rules you can create. *Type: int*
    security_group_rules = resource.Body('security_group_rule', type=int)
    #: The maximum amount of security groups you can create. *Type: int*
    security_groups = resource.Body('security_group', type=int)

    def _prepare_request(self, requires_id=True, prepend_key=False):
        _request = super(Quota, self)._prepare_request(requires_id,
                                                       prepend_key)
        if self.resource_key in _request.body:
            _body = _request.body[self.resource_key]
        else:
            _body = _request.body
        if 'id' in _body:
            del _body['id']
        return _request


class QuotaDefault(Quota):
    base_path = '/quotas/%(project)s/default'

    # capabilities
    allow_retrieve = True
    allow_update = False
    allow_delete = False
    allow_list = False

    # Properties
    #: The ID of the project.
    project = resource.URI('project')
