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

from openstack.orchestration.v1 import template
from openstack import resource2 as resource


FAKE = {
    'Description': 'Blah blah',
    'Parameters': {
        'key_name': {
            'type': 'string'
        }
    },
    'ParameterGroups': [{
        'label': 'Group 1',
        'parameters': ['key_name']
    }]
}


class TestTemplate(testtools.TestCase):

    def test_basic(self):
        sot = template.Template()
        self.assertEqual('orchestration', sot.service.service_type)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_list)

    def test_make_it(self):
        sot = template.Template(**FAKE)
        self.assertEqual(FAKE['Description'], sot.description)
        self.assertEqual(FAKE['Parameters'], sot.parameters)
        self.assertEqual(FAKE['ParameterGroups'], sot.parameter_groups)

    @mock.patch.object(resource.Resource, '_translate_response')
    def test_validate(self, mock_translate):
        sess = mock.Mock()
        sot = template.Template()
        tmpl = mock.Mock()
        body = {'template': tmpl}

        sot.validate(sess, tmpl)

        sess.post.assert_called_once_with(
            '/validate', endpoint_filter=sot.service, json=body)
        mock_translate.assert_called_once_with(sess.post.return_value)

    @mock.patch.object(resource.Resource, '_translate_response')
    def test_validate_with_env(self, mock_translate):
        sess = mock.Mock()
        sot = template.Template()
        tmpl = mock.Mock()
        env = mock.Mock()
        body = {'template': tmpl, 'environment': env}

        sot.validate(sess, tmpl, environment=env)

        sess.post.assert_called_once_with(
            '/validate', endpoint_filter=sot.service, json=body)
        mock_translate.assert_called_once_with(sess.post.return_value)

    @mock.patch.object(resource.Resource, '_translate_response')
    def test_validate_with_template_url(self, mock_translate):
        sess = mock.Mock()
        sot = template.Template()
        template_url = 'http://host1'
        body = {'template': None, 'template_url': template_url}

        sot.validate(sess, None, template_url=template_url)

        sess.post.assert_called_once_with(
            '/validate', endpoint_filter=sot.service, json=body)
        mock_translate.assert_called_once_with(sess.post.return_value)

    @mock.patch.object(resource.Resource, '_translate_response')
    def test_validate_with_ignore_errors(self, mock_translate):
        sess = mock.Mock()
        sot = template.Template()
        tmpl = mock.Mock()
        body = {'template': tmpl}

        sot.validate(sess, tmpl, ignore_errors='123,456')

        sess.post.assert_called_once_with(
            '/validate?ignore_errors=123%2C456',
            endpoint_filter=sot.service, json=body)
        mock_translate.assert_called_once_with(sess.post.return_value)
