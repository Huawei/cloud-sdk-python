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


class QoSPolicy(resource.Resource):
    resource_key = 'policy'
    resources_key = 'policies'
    base_path = '/qos/policies'
    service = network_service.NetworkService()

    # capabilities
    allow_create = True
    allow_get = True
    allow_update = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'name', 'description', 'is_default',
        project_id='tenant_id',
        is_shared='shared',
    )

    # Properties
    #: QoS policy name.
    name = resource.Body('name')
    #: The ID of the project who owns the network. Only administrative
    #: users can specify a project ID other than their own.
    project_id = resource.Body('tenant_id')
    #: The QoS policy description.
    description = resource.Body('description')
    #: Indicates whether this QoS policy is the default policy for this
    #: project.
    #: *Type: bool*
    is_default = resource.Body('is_default', type=bool)
    #: Indicates whether this QoS policy is shared across all projects.
    #: *Type: bool*
    is_shared = resource.Body('shared', type=bool)
    #: List of QoS rules applied to this QoS policy.
    rules = resource.Body('rules')
