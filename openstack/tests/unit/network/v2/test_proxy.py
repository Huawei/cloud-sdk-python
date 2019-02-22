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

import deprecation
import mock
import uuid

from openstack.network.v2 import _proxy
from openstack.network.v2 import address_scope
from openstack.network.v2 import agent
from openstack.network.v2 import auto_allocated_topology
from openstack.network.v2 import availability_zone
from openstack.network.v2 import extension
from openstack.network.v2 import flavor
from openstack.network.v2 import floating_ip
from openstack.network.v2 import health_monitor
from openstack.network.v2 import listener
from openstack.network.v2 import load_balancer
from openstack.network.v2 import metering_label
from openstack.network.v2 import metering_label_rule
from openstack.network.v2 import network
from openstack.network.v2 import network_ip_availability
from openstack.network.v2 import pool
from openstack.network.v2 import pool_member
from openstack.network.v2 import port
from openstack.network.v2 import qos_bandwidth_limit_rule
from openstack.network.v2 import qos_dscp_marking_rule
from openstack.network.v2 import qos_minimum_bandwidth_rule
from openstack.network.v2 import qos_policy
from openstack.network.v2 import qos_rule_type
from openstack.network.v2 import quota
from openstack.network.v2 import rbac_policy
from openstack.network.v2 import router
from openstack.network.v2 import security_group
from openstack.network.v2 import security_group_rule
from openstack.network.v2 import segment
from openstack.network.v2 import service_profile
from openstack.network.v2 import service_provider
from openstack.network.v2 import subnet
from openstack.network.v2 import subnet_pool
from openstack.network.v2 import vpn_service
from openstack import proxy2 as proxy_base2
from openstack.tests.unit import test_proxy_base2


QOS_POLICY_ID = 'qos-policy-id-' + uuid.uuid4().hex
QOS_RULE_ID = 'qos-rule-id-' + uuid.uuid4().hex
NETWORK_ID = 'network-id-' + uuid.uuid4().hex
AGENT_ID = 'agent-id-' + uuid.uuid4().hex
ROUTER_ID = 'router-id-' + uuid.uuid4().hex


class TestNetworkProxy(test_proxy_base2.TestProxyBase):
    def setUp(self):
        super(TestNetworkProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_address_scope_create_attrs(self):
        self.verify_create(self.proxy.create_address_scope,
                           address_scope.AddressScope)

    def test_address_scope_delete(self):
        self.verify_delete(self.proxy.delete_address_scope,
                           address_scope.AddressScope,
                           False)

    def test_address_scope_delete_ignore(self):
        self.verify_delete(self.proxy.delete_address_scope,
                           address_scope.AddressScope,
                           True)

    def test_address_scope_find(self):
        self.verify_find(self.proxy.find_address_scope,
                         address_scope.AddressScope)

    def test_address_scope_get(self):
        self.verify_get(self.proxy.get_address_scope,
                        address_scope.AddressScope)

    def test_address_scopes(self):
        self.verify_list(self.proxy.address_scopes,
                         address_scope.AddressScope,
                         paginated=False)

    def test_address_scope_update(self):
        self.verify_update(self.proxy.update_address_scope,
                           address_scope.AddressScope)

    def test_agent_delete(self):
        self.verify_delete(self.proxy.delete_agent, agent.Agent, True)

    def test_agent_get(self):
        self.verify_get(self.proxy.get_agent, agent.Agent)

    def test_agents(self):
        self.verify_list(self.proxy.agents, agent.Agent,
                         paginated=False)

    def test_agent_update(self):
        self.verify_update(self.proxy.update_agent, agent.Agent)

    def test_availability_zones(self):
        self.verify_list_no_kwargs(self.proxy.availability_zones,
                                   availability_zone.AvailabilityZone,
                                   paginated=False)

    def test_dhcp_agent_hosting_networks(self):
        self.verify_list(
            self.proxy.dhcp_agent_hosting_networks,
            network.DHCPAgentHostingNetwork,
            paginated=False,
            method_kwargs={'agent': AGENT_ID},
            expected_kwargs={'agent_id': AGENT_ID}
        )

    def test_network_hosting_dhcp_agents(self):
        self.verify_list(
            self.proxy.network_hosting_dhcp_agents,
            agent.NetworkHostingDHCPAgent,
            paginated=False,
            method_kwargs={'network': NETWORK_ID},
            expected_kwargs={'network_id': NETWORK_ID}
        )

    def test_extension_find(self):
        self.verify_find(self.proxy.find_extension, extension.Extension)

    def test_extensions(self):
        self.verify_list(self.proxy.extensions, extension.Extension,
                         paginated=False)

    def test_floating_ip_create_attrs(self):
        self.verify_create(self.proxy.create_ip, floating_ip.FloatingIP)

    def test_floating_ip_delete(self):
        self.verify_delete(self.proxy.delete_ip, floating_ip.FloatingIP,
                           False)

    def test_floating_ip_delete_ignore(self):
        self.verify_delete(self.proxy.delete_ip, floating_ip.FloatingIP,
                           True)

    def test_floating_ip_find(self):
        self.verify_find(self.proxy.find_ip, floating_ip.FloatingIP)

    def test_floating_ip_get(self):
        self.verify_get(self.proxy.get_ip, floating_ip.FloatingIP)

    def test_ips(self):
        self.verify_list(self.proxy.ips, floating_ip.FloatingIP,
                         paginated=False)

    def test_floating_ip_update(self):
        self.verify_update(self.proxy.update_ip, floating_ip.FloatingIP)

    def test_health_monitor_create_attrs(self):
        self.verify_create(self.proxy.create_health_monitor,
                           health_monitor.HealthMonitor)

    def test_health_monitor_delete(self):
        self.verify_delete(self.proxy.delete_health_monitor,
                           health_monitor.HealthMonitor, False)

    def test_health_monitor_delete_ignore(self):
        self.verify_delete(self.proxy.delete_health_monitor,
                           health_monitor.HealthMonitor, True)

    def test_health_monitor_find(self):
        self.verify_find(self.proxy.find_health_monitor,
                         health_monitor.HealthMonitor)

    def test_health_monitor_get(self):
        self.verify_get(self.proxy.get_health_monitor,
                        health_monitor.HealthMonitor)

    def test_health_monitors(self):
        self.verify_list(self.proxy.health_monitors,
                         health_monitor.HealthMonitor,
                         paginated=False)

    def test_health_monitor_update(self):
        self.verify_update(self.proxy.update_health_monitor,
                           health_monitor.HealthMonitor)

    def test_listener_create_attrs(self):
        self.verify_create(self.proxy.create_listener, listener.Listener)

    def test_listener_delete(self):
        self.verify_delete(self.proxy.delete_listener,
                           listener.Listener, False)

    def test_listener_delete_ignore(self):
        self.verify_delete(self.proxy.delete_listener,
                           listener.Listener, True)

    def test_listener_find(self):
        self.verify_find(self.proxy.find_listener, listener.Listener)

    def test_listener_get(self):
        self.verify_get(self.proxy.get_listener, listener.Listener)

    def test_listeners(self):
        self.verify_list(self.proxy.listeners, listener.Listener,
                         paginated=False)

    def test_listener_update(self):
        self.verify_update(self.proxy.update_listener, listener.Listener)

    def test_load_balancer_create_attrs(self):
        self.verify_create(self.proxy.create_load_balancer,
                           load_balancer.LoadBalancer)

    def test_load_balancer_delete(self):
        self.verify_delete(self.proxy.delete_load_balancer,
                           load_balancer.LoadBalancer, False)

    def test_load_balancer_delete_ignore(self):
        self.verify_delete(self.proxy.delete_load_balancer,
                           load_balancer.LoadBalancer, True)

    def test_load_balancer_find(self):
        self.verify_find(self.proxy.find_load_balancer,
                         load_balancer.LoadBalancer)

    def test_load_balancer_get(self):
        self.verify_get(self.proxy.get_load_balancer,
                        load_balancer.LoadBalancer)

    def test_load_balancers(self):
        self.verify_list(self.proxy.load_balancers,
                         load_balancer.LoadBalancer,
                         paginated=False)

    def test_load_balancer_update(self):
        self.verify_update(self.proxy.update_load_balancer,
                           load_balancer.LoadBalancer)

    def test_metering_label_create_attrs(self):
        self.verify_create(self.proxy.create_metering_label,
                           metering_label.MeteringLabel)

    def test_metering_label_delete(self):
        self.verify_delete(self.proxy.delete_metering_label,
                           metering_label.MeteringLabel, False)

    def test_metering_label_delete_ignore(self):
        self.verify_delete(self.proxy.delete_metering_label,
                           metering_label.MeteringLabel, True)

    def test_metering_label_find(self):
        self.verify_find(self.proxy.find_metering_label,
                         metering_label.MeteringLabel)

    def test_metering_label_get(self):
        self.verify_get(self.proxy.get_metering_label,
                        metering_label.MeteringLabel)

    def test_metering_labels(self):
        self.verify_list(self.proxy.metering_labels,
                         metering_label.MeteringLabel,
                         paginated=False)

    def test_metering_label_update(self):
        self.verify_update(self.proxy.update_metering_label,
                           metering_label.MeteringLabel)

    def test_metering_label_rule_create_attrs(self):
        self.verify_create(self.proxy.create_metering_label_rule,
                           metering_label_rule.MeteringLabelRule)

    def test_metering_label_rule_delete(self):
        self.verify_delete(self.proxy.delete_metering_label_rule,
                           metering_label_rule.MeteringLabelRule, False)

    def test_metering_label_rule_delete_ignore(self):
        self.verify_delete(self.proxy.delete_metering_label_rule,
                           metering_label_rule.MeteringLabelRule, True)

    def test_metering_label_rule_find(self):
        self.verify_find(self.proxy.find_metering_label_rule,
                         metering_label_rule.MeteringLabelRule)

    def test_metering_label_rule_get(self):
        self.verify_get(self.proxy.get_metering_label_rule,
                        metering_label_rule.MeteringLabelRule)

    def test_metering_label_rules(self):
        self.verify_list(self.proxy.metering_label_rules,
                         metering_label_rule.MeteringLabelRule,
                         paginated=False)

    def test_metering_label_rule_update(self):
        self.verify_update(self.proxy.update_metering_label_rule,
                           metering_label_rule.MeteringLabelRule)

    def test_network_create_attrs(self):
        self.verify_create(self.proxy.create_network, network.Network)

    def test_network_delete(self):
        self.verify_delete(self.proxy.delete_network, network.Network, False)

    def test_network_delete_ignore(self):
        self.verify_delete(self.proxy.delete_network, network.Network, True)

    def test_network_find(self):
        self.verify_find(self.proxy.find_network, network.Network)

    def test_network_get(self):
        self.verify_get(self.proxy.get_network, network.Network)

    def test_networks(self):
        self.verify_list(self.proxy.networks, network.Network,
                         paginated=False)

    def test_network_update(self):
        self.verify_update(self.proxy.update_network, network.Network)

    def test_flavor_create_attrs(self):
        self.verify_create(self.proxy.create_flavor, flavor.Flavor)

    def test_flavor_delete(self):
        self.verify_delete(self.proxy.delete_flavor, flavor.Flavor, True)

    def test_flavor_find(self):
        self.verify_find(self.proxy.find_flavor, flavor.Flavor)

    def test_flavor_get(self):
        self.verify_get(self.proxy.get_flavor, flavor.Flavor)

    def test_flavor_update(self):
        self.verify_update(self.proxy.update_flavor, flavor.Flavor)

    def test_flavors(self):
        self.verify_list(self.proxy.flavors, flavor.Flavor,
                         paginated=True)

    def test_service_profile_create_attrs(self):
        self.verify_create(self.proxy.create_service_profile,
                           service_profile.ServiceProfile)

    def test_service_profile_delete(self):
        self.verify_delete(self.proxy.delete_service_profile,
                           service_profile.ServiceProfile, True)

    def test_service_profile_find(self):
        self.verify_find(self.proxy.find_service_profile,
                         service_profile.ServiceProfile)

    def test_service_profile_get(self):
        self.verify_get(self.proxy.get_service_profile,
                        service_profile.ServiceProfile)

    def test_service_profiles(self):
        self.verify_list(self.proxy.service_profiles,
                         service_profile.ServiceProfile, paginated=True)

    def test_service_profile_update(self):
        self.verify_update(self.proxy.update_service_profile,
                           service_profile.ServiceProfile)

    def test_network_ip_availability_find(self):
        self.verify_find(self.proxy.find_network_ip_availability,
                         network_ip_availability.NetworkIPAvailability)

    def test_network_ip_availability_get(self):
        self.verify_get(self.proxy.get_network_ip_availability,
                        network_ip_availability.NetworkIPAvailability)

    def test_network_ip_availabilities(self):
        self.verify_list(self.proxy.network_ip_availabilities,
                         network_ip_availability.NetworkIPAvailability)

    def test_pool_member_create_attrs(self):
        self.verify_create(self.proxy.create_pool_member,
                           pool_member.PoolMember,
                           method_kwargs={"pool": "test_id"},
                           expected_kwargs={"pool_id": "test_id"})

    def test_pool_member_delete(self):
        self.verify_delete(self.proxy.delete_pool_member,
                           pool_member.PoolMember, False,
                           {"pool": "test_id"}, {"pool_id": "test_id"})

    def test_pool_member_delete_ignore(self):
        self.verify_delete(self.proxy.delete_pool_member,
                           pool_member.PoolMember, True,
                           {"pool": "test_id"}, {"pool_id": "test_id"})

    def test_pool_member_find(self):
        self._verify2('openstack.proxy2.BaseProxy._find',
                      self.proxy.find_pool_member,
                      method_args=["MEMBER", "POOL"],
                      expected_args=[pool_member.PoolMember, "MEMBER"],
                      expected_kwargs={"pool_id": "POOL",
                                       "ignore_missing": True})

    def test_pool_member_get(self):
        self._verify2('openstack.proxy2.BaseProxy._get',
                      self.proxy.get_pool_member,
                      method_args=["MEMBER", "POOL"],
                      expected_args=[pool_member.PoolMember, "MEMBER"],
                      expected_kwargs={"pool_id": "POOL"})

    def test_pool_members(self):
        self.verify_list(self.proxy.pool_members, pool_member.PoolMember,
                         paginated=False, method_args=["test_id"],
                         expected_kwargs={"pool_id": "test_id"})

    def test_pool_member_update(self):
        self._verify2("openstack.proxy2.BaseProxy._update",
                      self.proxy.update_pool_member,
                      method_args=["MEMBER", "POOL"],
                      expected_args=[pool_member.PoolMember, "MEMBER"],
                      expected_kwargs={"pool_id": "POOL"})

    def test_pool_create_attrs(self):
        self.verify_create(self.proxy.create_pool, pool.Pool)

    def test_pool_delete(self):
        self.verify_delete(self.proxy.delete_pool, pool.Pool, False)

    def test_pool_delete_ignore(self):
        self.verify_delete(self.proxy.delete_pool, pool.Pool, True)

    def test_pool_find(self):
        self.verify_find(self.proxy.find_pool, pool.Pool)

    def test_pool_get(self):
        self.verify_get(self.proxy.get_pool, pool.Pool)

    def test_pools(self):
        self.verify_list(self.proxy.pools, pool.Pool, paginated=False)

    def test_pool_update(self):
        self.verify_update(self.proxy.update_pool, pool.Pool)

    def test_port_create_attrs(self):
        self.verify_create(self.proxy.create_port, port.Port)

    def test_port_delete(self):
        self.verify_delete(self.proxy.delete_port, port.Port, False)

    def test_port_delete_ignore(self):
        self.verify_delete(self.proxy.delete_port, port.Port, True)

    def test_port_find(self):
        self.verify_find(self.proxy.find_port, port.Port)

    def test_port_get(self):
        self.verify_get(self.proxy.get_port, port.Port)

    def test_ports(self):
        self.verify_list(self.proxy.ports, port.Port, paginated=False)

    def test_port_update(self):
        self.verify_update(self.proxy.update_port, port.Port)

    def test_qos_bandwidth_limit_rule_create_attrs(self):
        self.verify_create(
            self.proxy.create_qos_bandwidth_limit_rule,
            qos_bandwidth_limit_rule.QoSBandwidthLimitRule,
            method_kwargs={'qos_policy': QOS_POLICY_ID},
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_bandwidth_limit_rule_delete(self):
        self.verify_delete(
            self.proxy.delete_qos_bandwidth_limit_rule,
            qos_bandwidth_limit_rule.QoSBandwidthLimitRule,
            False, input_path_args=["resource_or_id", QOS_POLICY_ID],
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_bandwidth_limit_rule_delete_ignore(self):
        self.verify_delete(
            self.proxy.delete_qos_bandwidth_limit_rule,
            qos_bandwidth_limit_rule.QoSBandwidthLimitRule,
            True, input_path_args=["resource_or_id", QOS_POLICY_ID],
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_bandwidth_limit_rule_find(self):
        policy = qos_policy.QoSPolicy.new(id=QOS_POLICY_ID)
        self._verify2('openstack.proxy2.BaseProxy._find',
                      self.proxy.find_qos_bandwidth_limit_rule,
                      method_args=['rule_id', policy],
                      expected_args=[
                          qos_bandwidth_limit_rule.QoSBandwidthLimitRule,
                          'rule_id'],
                      expected_kwargs={'ignore_missing': True,
                                       'qos_policy_id': QOS_POLICY_ID})

    def test_qos_bandwidth_limit_rule_get(self):
        self.verify_get(
            self.proxy.get_qos_bandwidth_limit_rule,
            qos_bandwidth_limit_rule.QoSBandwidthLimitRule,
            method_kwargs={'qos_policy': QOS_POLICY_ID},
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_bandwidth_limit_rules(self):
        self.verify_list(
            self.proxy.qos_bandwidth_limit_rules,
            qos_bandwidth_limit_rule.QoSBandwidthLimitRule,
            paginated=False,
            method_kwargs={'qos_policy': QOS_POLICY_ID},
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_bandwidth_limit_rule_update(self):
        policy = qos_policy.QoSPolicy.new(id=QOS_POLICY_ID)
        self._verify2('openstack.proxy2.BaseProxy._update',
                      self.proxy.update_qos_bandwidth_limit_rule,
                      method_args=['rule_id', policy],
                      method_kwargs={'foo': 'bar'},
                      expected_args=[
                          qos_bandwidth_limit_rule.QoSBandwidthLimitRule,
                          'rule_id'],
                      expected_kwargs={'qos_policy_id': QOS_POLICY_ID,
                                       'foo': 'bar'})

    def test_qos_dscp_marking_rule_create_attrs(self):
        self.verify_create(
            self.proxy.create_qos_dscp_marking_rule,
            qos_dscp_marking_rule.QoSDSCPMarkingRule,
            method_kwargs={'qos_policy': QOS_POLICY_ID},
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_dscp_marking_rule_delete(self):
        self.verify_delete(
            self.proxy.delete_qos_dscp_marking_rule,
            qos_dscp_marking_rule.QoSDSCPMarkingRule,
            False, input_path_args=["resource_or_id", QOS_POLICY_ID],
            expected_path_args={'qos_policy_id': QOS_POLICY_ID},)

    def test_qos_dscp_marking_rule_delete_ignore(self):
        self.verify_delete(
            self.proxy.delete_qos_dscp_marking_rule,
            qos_dscp_marking_rule.QoSDSCPMarkingRule,
            True, input_path_args=["resource_or_id", QOS_POLICY_ID],
            expected_path_args={'qos_policy_id': QOS_POLICY_ID}, )

    def test_qos_dscp_marking_rule_find(self):
        policy = qos_policy.QoSPolicy.new(id=QOS_POLICY_ID)
        self._verify2('openstack.proxy2.BaseProxy._find',
                      self.proxy.find_qos_dscp_marking_rule,
                      method_args=['rule_id', policy],
                      expected_args=[qos_dscp_marking_rule.QoSDSCPMarkingRule,
                                     'rule_id'],
                      expected_kwargs={'ignore_missing': True,
                                       'qos_policy_id': QOS_POLICY_ID})

    def test_qos_dscp_marking_rule_get(self):
        self.verify_get(
            self.proxy.get_qos_dscp_marking_rule,
            qos_dscp_marking_rule.QoSDSCPMarkingRule,
            method_kwargs={'qos_policy': QOS_POLICY_ID},
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_dscp_marking_rules(self):
        self.verify_list(
            self.proxy.qos_dscp_marking_rules,
            qos_dscp_marking_rule.QoSDSCPMarkingRule,
            paginated=False,
            method_kwargs={'qos_policy': QOS_POLICY_ID},
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_dscp_marking_rule_update(self):
        policy = qos_policy.QoSPolicy.new(id=QOS_POLICY_ID)
        self._verify2('openstack.proxy2.BaseProxy._update',
                      self.proxy.update_qos_dscp_marking_rule,
                      method_args=['rule_id', policy],
                      method_kwargs={'foo': 'bar'},
                      expected_args=[
                          qos_dscp_marking_rule.QoSDSCPMarkingRule,
                          'rule_id'],
                      expected_kwargs={'qos_policy_id': QOS_POLICY_ID,
                                       'foo': 'bar'})

    def test_qos_minimum_bandwidth_rule_create_attrs(self):
        self.verify_create(
            self.proxy.create_qos_minimum_bandwidth_rule,
            qos_minimum_bandwidth_rule.QoSMinimumBandwidthRule,
            method_kwargs={'qos_policy': QOS_POLICY_ID},
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_minimum_bandwidth_rule_delete(self):
        self.verify_delete(
            self.proxy.delete_qos_minimum_bandwidth_rule,
            qos_minimum_bandwidth_rule.QoSMinimumBandwidthRule,
            False, input_path_args=["resource_or_id", QOS_POLICY_ID],
            expected_path_args={'qos_policy_id': QOS_POLICY_ID},)

    def test_qos_minimum_bandwidth_rule_delete_ignore(self):
        self.verify_delete(
            self.proxy.delete_qos_minimum_bandwidth_rule,
            qos_minimum_bandwidth_rule.QoSMinimumBandwidthRule,
            True, input_path_args=["resource_or_id", QOS_POLICY_ID],
            expected_path_args={'qos_policy_id': QOS_POLICY_ID}, )

    def test_qos_minimum_bandwidth_rule_find(self):
        policy = qos_policy.QoSPolicy.new(id=QOS_POLICY_ID)
        self._verify2('openstack.proxy2.BaseProxy._find',
                      self.proxy.find_qos_minimum_bandwidth_rule,
                      method_args=['rule_id', policy],
                      expected_args=[
                          qos_minimum_bandwidth_rule.QoSMinimumBandwidthRule,
                          'rule_id'],
                      expected_kwargs={'ignore_missing': True,
                                       'qos_policy_id': QOS_POLICY_ID})

    def test_qos_minimum_bandwidth_rule_get(self):
        self.verify_get(
            self.proxy.get_qos_minimum_bandwidth_rule,
            qos_minimum_bandwidth_rule.QoSMinimumBandwidthRule,
            method_kwargs={'qos_policy': QOS_POLICY_ID},
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_minimum_bandwidth_rules(self):
        self.verify_list(
            self.proxy.qos_minimum_bandwidth_rules,
            qos_minimum_bandwidth_rule.QoSMinimumBandwidthRule,
            paginated=False,
            method_kwargs={'qos_policy': QOS_POLICY_ID},
            expected_kwargs={'qos_policy_id': QOS_POLICY_ID})

    def test_qos_minimum_bandwidth_rule_update(self):
        policy = qos_policy.QoSPolicy.new(id=QOS_POLICY_ID)
        self._verify2('openstack.proxy2.BaseProxy._update',
                      self.proxy.update_qos_minimum_bandwidth_rule,
                      method_args=['rule_id', policy],
                      method_kwargs={'foo': 'bar'},
                      expected_args=[
                          qos_minimum_bandwidth_rule.QoSMinimumBandwidthRule,
                          'rule_id'],
                      expected_kwargs={'qos_policy_id': QOS_POLICY_ID,
                                       'foo': 'bar'})

    def test_qos_policy_create_attrs(self):
        self.verify_create(self.proxy.create_qos_policy, qos_policy.QoSPolicy)

    def test_qos_policy_delete(self):
        self.verify_delete(self.proxy.delete_qos_policy, qos_policy.QoSPolicy,
                           False)

    def test_qos_policy_delete_ignore(self):
        self.verify_delete(self.proxy.delete_qos_policy, qos_policy.QoSPolicy,
                           True)

    def test_qos_policy_find(self):
        self.verify_find(self.proxy.find_qos_policy, qos_policy.QoSPolicy)

    def test_qos_policy_get(self):
        self.verify_get(self.proxy.get_qos_policy, qos_policy.QoSPolicy)

    def test_qos_policies(self):
        self.verify_list(self.proxy.qos_policies, qos_policy.QoSPolicy,
                         paginated=False)

    def test_qos_policy_update(self):
        self.verify_update(self.proxy.update_qos_policy, qos_policy.QoSPolicy)

    def test_qos_rule_types(self):
        self.verify_list(self.proxy.qos_rule_types, qos_rule_type.QoSRuleType,
                         paginated=False)

    def test_quota_delete(self):
        self.verify_delete(self.proxy.delete_quota, quota.Quota, False)

    def test_quota_delete_ignore(self):
        self.verify_delete(self.proxy.delete_quota, quota.Quota, True)

    def test_quota_get(self):
        self.verify_get(self.proxy.get_quota, quota.Quota)

    @mock.patch.object(proxy_base2.BaseProxy, "_get_resource")
    def test_quota_default_get(self, mock_get):
        fake_quota = mock.Mock(project_id='PROJECT')
        mock_get.return_value = fake_quota
        self._verify2("openstack.proxy2.BaseProxy._get",
                      self.proxy.get_quota_default,
                      method_args=['QUOTA_ID'],
                      expected_args=[quota.QuotaDefault],
                      expected_kwargs={'project': fake_quota.id,
                                       'requires_id': False})
        mock_get.assert_called_once_with(quota.Quota, 'QUOTA_ID')

    def test_quotas(self):
        self.verify_list(self.proxy.quotas, quota.Quota, paginated=False)

    def test_quota_update(self):
        self.verify_update(self.proxy.update_quota, quota.Quota)

    def test_rbac_policy_create_attrs(self):
        self.verify_create(self.proxy.create_rbac_policy,
                           rbac_policy.RBACPolicy)

    def test_rbac_policy_delete(self):
        self.verify_delete(self.proxy.delete_rbac_policy,
                           rbac_policy.RBACPolicy, False)

    def test_rbac_policy_delete_ignore(self):
        self.verify_delete(self.proxy.delete_rbac_policy,
                           rbac_policy.RBACPolicy, True)

    def test_rbac_policy_find(self):
        self.verify_find(self.proxy.find_rbac_policy, rbac_policy.RBACPolicy)

    def test_rbac_policy_get(self):
        self.verify_get(self.proxy.get_rbac_policy, rbac_policy.RBACPolicy)

    def test_rbac_policies(self):
        self.verify_list(self.proxy.rbac_policies,
                         rbac_policy.RBACPolicy, paginated=False)

    def test_rbac_policy_update(self):
        self.verify_update(self.proxy.update_rbac_policy,
                           rbac_policy.RBACPolicy)

    def test_router_create_attrs(self):
        self.verify_create(self.proxy.create_router, router.Router)

    def test_router_delete(self):
        self.verify_delete(self.proxy.delete_router, router.Router, False)

    def test_router_delete_ignore(self):
        self.verify_delete(self.proxy.delete_router, router.Router, True)

    def test_router_find(self):
        self.verify_find(self.proxy.find_router, router.Router)

    def test_router_get(self):
        self.verify_get(self.proxy.get_router, router.Router)

    def test_routers(self):
        self.verify_list(self.proxy.routers, router.Router, paginated=False)

    def test_router_update(self):
        self.verify_update(self.proxy.update_router, router.Router)

    @mock.patch.object(proxy_base2.BaseProxy, '_get_resource')
    @mock.patch.object(router.Router, 'add_interface')
    def test_add_interface_to_router_with_port(self, mock_add_interface,
                                               mock_get):
        x_router = router.Router.new(id="ROUTER_ID")
        mock_get.return_value = x_router

        self._verify("openstack.network.v2.router.Router.add_interface",
                     self.proxy.add_interface_to_router,
                     method_args=["FAKE_ROUTER"],
                     method_kwargs={"port_id": "PORT"},
                     expected_kwargs={"port_id": "PORT"})
        mock_get.assert_called_once_with(router.Router, "FAKE_ROUTER")

    @mock.patch.object(proxy_base2.BaseProxy, '_get_resource')
    @mock.patch.object(router.Router, 'add_interface')
    def test_add_interface_to_router_with_subnet(self, mock_add_interface,
                                                 mock_get):
        x_router = router.Router.new(id="ROUTER_ID")
        mock_get.return_value = x_router

        self._verify("openstack.network.v2.router.Router.add_interface",
                     self.proxy.add_interface_to_router,
                     method_args=["FAKE_ROUTER"],
                     method_kwargs={"subnet_id": "SUBNET"},
                     expected_kwargs={"subnet_id": "SUBNET"})
        mock_get.assert_called_once_with(router.Router, "FAKE_ROUTER")

    @mock.patch.object(proxy_base2.BaseProxy, '_get_resource')
    @mock.patch.object(router.Router, 'remove_interface')
    def test_remove_interface_from_router_with_port(self, mock_remove,
                                                    mock_get):
        x_router = router.Router.new(id="ROUTER_ID")
        mock_get.return_value = x_router

        self._verify("openstack.network.v2.router.Router.remove_interface",
                     self.proxy.remove_interface_from_router,
                     method_args=["FAKE_ROUTER"],
                     method_kwargs={"port_id": "PORT"},
                     expected_kwargs={"port_id": "PORT"})
        mock_get.assert_called_once_with(router.Router, "FAKE_ROUTER")

    @mock.patch.object(proxy_base2.BaseProxy, '_get_resource')
    @mock.patch.object(router.Router, 'remove_interface')
    def test_remove_interface_from_router_with_subnet(self, mock_remove,
                                                      mock_get):
        x_router = router.Router.new(id="ROUTER_ID")
        mock_get.return_value = x_router

        self._verify("openstack.network.v2.router.Router.remove_interface",
                     self.proxy.remove_interface_from_router,
                     method_args=["FAKE_ROUTER"],
                     method_kwargs={"subnet_id": "SUBNET"},
                     expected_kwargs={"subnet_id": "SUBNET"})
        mock_get.assert_called_once_with(router.Router, "FAKE_ROUTER")

    @mock.patch.object(proxy_base2.BaseProxy, '_get_resource')
    @mock.patch.object(router.Router, 'add_gateway')
    def test_add_gateway_to_router(self, mock_add, mock_get):
        x_router = router.Router.new(id="ROUTER_ID")
        mock_get.return_value = x_router

        self._verify("openstack.network.v2.router.Router.add_gateway",
                     self.proxy.add_gateway_to_router,
                     method_args=["FAKE_ROUTER"],
                     method_kwargs={"foo": "bar"},
                     expected_kwargs={"foo": "bar"})
        mock_get.assert_called_once_with(router.Router, "FAKE_ROUTER")

    @mock.patch.object(proxy_base2.BaseProxy, '_get_resource')
    @mock.patch.object(router.Router, 'remove_gateway')
    def test_remove_gateway_from_router(self, mock_remove, mock_get):
        x_router = router.Router.new(id="ROUTER_ID")
        mock_get.return_value = x_router

        self._verify("openstack.network.v2.router.Router.remove_gateway",
                     self.proxy.remove_gateway_from_router,
                     method_args=["FAKE_ROUTER"],
                     method_kwargs={"foo": "bar"},
                     expected_kwargs={"foo": "bar"})
        mock_get.assert_called_once_with(router.Router, "FAKE_ROUTER")

    def test_router_hosting_l3_agents_list(self):
        self.verify_list(
            self.proxy.routers_hosting_l3_agents,
            agent.RouterL3Agent,
            paginated=False,
            method_kwargs={'router': ROUTER_ID},
            expected_kwargs={'router_id': ROUTER_ID},
        )

    def test_agent_hosted_routers_list(self):
        self.verify_list(
            self.proxy.agent_hosted_routers,
            router.L3AgentRouter,
            paginated=False,
            method_kwargs={'agent': AGENT_ID},
            expected_kwargs={'agent_id': AGENT_ID},
        )

    def test_security_group_create_attrs(self):
        self.verify_create(self.proxy.create_security_group,
                           security_group.SecurityGroup)

    def test_security_group_delete(self):
        self.verify_delete(self.proxy.delete_security_group,
                           security_group.SecurityGroup, False)

    def test_security_group_delete_ignore(self):
        self.verify_delete(self.proxy.delete_security_group,
                           security_group.SecurityGroup, True)

    def test_security_group_find(self):
        self.verify_find(self.proxy.find_security_group,
                         security_group.SecurityGroup)

    def test_security_group_get(self):
        self.verify_get(self.proxy.get_security_group,
                        security_group.SecurityGroup)

    def test_security_groups(self):
        self.verify_list(self.proxy.security_groups,
                         security_group.SecurityGroup,
                         paginated=False)

    def test_security_group_update(self):
        self.verify_update(self.proxy.update_security_group,
                           security_group.SecurityGroup)

    @deprecation.fail_if_not_removed
    def test_security_group_open_port(self):
        mock_class = 'openstack.network.v2._proxy.Proxy'
        mock_method = mock_class + '.create_security_group_rule'
        expected_result = 'result'
        sgid = 1
        port = 2
        with mock.patch(mock_method) as mocked:
            mocked.return_value = expected_result
            actual = self.proxy.security_group_open_port(sgid, port)
            self.assertEqual(expected_result, actual)
            expected_args = {
                'direction': 'ingress',
                'protocol': 'tcp',
                'remote_ip_prefix': '0.0.0.0/0',
                'port_range_max': port,
                'security_group_id': sgid,
                'port_range_min': port,
                'ethertype': 'IPv4',
            }
            mocked.assert_called_with(**expected_args)

    @deprecation.fail_if_not_removed
    def test_security_group_allow_ping(self):
        mock_class = 'openstack.network.v2._proxy.Proxy'
        mock_method = mock_class + '.create_security_group_rule'
        expected_result = 'result'
        sgid = 1
        with mock.patch(mock_method) as mocked:
            mocked.return_value = expected_result
            actual = self.proxy.security_group_allow_ping(sgid)
            self.assertEqual(expected_result, actual)
            expected_args = {
                'direction': 'ingress',
                'protocol': 'icmp',
                'remote_ip_prefix': '0.0.0.0/0',
                'port_range_max': None,
                'security_group_id': sgid,
                'port_range_min': None,
                'ethertype': 'IPv4',
            }
            mocked.assert_called_with(**expected_args)

    def test_security_group_rule_create_attrs(self):
        self.verify_create(self.proxy.create_security_group_rule,
                           security_group_rule.SecurityGroupRule)

    def test_security_group_rule_delete(self):
        self.verify_delete(self.proxy.delete_security_group_rule,
                           security_group_rule.SecurityGroupRule, False)

    def test_security_group_rule_delete_ignore(self):
        self.verify_delete(self.proxy.delete_security_group_rule,
                           security_group_rule.SecurityGroupRule, True)

    def test_security_group_rule_find(self):
        self.verify_find(self.proxy.find_security_group_rule,
                         security_group_rule.SecurityGroupRule)

    def test_security_group_rule_get(self):
        self.verify_get(self.proxy.get_security_group_rule,
                        security_group_rule.SecurityGroupRule)

    def test_security_group_rules(self):
        self.verify_list(self.proxy.security_group_rules,
                         security_group_rule.SecurityGroupRule,
                         paginated=False)

    def test_segment_create_attrs(self):
        self.verify_create(self.proxy.create_segment, segment.Segment)

    def test_segment_delete(self):
        self.verify_delete(self.proxy.delete_segment, segment.Segment, False)

    def test_segment_delete_ignore(self):
        self.verify_delete(self.proxy.delete_segment, segment.Segment, True)

    def test_segment_find(self):
        self.verify_find(self.proxy.find_segment, segment.Segment)

    def test_segment_get(self):
        self.verify_get(self.proxy.get_segment, segment.Segment)

    def test_segments(self):
        self.verify_list(self.proxy.segments, segment.Segment, paginated=False)

    def test_segment_update(self):
        self.verify_update(self.proxy.update_segment, segment.Segment)

    def test_subnet_create_attrs(self):
        self.verify_create(self.proxy.create_subnet, subnet.Subnet)

    def test_subnet_delete(self):
        self.verify_delete(self.proxy.delete_subnet, subnet.Subnet, False)

    def test_subnet_delete_ignore(self):
        self.verify_delete(self.proxy.delete_subnet, subnet.Subnet, True)

    def test_subnet_find(self):
        self.verify_find(self.proxy.find_subnet, subnet.Subnet)

    def test_subnet_get(self):
        self.verify_get(self.proxy.get_subnet, subnet.Subnet)

    def test_subnets(self):
        self.verify_list(self.proxy.subnets, subnet.Subnet, paginated=False)

    def test_subnet_update(self):
        self.verify_update(self.proxy.update_subnet, subnet.Subnet)

    def test_subnet_pool_create_attrs(self):
        self.verify_create(self.proxy.create_subnet_pool,
                           subnet_pool.SubnetPool)

    def test_subnet_pool_delete(self):
        self.verify_delete(self.proxy.delete_subnet_pool,
                           subnet_pool.SubnetPool, False)

    def test_subnet_pool_delete_ignore(self):
        self.verify_delete(self.proxy.delete_subnet_pool,
                           subnet_pool.SubnetPool, True)

    def test_subnet_pool_find(self):
        self.verify_find(self.proxy.find_subnet_pool,
                         subnet_pool.SubnetPool)

    def test_subnet_pool_get(self):
        self.verify_get(self.proxy.get_subnet_pool,
                        subnet_pool.SubnetPool)

    def test_subnet_pools(self):
        self.verify_list(self.proxy.subnet_pools,
                         subnet_pool.SubnetPool,
                         paginated=False)

    def test_subnet_pool_update(self):
        self.verify_update(self.proxy.update_subnet_pool,
                           subnet_pool.SubnetPool)

    def test_vpn_service_create_attrs(self):
        self.verify_create(self.proxy.create_vpn_service,
                           vpn_service.VPNService)

    def test_vpn_service_delete(self):
        self.verify_delete(self.proxy.delete_vpn_service,
                           vpn_service.VPNService, False)

    def test_vpn_service_delete_ignore(self):
        self.verify_delete(self.proxy.delete_vpn_service,
                           vpn_service.VPNService, True)

    def test_vpn_service_find(self):
        self.verify_find(self.proxy.find_vpn_service,
                         vpn_service.VPNService)

    def test_vpn_service_get(self):
        self.verify_get(self.proxy.get_vpn_service, vpn_service.VPNService)

    def test_vpn_services(self):
        self.verify_list(self.proxy.vpn_services, vpn_service.VPNService,
                         paginated=False)

    def test_vpn_service_update(self):
        self.verify_update(self.proxy.update_vpn_service,
                           vpn_service.VPNService)

    def test_service_provider(self):
        self.verify_list(self.proxy.service_providers,
                         service_provider.ServiceProvider,
                         paginated=False)

    def test_auto_allocated_topology_get(self):
        self.verify_get(self.proxy.get_auto_allocated_topology,
                        auto_allocated_topology.AutoAllocatedTopology)

    def test_auto_allocated_topology_delete(self):
        self.verify_delete(self.proxy.delete_auto_allocated_topology,
                           auto_allocated_topology.AutoAllocatedTopology,
                           False)

    def test_auto_allocated_topology_delete_ignore(self):
        self.verify_delete(self.proxy.delete_auto_allocated_topology,
                           auto_allocated_topology.AutoAllocatedTopology,
                           True)

    def test_validate_topology(self):
        self.verify_get(self.proxy.validate_auto_allocated_topology,
                        auto_allocated_topology.ValidateTopology,
                        value=[mock.sentinel.project_id],
                        expected_args=[
                            auto_allocated_topology.ValidateTopology],
                        expected_kwargs={"project": mock.sentinel.project_id,
                                         "requires_id": False})
