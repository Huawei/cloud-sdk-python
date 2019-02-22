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

from openstack.cluster.v1 import _proxy
from openstack.cluster.v1 import action
from openstack.cluster.v1 import build_info
from openstack.cluster.v1 import cluster
from openstack.cluster.v1 import cluster_attr
from openstack.cluster.v1 import cluster_policy
from openstack.cluster.v1 import event
from openstack.cluster.v1 import node
from openstack.cluster.v1 import policy
from openstack.cluster.v1 import policy_type
from openstack.cluster.v1 import profile
from openstack.cluster.v1 import profile_type
from openstack.cluster.v1 import receiver
from openstack import proxy2 as proxy_base
from openstack.tests.unit import test_proxy_base2


class TestClusterProxy(test_proxy_base2.TestProxyBase):
    def setUp(self):
        super(TestClusterProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_build_info_get(self):
        self.verify_get(self.proxy.get_build_info, build_info.BuildInfo,
                        ignore_value=True,
                        expected_kwargs={'requires_id': False})

    def test_profile_types(self):
        self.verify_list(self.proxy.profile_types,
                         profile_type.ProfileType,
                         paginated=False)

    def test_profile_type_get(self):
        self.verify_get(self.proxy.get_profile_type,
                        profile_type.ProfileType)

    def test_policy_types(self):
        self.verify_list(self.proxy.policy_types, policy_type.PolicyType,
                         paginated=False)

    def test_policy_type_get(self):
        self.verify_get(self.proxy.get_policy_type, policy_type.PolicyType)

    def test_profile_create(self):
        self.verify_create(self.proxy.create_profile, profile.Profile)

    def test_profile_validate(self):
        self.verify_create(self.proxy.validate_profile,
                           profile.ProfileValidate)

    def test_profile_delete(self):
        self.verify_delete(self.proxy.delete_profile, profile.Profile, False)

    def test_profile_delete_ignore(self):
        self.verify_delete(self.proxy.delete_profile, profile.Profile, True)

    def test_profile_find(self):
        self.verify_find(self.proxy.find_profile, profile.Profile)

    def test_profile_get(self):
        self.verify_get(self.proxy.get_profile, profile.Profile)

    def test_profiles(self):
        self.verify_list(self.proxy.profiles, profile.Profile,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_profile_update(self):
        self.verify_update(self.proxy.update_profile, profile.Profile)

    def test_cluster_create(self):
        self.verify_create(self.proxy.create_cluster, cluster.Cluster)

    def test_cluster_delete(self):
        self.verify_delete(self.proxy.delete_cluster, cluster.Cluster, False)

    def test_cluster_delete_ignore(self):
        self.verify_delete(self.proxy.delete_cluster, cluster.Cluster, True)

    def test_cluster_find(self):
        self.verify_find(self.proxy.find_cluster, cluster.Cluster)

    def test_cluster_get(self):
        self.verify_get(self.proxy.get_cluster, cluster.Cluster)

    def test_clusters(self):
        self.verify_list(self.proxy.clusters, cluster.Cluster,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_cluster_update(self):
        self.verify_update(self.proxy.update_cluster, cluster.Cluster)

    @deprecation.fail_if_not_removed
    @mock.patch.object(proxy_base.BaseProxy, '_find')
    def test_cluster_add_nodes(self, mock_find):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_find.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.add_nodes",
                     self.proxy.cluster_add_nodes,
                     method_args=["FAKE_CLUSTER", ["node1"]],
                     expected_args=[["node1"]])
        mock_find.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER",
                                          ignore_missing=False)

    @deprecation.fail_if_not_removed
    def test_cluster_add_nodes_with_obj(self):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        self._verify("openstack.cluster.v1.cluster.Cluster.add_nodes",
                     self.proxy.cluster_add_nodes,
                     method_args=[mock_cluster, ["node1"]],
                     expected_args=[["node1"]])

    @deprecation.fail_if_not_removed
    @mock.patch.object(proxy_base.BaseProxy, '_find')
    def test_cluster_del_nodes(self, mock_find):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_find.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.del_nodes",
                     self.proxy.cluster_del_nodes,
                     method_args=["FAKE_CLUSTER", ["node1"]],
                     expected_args=[["node1"]])
        mock_find.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER",
                                          ignore_missing=False)

    @deprecation.fail_if_not_removed
    def test_cluster_del_nodes_with_obj(self):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        self._verify("openstack.cluster.v1.cluster.Cluster.del_nodes",
                     self.proxy.cluster_del_nodes,
                     method_args=[mock_cluster, ["node1"]],
                     method_kwargs={"key": "value"},
                     expected_args=[["node1"]],
                     expected_kwargs={"key": "value"})

    @deprecation.fail_if_not_removed
    @mock.patch.object(proxy_base.BaseProxy, '_find')
    def test_cluster_replace_nodes(self, mock_find):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_find.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.replace_nodes",
                     self.proxy.cluster_replace_nodes,
                     method_args=["FAKE_CLUSTER", {"node1": "node2"}],
                     expected_args=[{"node1": "node2"}])
        mock_find.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER",
                                          ignore_missing=False)

    @deprecation.fail_if_not_removed
    def test_cluster_replace_nodes_with_obj(self):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        self._verify("openstack.cluster.v1.cluster.Cluster.replace_nodes",
                     self.proxy.cluster_replace_nodes,
                     method_args=[mock_cluster, {"node1": "node2"}],
                     expected_args=[{"node1": "node2"}])

    @deprecation.fail_if_not_removed
    @mock.patch.object(proxy_base.BaseProxy, '_find')
    def test_cluster_scale_out(self, mock_find):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_find.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.scale_out",
                     self.proxy.cluster_scale_out,
                     method_args=["FAKE_CLUSTER", 3],
                     expected_args=[3])
        mock_find.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER",
                                          ignore_missing=False)

    @deprecation.fail_if_not_removed
    def test_cluster_scale_out_with_obj(self):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        self._verify("openstack.cluster.v1.cluster.Cluster.scale_out",
                     self.proxy.cluster_scale_out,
                     method_args=[mock_cluster, 5],
                     expected_args=[5])

    @deprecation.fail_if_not_removed
    @mock.patch.object(proxy_base.BaseProxy, '_find')
    def test_cluster_scale_in(self, mock_find):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_find.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.scale_in",
                     self.proxy.cluster_scale_in,
                     method_args=["FAKE_CLUSTER", 3],
                     expected_args=[3])
        mock_find.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER",
                                          ignore_missing=False)

    @deprecation.fail_if_not_removed
    def test_cluster_scale_in_with_obj(self):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        self._verify("openstack.cluster.v1.cluster.Cluster.scale_in",
                     self.proxy.cluster_scale_in,
                     method_args=[mock_cluster, 5],
                     expected_args=[5])

    @mock.patch.object(proxy_base.BaseProxy, '_find')
    def test_cluster_resize(self, mock_find):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_find.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.resize",
                     self.proxy.cluster_resize,
                     method_args=["FAKE_CLUSTER"],
                     method_kwargs={'k1': 'v1', 'k2': 'v2'},
                     expected_kwargs={'k1': 'v1', 'k2': 'v2'})
        mock_find.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER",
                                          ignore_missing=False)

    def test_cluster_resize_with_obj(self):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        self._verify("openstack.cluster.v1.cluster.Cluster.resize",
                     self.proxy.cluster_resize,
                     method_args=[mock_cluster],
                     method_kwargs={'k1': 'v1', 'k2': 'v2'},
                     expected_kwargs={'k1': 'v1', 'k2': 'v2'})

    @deprecation.fail_if_not_removed
    @mock.patch.object(proxy_base.BaseProxy, '_find')
    def test_cluster_attach_policy(self, mock_find):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_find.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.policy_attach",
                     self.proxy.cluster_attach_policy,
                     method_args=["FAKE_CLUSTER", "FAKE_POLICY"],
                     method_kwargs={"k1": "v1", "k2": "v2"},
                     expected_args=["FAKE_POLICY"],
                     expected_kwargs={"k1": "v1", 'k2': "v2"})
        mock_find.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER",
                                          ignore_missing=False)

    @deprecation.fail_if_not_removed
    def test_cluster_attach_policy_with_obj(self):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        self._verify("openstack.cluster.v1.cluster.Cluster.policy_attach",
                     self.proxy.cluster_attach_policy,
                     method_args=[mock_cluster, "FAKE_POLICY"],
                     method_kwargs={"k1": "v1", "k2": "v2"},
                     expected_args=["FAKE_POLICY"],
                     expected_kwargs={"k1": "v1", 'k2': "v2"})

    @deprecation.fail_if_not_removed
    @mock.patch.object(proxy_base.BaseProxy, '_find')
    def test_cluster_detach_policy(self, mock_find):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_find.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.policy_detach",
                     self.proxy.cluster_detach_policy,
                     method_args=["FAKE_CLUSTER", "FAKE_POLICY"],
                     expected_args=["FAKE_POLICY"])
        mock_find.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER",
                                          ignore_missing=False)

    @deprecation.fail_if_not_removed
    def test_cluster_detach_policy_with_obj(self):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        self._verify("openstack.cluster.v1.cluster.Cluster.policy_detach",
                     self.proxy.cluster_detach_policy,
                     method_args=[mock_cluster, "FAKE_POLICY"],
                     expected_args=["FAKE_POLICY"])

    @deprecation.fail_if_not_removed
    @mock.patch.object(proxy_base.BaseProxy, '_find')
    def test_cluster_update_policy(self, mock_find):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_find.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.policy_update",
                     self.proxy.cluster_update_policy,
                     method_args=["FAKE_CLUSTER", "FAKE_POLICY"],
                     method_kwargs={"k1": "v1", "k2": "v2"},
                     expected_args=["FAKE_POLICY"],
                     expected_kwargs={"k1": "v1", 'k2': "v2"})
        mock_find.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER",
                                          ignore_missing=False)

    @deprecation.fail_if_not_removed
    def test_cluster_update_policy_with_obj(self):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        self._verify("openstack.cluster.v1.cluster.Cluster.policy_update",
                     self.proxy.cluster_update_policy,
                     method_args=[mock_cluster, "FAKE_POLICY"],
                     method_kwargs={"k1": "v1", "k2": "v2"},
                     expected_args=["FAKE_POLICY"],
                     expected_kwargs={"k1": "v1", 'k2': "v2"})

    def test_collect_cluster_attrs(self):
        self.verify_list(self.proxy.collect_cluster_attrs,
                         cluster_attr.ClusterAttr, paginated=False,
                         method_args=['FAKE_ID', 'path.to.attr'],
                         expected_kwargs={'cluster_id': 'FAKE_ID',
                                          'path': 'path.to.attr'})

    @mock.patch.object(proxy_base.BaseProxy, '_get_resource')
    def test_cluster_check(self, mock_get):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_get.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.check",
                     self.proxy.check_cluster,
                     method_args=["FAKE_CLUSTER"])
        mock_get.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER")

    @mock.patch.object(proxy_base.BaseProxy, '_get_resource')
    def test_cluster_recover(self, mock_get):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_get.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.recover",
                     self.proxy.recover_cluster,
                     method_args=["FAKE_CLUSTER"])
        mock_get.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER")

    @deprecation.fail_if_not_removed
    @mock.patch.object(proxy_base.BaseProxy, '_get_resource')
    def test_cluster_operation(self, mock_get):
        mock_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')
        mock_get.return_value = mock_cluster
        self._verify("openstack.cluster.v1.cluster.Cluster.op",
                     self.proxy.cluster_operation,
                     method_args=["FAKE_CLUSTER", "dance"],
                     expected_args=["dance"])
        mock_get.assert_called_once_with(cluster.Cluster, "FAKE_CLUSTER")

    def test_node_create(self):
        self.verify_create(self.proxy.create_node, node.Node)

    def test_node_delete(self):
        self.verify_delete(self.proxy.delete_node, node.Node, False)

    def test_node_delete_ignore(self):
        self.verify_delete(self.proxy.delete_node, node.Node, True)

    def test_node_find(self):
        self.verify_find(self.proxy.find_node, node.Node)

    def test_node_get(self):
        self.verify_get(self.proxy.get_node, node.Node)

    def test_node_get_with_details(self):
        self._verify2('openstack.proxy2.BaseProxy._get',
                      self.proxy.get_node,
                      method_args=['NODE_ID'],
                      method_kwargs={'details': True},
                      expected_args=[node.NodeDetail],
                      expected_kwargs={'node_id': 'NODE_ID',
                                       'requires_id': False})

    def test_nodes(self):
        self.verify_list(self.proxy.nodes, node.Node,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_node_update(self):
        self.verify_update(self.proxy.update_node, node.Node)

    @mock.patch.object(proxy_base.BaseProxy, '_get_resource')
    def test_node_check(self, mock_get):
        mock_node = node.Node.new(id='FAKE_NODE')
        mock_get.return_value = mock_node
        self._verify("openstack.cluster.v1.node.Node.check",
                     self.proxy.check_node,
                     method_args=["FAKE_NODE"])
        mock_get.assert_called_once_with(node.Node, "FAKE_NODE")

    @mock.patch.object(proxy_base.BaseProxy, '_get_resource')
    def test_node_recover(self, mock_get):
        mock_node = node.Node.new(id='FAKE_NODE')
        mock_get.return_value = mock_node
        self._verify("openstack.cluster.v1.node.Node.recover",
                     self.proxy.recover_node,
                     method_args=["FAKE_NODE"])
        mock_get.assert_called_once_with(node.Node, "FAKE_NODE")

    @deprecation.fail_if_not_removed
    @mock.patch.object(proxy_base.BaseProxy, '_get_resource')
    def test_node_operation(self, mock_get):
        mock_node = node.Node.new(id='FAKE_CLUSTER')
        mock_get.return_value = mock_node
        self._verify("openstack.cluster.v1.node.Node.op",
                     self.proxy.node_operation,
                     method_args=["FAKE_NODE", "dance"],
                     expected_args=["dance"])
        mock_get.assert_called_once_with(node.Node, "FAKE_NODE")

    def test_policy_create(self):
        self.verify_create(self.proxy.create_policy, policy.Policy)

    def test_policy_validate(self):
        self.verify_create(self.proxy.validate_policy, policy.PolicyValidate)

    def test_policy_delete(self):
        self.verify_delete(self.proxy.delete_policy, policy.Policy, False)

    def test_policy_delete_ignore(self):
        self.verify_delete(self.proxy.delete_policy, policy.Policy, True)

    def test_policy_find(self):
        self.verify_find(self.proxy.find_policy, policy.Policy)

    def test_policy_get(self):
        self.verify_get(self.proxy.get_policy, policy.Policy)

    def test_policies(self):
        self.verify_list(self.proxy.policies, policy.Policy,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_policy_update(self):
        self.verify_update(self.proxy.update_policy, policy.Policy)

    def test_cluster_policies(self):
        self.verify_list(self.proxy.cluster_policies,
                         cluster_policy.ClusterPolicy,
                         paginated=False, method_args=["FAKE_CLUSTER"],
                         expected_kwargs={"cluster_id": "FAKE_CLUSTER"})

    def test_get_cluster_policy(self):
        fake_policy = cluster_policy.ClusterPolicy.new(id="FAKE_POLICY")
        fake_cluster = cluster.Cluster.new(id='FAKE_CLUSTER')

        # ClusterPolicy object as input
        self._verify2('openstack.proxy2.BaseProxy._get',
                      self.proxy.get_cluster_policy,
                      method_args=[fake_policy, "FAKE_CLUSTER"],
                      expected_args=[cluster_policy.ClusterPolicy,
                                     fake_policy],
                      expected_kwargs={'cluster_id': 'FAKE_CLUSTER'},
                      expected_result=fake_policy)

        # Policy ID as input
        self._verify2('openstack.proxy2.BaseProxy._get',
                      self.proxy.get_cluster_policy,
                      method_args=["FAKE_POLICY", "FAKE_CLUSTER"],
                      expected_args=[cluster_policy.ClusterPolicy,
                                     "FAKE_POLICY"],
                      expected_kwargs={"cluster_id": "FAKE_CLUSTER"})

        # Cluster object as input
        self._verify2('openstack.proxy2.BaseProxy._get',
                      self.proxy.get_cluster_policy,
                      method_args=["FAKE_POLICY", fake_cluster],
                      expected_args=[cluster_policy.ClusterPolicy,
                                     "FAKE_POLICY"],
                      expected_kwargs={"cluster_id": fake_cluster})

    def test_receiver_create(self):
        self.verify_create(self.proxy.create_receiver, receiver.Receiver)

    def test_receiver_delete(self):
        self.verify_delete(self.proxy.delete_receiver, receiver.Receiver,
                           False)

    def test_receiver_delete_ignore(self):
        self.verify_delete(self.proxy.delete_receiver, receiver.Receiver, True)

    def test_receiver_find(self):
        self.verify_find(self.proxy.find_receiver, receiver.Receiver)

    def test_receiver_get(self):
        self.verify_get(self.proxy.get_receiver, receiver.Receiver)

    def test_receivers(self):
        self.verify_list(self.proxy.receivers, receiver.Receiver,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_action_get(self):
        self.verify_get(self.proxy.get_action, action.Action)

    def test_actions(self):
        self.verify_list(self.proxy.actions, action.Action,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    def test_event_get(self):
        self.verify_get(self.proxy.get_event, event.Event)

    def test_events(self):
        self.verify_list(self.proxy.events, event.Event,
                         paginated=True,
                         method_kwargs={'limit': 2},
                         expected_kwargs={'limit': 2})

    @mock.patch("openstack.resource2.wait_for_status")
    def test_wait_for(self, mock_wait):
        mock_resource = mock.Mock()
        mock_wait.return_value = mock_resource

        self.proxy.wait_for_status(mock_resource, 'ACTIVE')

        mock_wait.assert_called_once_with(self.session, mock_resource,
                                          'ACTIVE', [], 2, 120)

    @mock.patch("openstack.resource2.wait_for_status")
    def test_wait_for_params(self, mock_wait):
        mock_resource = mock.Mock()
        mock_wait.return_value = mock_resource

        self.proxy.wait_for_status(mock_resource, 'ACTIVE', ['ERROR'], 1, 2)

        mock_wait.assert_called_once_with(self.session, mock_resource,
                                          'ACTIVE', ['ERROR'], 1, 2)

    @mock.patch("openstack.resource2.wait_for_delete")
    def test_wait_for_delete(self, mock_wait):
        mock_resource = mock.Mock()
        mock_wait.return_value = mock_resource

        self.proxy.wait_for_delete(mock_resource)

        mock_wait.assert_called_once_with(self.session, mock_resource, 2, 120)

    @mock.patch("openstack.resource2.wait_for_delete")
    def test_wait_for_delete_params(self, mock_wait):
        mock_resource = mock.Mock()
        mock_wait.return_value = mock_resource

        self.proxy.wait_for_delete(mock_resource, 1, 2)

        mock_wait.assert_called_once_with(self.session, mock_resource, 1, 2)
