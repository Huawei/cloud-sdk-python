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

from openstack.identity import identity_service
from openstack import resource2 as resource


class Policy(resource.Resource):
    resource_key = 'policy'
    resources_key = 'policies'
    base_path = '/policies'
    service = identity_service.IdentityService()

    # capabilities
    allow_create = True
    allow_get = True
    allow_update = True
    allow_delete = True
    allow_list = True
    patch_update = True

    # Properties
    #: The policy rule set itself, as a serialized blob. *Type: string*
    blob = resource.Body('blob')
    #: The links for the policy resource.
    links = resource.Body('links')
    #: The ID for the project.
    project_id = resource.Body('project_id')
    #: The MIME Media Type of the serialized policy blob. *Type: string*
    type = resource.Body('type')
    #: The ID of the user who owns the policy
    user_id = resource.Body('user_id')
