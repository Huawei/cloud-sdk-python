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

import mock
import testtools

from openstack.network.v2 import floating_ip

IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    'created_at': '0',
    'fixed_ip_address': '1',
    'floating_ip_address': '127.0.0.1',
    'floating_network_id': '3',
    'id': IDENTIFIER,
    'port_id': '5',
    'tenant_id': '6',
    'router_id': '7',
    'description': '8',
    'status': 'ACTIVE',
    'revision_number': 12,
    'updated_at': '13',
}


class TestFloatingIP(testtools.TestCase):

    def test_basic(self):
        sot = floating_ip.FloatingIP()
        self.assertEqual('floatingip', sot.resource_key)
        self.assertEqual('floatingips', sot.resources_key)
        self.assertEqual('/floatingips', sot.base_path)
        self.assertEqual('network', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)

        self.assertDictEqual(
            {
                "description": "description",
                "fixed_ip_address": "fixed_ip_address",
                "floating_ip_address": "floating_ip_address",
                "floating_network_id": "floating_network_id",
                "port_id": "port_id",
                "router_id": "router_id",
                "status": "status",
                "limit": "limit",
                "marker": "marker",
                "page_reverse": "page_reverse",
                "id": "id",
                "project_id": "tenant_id"
            },
            sot._query_mapping._mapping
        )

    def test_make_it(self):
        sot = floating_ip.FloatingIP(**EXAMPLE)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['fixed_ip_address'], sot.fixed_ip_address)
        self.assertEqual(EXAMPLE['floating_ip_address'],
                         sot.floating_ip_address)
        self.assertEqual(EXAMPLE['floating_network_id'],
                         sot.floating_network_id)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['port_id'], sot.port_id)
        self.assertEqual(EXAMPLE['tenant_id'], sot.project_id)
        self.assertEqual(EXAMPLE['router_id'], sot.router_id)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['revision_number'], sot.revision_number)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)

    def test_find_available(self):
        mock_session = mock.Mock()
        mock_session.get_filter = mock.Mock(return_value={})
        data = {'id': 'one', 'floating_ip_address': '10.0.0.1'}
        fake_response = mock.Mock()
        body = {floating_ip.FloatingIP.resources_key: [data]}
        fake_response.json = mock.Mock(return_value=body)
        mock_session.get = mock.Mock(return_value=fake_response)

        result = floating_ip.FloatingIP.find_available(mock_session)

        self.assertEqual('one', result.id)
        mock_session.get.assert_called_with(
            floating_ip.FloatingIP.base_path,
            endpoint_filter=floating_ip.FloatingIP.service,
            endpoint_override=None,
            headers={'Accept': 'application/json'},
            params={'port_id': ''})

    def test_find_available_nada(self):
        mock_session = mock.Mock()
        fake_response = mock.Mock()
        body = {floating_ip.FloatingIP.resources_key: []}
        fake_response.json = mock.Mock(return_value=body)
        mock_session.get = mock.Mock(return_value=fake_response)

        self.assertIsNone(floating_ip.FloatingIP.find_available(mock_session))
