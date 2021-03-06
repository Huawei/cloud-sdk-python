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

import os

from openstack import connection

auth_url = '******'
userDomainId = '******'
projectId = '******'
username = '******'
password = os.getenv('get_secret_code')

conn = connection.Connection(
    auth_url=auth_url,
    user_domain_id=userDomainId,
    project_id=projectId,
    username=username,
    password=password
)

os.environ.setdefault(
    'OS_VPCV2.0_ENDPOINT_OVERRIDE',
    'https://vpc.xxx.yyy.com/v2.0/%(project_id)s'
)


def create_publicip_ext(_conn):
    data = {
        "publicip": {
            "type": "5_bgp"
                },
        "bandwidth": {
            "name": "bandwidthDemo",
            "size": 10,
            "share_type": "PER"
        }
    }
    print(_conn.vpc.create_publicip_ext(**data))


if __name__ == '__main__':
    create_publicip_ext(conn)
