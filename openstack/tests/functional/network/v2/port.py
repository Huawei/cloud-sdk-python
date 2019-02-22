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

import sys
import warnings

from openstack import utils
from openstack import connection

utils.enable_logging(debug=False, stream=sys.stdout)
warnings.filterwarnings('ignore')

auth_url = '******'
userDomainId = '******'
projectId = '******'
username = '******'
password = '******'

conn = connection.Connection(
    auth_url=auth_url,
    user_domain_id=userDomainId,
    project_id=projectId,
    username=username,
    password=password,
    verify=False
)


def ports(_conn):
    query = {
        "admin_state_up": False,
    }
    pts = _conn.network.ports(**query)
    for pt in pts:
        print(pt)


def get_port(_conn):
    print(_conn.network.get_port('8b450a6a-579c-47c7-a9cb-13bc95af6a02'))


def create_port(_conn):
    data = {
        "network_id": "6df498a2-3480-4faf-b6e7-ac25a053bbbc",
    }
    print(_conn.network.create_port(**data))


def update_port(_conn):
    data = {
        "name": "port-test-20181018",
    }
    print(_conn.network.update_port('8b450a6a-579c-47c7-a9cb-13bc95af6a02', **data))


def delete_port(_conn):
    print(_conn.network.delete_port('8b450a6a-579c-47c7-a9cb-13bc95af6a02'))


if __name__ == '__main__':
    # ports(conn)
    # get_port(conn)
    # create_port(conn)
    # update_port(conn)
    # delete_port(conn)
    pass
