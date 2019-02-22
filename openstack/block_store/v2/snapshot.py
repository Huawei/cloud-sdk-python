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

from openstack.block_store import block_store_service
from openstack import format
from openstack import resource2


class Snapshot(resource2.Resource):
    resource_key = "snapshot"
    resources_key = "snapshots"
    base_path = "/snapshots"
    service = block_store_service.BlockStoreService()

    _query_mapping = resource2.QueryParameters('all_tenants', 'name', 'status',
                                               'volume_id', "offset")

    # capabilities
    allow_get = True
    allow_create = True
    allow_delete = True
    allow_update = True
    allow_list = True

    # Properties
    #: A ID representing this snapshot.
    id = resource2.Body("id")
    #: Name of the snapshot. Default is None.
    name = resource2.Body("name")

    #: The current status of this snapshot. Potential values are creating,
    #: available, deleting, error, and error_deleting.
    status = resource2.Body("status")
    #: Description of snapshot. Default is None.
    description = resource2.Body("description")
    #: The timestamp of this snapshot creation.
    created_at = resource2.Body("created_at")
    #: Metadata associated with this snapshot.
    metadata = resource2.Body("metadata", type=dict)
    #: The ID of the volume this snapshot was taken of.
    volume_id = resource2.Body("volume_id")
    #: The size of the volume, in GBs.
    size = resource2.Body("size", type=int)
    #: Indicate whether to create snapshot, even if the volume is attached.
    #: Default is ``False``. *Type: bool*
    is_forced = resource2.Body("force", type=format.BoolStr)
    #: Update time.
    updated_at = resource2.Body("updated_at")
    #: Same as name.
    display_name = resource2.Body("display_name")
    #: Same as description.
    display_description = resource2.Body("display_description")


class SnapshotDetail(Snapshot):

    base_path = "/snapshots/detail"

    #: The percentage of completeness the snapshot is currently at.
    progress = resource2.Body("os-extended-snapshot-attributes:progress")
    #: The project ID this snapshot is associated with.
    project_id = resource2.Body("os-extended-snapshot-attributes:project_id")
