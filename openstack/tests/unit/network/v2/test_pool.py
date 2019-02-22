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

import testtools

from openstack.network.v2 import pool

IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    'admin_state_up': True,
    'description': '2',
    'id': IDENTIFIER,
    'lb_algorithm': '5',
    'listeners': [{'id': '6'}],
    "listener_id": "listener_id",
    'members': [{'id': '7'}],
    'name': '8',
    'tenant_id': '9',
    'protocol': '10',
    'provider': '11',
    'session_persistence': {},
    'status': '13',
    'status_description': '14',
    'subnet_id': '15',
    'loadbalancer_id': '',
    'healthmonitor_id': '17',
}


class TestPool(testtools.TestCase):

    def test_basic(self):
        sot = pool.Pool()
        self.assertEqual('pool', sot.resource_key)
        self.assertEqual('pools', sot.resources_key)
        self.assertEqual('/lbaas/pools', sot.base_path)
        self.assertEqual('network', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)
        self.assertDictEqual(
            {
                "limit": "limit",
                "marker": "marker",
                "page_reverse": "page_reverse",
                "id": "id",
                "name": "name",
                "description": "description",
                "healthmonitor_id": "healthmonitor_id",
                "loadbalancer_id": "loadbalancer_id",
                "protocol": "protocol",
                "lb_algorithm": "lb_algorithm",
                "member_address": "member_address" ,
                "member_device_id": "member_device_id"
            },
            pool.Pool._query_mapping._mapping
        )

    def test_make_it(self):
        sot = pool.Pool(**EXAMPLE)
        self.assertTrue(sot.admin_state_up)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['lb_algorithm'], sot.lb_algorithm)
        self.assertEqual(EXAMPLE['listeners'], sot.listeners)
        self.assertEqual(EXAMPLE['listener_id'], sot.listener_id)
        self.assertEqual(EXAMPLE['members'], sot.members)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['tenant_id'], sot.tenant_id)
        self.assertEqual(EXAMPLE['protocol'], sot.protocol)
        self.assertEqual(EXAMPLE['session_persistence'],
                         sot.session_persistence)
        self.assertEqual(EXAMPLE['loadbalancer_id'], sot.loadbalancer_id)
        self.assertEqual(EXAMPLE['healthmonitor_id'], sot.healthmonitor_id)
