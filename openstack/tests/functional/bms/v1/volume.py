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
import os

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

os.environ.setdefault(
    'OS_BMS_ENDPOINT_OVERRIDE',
    'https://******/v1/%(project_id)s'
)
print('endpoint: ' + os.environ.get('OS_BMS_ENDPOINT_OVERRIDE'))


def mount_disk(_conn):
    data = {
        "volumeId": "abc123",
        "device": ""
    }
    mount = _conn.bms.create_volume_attachment('******', **data)
    print(mount)


def umount_disk(_conn):
    umount = _conn.bms.delete_volume_attachment('******', 'abc123')
    print(umount)


if __name__ == "__main__":
    # mount_disk(conn)
    # umount_disk(conn)
    pass
