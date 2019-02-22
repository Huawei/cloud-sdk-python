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


def ips(_conn):
    query = {
        # "id": "f01a9741-baee-41a6-b973-dcb6b2c22b26"
    }
    fips = _conn.network.ips(**query)
    for fip in fips:
        print(fip)


def get_ip(_conn):
    print(_conn.network.get_ip('0b77dfd6-9a4b-41d0-8f85-40fcf52073ab'))


def create_ip(_conn):
    data = {
        "floating_network_id": "0a2228f2-7f8a-45f1-8e09-9039e1d09975"
    }
    print(_conn.network.create_ip(**data))


def update_ip(_conn):
    data = {
        "fixed_ip_address": "192.168.1.109"
    }
    print(_conn.network.update_ip('0b77dfd6-9a4b-41d0-8f85-40fcf52073ab', **data))


def delete_ip(_conn):
    print(_conn.network.delete_ip('0b77dfd6-9a4b-41d0-8f85-40fcf52073ab'))


if __name__ == '__main__':
    # ips(conn)
    # get_ip(conn)
    # create_ip(conn)
    # update_ip(conn)
    # delete_ip(conn)
    pass
