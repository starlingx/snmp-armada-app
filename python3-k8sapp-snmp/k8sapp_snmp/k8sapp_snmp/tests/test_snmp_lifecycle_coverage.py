#
# Copyright (c) 2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Coverage tests for k8sapp_snmp lifecycle module."""

from unittest import mock

from k8sapp_snmp.lifecycle import lifecycle_snmp
from k8sapp_snmp.tests.test_helpers import BaseLifecycleTestCase
from k8sapp_snmp.tests import test_constants as tc


class TestPostApply(BaseLifecycleTestCase):
    """Tests for post-apply lifecycle action."""

    def test_via_lifecycle(self):
        """Verify post-apply triggers config update."""
        self._invoke_lifecycle(
            tc.LIFECYCLE_TYPE_OPERATION,
            tc.LIFECYCLE_OP_APPLY,
            tc.LIFECYCLE_TIMING_POST)
        self.conductor._config_update_hosts \
            .assert_called_once()
        self.conductor._config_apply_runtime_manifest \
            .assert_called_once()

    def test_direct(self):
        """Verify post_apply uses controller."""
        self.operator.post_apply(
            self.context, self.conductor,
            mock.MagicMock())
        call_args = self.conductor \
            ._config_update_hosts.call_args[0]
        self.assertIn(
            tc.LIFECYCLE_CONTROLLER, call_args[1])

    def test_manifest_called(self):
        """Verify runtime manifest is applied."""
        self.operator.post_apply(
            self.context, self.conductor,
            mock.MagicMock())
        self.conductor._config_apply_runtime_manifest \
            .assert_called_once()


class TestPostRemove(BaseLifecycleTestCase):
    """Tests for post-remove lifecycle action."""

    def test_via_lifecycle(self):
        """Verify post-remove triggers config update."""
        self._invoke_lifecycle(
            tc.LIFECYCLE_TYPE_OPERATION,
            tc.LIFECYCLE_OP_REMOVE,
            tc.LIFECYCLE_TIMING_POST)
        self.conductor._config_update_hosts \
            .assert_called_once()

    def test_direct(self):
        """Verify post_remove uses controller."""
        self.operator.post_remove(
            self.context, self.conductor,
            mock.MagicMock())
        call_args = self.conductor \
            ._config_update_hosts.call_args[0]
        self.assertIn(
            tc.LIFECYCLE_CONTROLLER, call_args[1])

    def test_manifest_called(self):
        """Verify runtime manifest is applied."""
        self.operator.post_remove(
            self.context, self.conductor,
            mock.MagicMock())
        self.conductor._config_apply_runtime_manifest \
            .assert_called_once()


class TestResourceOps(BaseLifecycleTestCase):
    """Tests for resource lifecycle operations."""

    @mock.patch(
        'k8sapp_snmp.lifecycle.lifecycle_snmp'
        '.lifecycle_utils')
    def test_pre_apply(self, mock_lifecycle_utils):
        """Verify pre-apply creates registry secrets."""
        self._invoke_lifecycle(
            tc.LIFECYCLE_TYPE_RESOURCE,
            tc.LIFECYCLE_OP_APPLY,
            tc.LIFECYCLE_TIMING_PRE)
        mock_lifecycle_utils \
            .create_local_registry_secrets \
            .assert_called_once()

    @mock.patch(
        'k8sapp_snmp.lifecycle.lifecycle_snmp'
        '.lifecycle_utils')
    def test_post_remove(self, mock_lifecycle_utils):
        """Verify post-remove deletes secrets."""
        self._invoke_lifecycle(
            tc.LIFECYCLE_TYPE_RESOURCE,
            tc.LIFECYCLE_OP_REMOVE,
            tc.LIFECYCLE_TIMING_POST)
        mock_lifecycle_utils \
            .delete_local_registry_secrets \
            .assert_called_once()


class TestDefaults(BaseLifecycleTestCase):
    """Tests for default/fallback lifecycle behavior."""

    def test_unknown_type(self):
        """Verify unknown type does not raise."""
        self._invoke_lifecycle(
            'unknown',
            tc.LIFECYCLE_OP_APPLY,
            tc.LIFECYCLE_TIMING_POST)

    def test_op_pre_apply(self):
        """Verify operation apply pre does not raise."""
        self._invoke_lifecycle(
            tc.LIFECYCLE_TYPE_OPERATION,
            tc.LIFECYCLE_OP_APPLY,
            tc.LIFECYCLE_TIMING_PRE)

    def test_op_unknown(self):
        """Verify unknown operation does not raise."""
        self._invoke_lifecycle(
            tc.LIFECYCLE_TYPE_OPERATION,
            'unknown',
            tc.LIFECYCLE_TIMING_POST)

    def test_res_apply_post(self):
        """Verify resource apply post does not raise."""
        self._invoke_lifecycle(
            tc.LIFECYCLE_TYPE_RESOURCE,
            tc.LIFECYCLE_OP_APPLY,
            tc.LIFECYCLE_TIMING_POST)

    def test_res_remove_pre(self):
        """Verify resource remove pre does not raise."""
        self._invoke_lifecycle(
            tc.LIFECYCLE_TYPE_RESOURCE,
            tc.LIFECYCLE_OP_REMOVE,
            tc.LIFECYCLE_TIMING_PRE)


class TestInit(BaseLifecycleTestCase):
    """Tests for operator initialization."""

    def test_instantiation(self):
        """Verify operator can be instantiated."""
        self.assertIsNotNone(
            lifecycle_snmp.SnmpAppLifecycleOperator())

    def test_has_lifecycle(self):
        """Verify has app_lifecycle_actions method."""
        self.assertTrue(
            hasattr(self.operator,
                    'app_lifecycle_actions'))

    def test_has_post_apply(self):
        """Verify has post_apply method."""
        self.assertTrue(
            hasattr(self.operator, 'post_apply'))

    def test_has_post_remove(self):
        """Verify has post_remove method."""
        self.assertTrue(
            hasattr(self.operator, 'post_remove'))

    def test_import(self):
        """Verify lifecycle package is importable."""
        import k8sapp_snmp.lifecycle  # noqa: F401,E501
        assert k8sapp_snmp.lifecycle is not None
