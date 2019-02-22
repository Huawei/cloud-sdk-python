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

from openstack.telemetry.alarm.v2 import _proxy
from openstack.telemetry.alarm.v2 import alarm
from openstack.telemetry.alarm.v2 import alarm_change
from openstack.tests.unit import test_proxy_base


class TestAlarmProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestAlarmProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_alarm_change_find(self):
        self.verify_find(self.proxy.find_alarm_change,
                         alarm_change.AlarmChange)

    def test_alarm_changes(self):
        larm = alarm.Alarm.existing(alarm_id='larm')
        expected_kwargs = {'path_args': {'alarm_id': 'larm'}}
        self.verify_list(self.proxy.alarm_changes, alarm_change.AlarmChange,
                         method_args=[larm], paginated=False,
                         expected_kwargs=expected_kwargs)

    def test_alarm_create_attrs(self):
        self.verify_create(self.proxy.create_alarm, alarm.Alarm)

    def test_alarm_delete(self):
        self.verify_delete(self.proxy.delete_alarm, alarm.Alarm, False)

    def test_alarm_delete_ignore(self):
        self.verify_delete(self.proxy.delete_alarm, alarm.Alarm, True)

    def test_alarm_find(self):
        self.verify_find(self.proxy.find_alarm, alarm.Alarm)

    def test_alarm_get(self):
        self.verify_get(self.proxy.get_alarm, alarm.Alarm)

    def test_alarms(self):
        self.verify_list(self.proxy.alarms, alarm.Alarm, paginated=False)

    def test_alarm_update(self):
        self.verify_update(self.proxy.update_alarm, alarm.Alarm)
