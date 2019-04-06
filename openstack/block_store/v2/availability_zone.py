# -*- coding:utf-8 -*-
# Copyright 2019 Huawei Technologies Co.,Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License.  You may obtain a copy of the
# License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.

from openstack import resource2 as resource
from openstack.block_store import block_store_service


class AvailabilityZone(resource.Resource):
    resource_key = None
    resources_key = 'availabilityZoneInfo'
    base_path = '/os-availability-zone'
    service = block_store_service.BlockStoreService()

    # capabilities
    allow_list = True

    # Properties
    #: The AZ status.
    zoneState = resource.Body('zoneState', type=dict)
    #: The AZ name.
    zoneName = resource.Body('zoneName')
