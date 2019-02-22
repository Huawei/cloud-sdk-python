# -*- coding:utf-8 -*-
# Copyright 2018 Huawei Technologies Co.,Ltd.
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

from openstack import resource2
from openstack.network import network_service


class Statuses(resource2.Resource):
    resource_key = 'statuses'
    resources_key = 'statuses'
    base_path = '/lbaas/loadbalancers/%(loadbalance_id)s/statuses'
    service = network_service.NetworkService()

    allow_create = False
    allow_get = True
    allow_update = False
    allow_delete = False
    allow_list = False
    # loadbalancer
    loadbalancer = resource2.Body("loadbalancer", type=dict)
    # loadbalancer id
    loadbalance_id = resource2.URI("loadbalance_id")

