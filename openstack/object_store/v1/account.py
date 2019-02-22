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

from openstack.object_store.v1 import _base
from openstack import resource


class Account(_base.BaseResource):
    _custom_metadata_prefix = "X-Account-Meta-"

    base_path = "/"

    allow_retrieve = True
    allow_update = True
    allow_head = True

    #: The total number of bytes that are stored in Object Storage for
    #: the account.
    account_bytes_used = resource.header("x-account-bytes-used", type=int)
    #: The number of containers.
    account_container_count = resource.header("x-account-container-count",
                                              type=int)
    #: The number of objects in the account.
    account_object_count = resource.header("x-account-object-count", type=int)
    #: The secret key value for temporary URLs. If not set,
    #: this header is not returned by this operation.
    meta_temp_url_key = resource.header("x-account-meta-temp-url-key")
    #: A second secret key value for temporary URLs. If not set,
    #: this header is not returned by this operation.
    meta_temp_url_key_2 = resource.header("x-account-meta-temp-url-key-2")
    #: The timestamp of the transaction.
    timestamp = resource.header("x-timestamp")
