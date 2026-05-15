#
# Copyright (c) 2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Shared test helpers for k8sapp_snmp tests."""

import os
import unittest
from unittest import mock

from k8sapp_snmp.helm import snmp as snmp_mod
from k8sapp_snmp.lifecycle import lifecycle_snmp
from k8sapp_snmp.tests import test_constants as tc

SnmpAppLifecycleOperator = \
    lifecycle_snmp.SnmpAppLifecycleOperator


def create_helm_instance():
    """Create a SnmpHelm instance with test defaults."""
    helm_obj = object.__new__(snmp_mod.SnmpHelm)
    for attr, val in (
        ('UNDEFINED_CONF_VALUE', tc.HELM_UNDEFINED_CONF_VALUE),
        ('SERVICE_FM_NAME', tc.HELM_SERVICE_FM_NAME),
        ('DB_FM_ADMIN', tc.HELM_DB_FM_ADMIN),
        ('SERVICE_FM_PORT', tc.HELM_SERVICE_FM_PORT),
        ('KERNEL_RELEASE_IDX', tc.HELM_KERNEL_RELEASE_IDX),
        ('CHART', tc.HELM_CHART_NAME),
        ('SUPPORTED_NAMESPACES', tc.HELM_SUPPORTED_NAMESPACES),
    ):
        setattr(helm_obj, attr, val)
    return helm_obj


def create_mock_system():
    """Create a mock system object with test defaults."""
    return mock.MagicMock(
        contact=tc.MOCK_SYSTEM_CONTACT,
        location=tc.MOCK_SYSTEM_LOCATION,
        name=tc.MOCK_SYSTEM_NAME,
        software_version=tc.MOCK_SYSTEM_SOFTWARE_VERSION)


def setup_overrides_mocks(
        mock_keyring, mock_utils, mock_constants,
        mock_common, mock_api):
    """Configure mocks for get_overrides tests."""
    mock_keyring.get_password.return_value = \
        tc.MOCK_DB_PASSWORD
    mock_utils.is_fqdn_ready_to_use.return_value = True
    mock_constants.CONTROLLER_FQDN = \
        tc.MOCK_CONTROLLER_FQDN
    mock_common.HELM_NS_KUBE_SYSTEM = 'kube-system'
    mock_api.get_instance.return_value \
        .isystem_get_one.return_value = \
        create_mock_system()


def project_path(*parts):
    """Build an absolute path relative to project root."""
    return os.path.join(tc.PROJECT_ROOT, *parts)


class BaseLifecycleTestCase(unittest.TestCase):
    """Base class for lifecycle operator tests."""

    def setUp(self):
        """Set up operator and mock conductor."""
        self.operator = SnmpAppLifecycleOperator()
        self.context = mock.MagicMock()
        self.conductor = mock.MagicMock()
        self.conductor._config_update_hosts \
            .return_value = 'config-uuid'

    def _invoke_lifecycle(self, lifecycle_type,
                          operation, timing):
        """Invoke app_lifecycle_actions with params."""
        hook_info = mock.MagicMock()
        hook_info.lifecycle_type = lifecycle_type
        hook_info.operation = operation
        hook_info.relative_timing = timing
        self.operator.app_lifecycle_actions(
            self.context, self.conductor,
            mock.MagicMock(), mock.MagicMock(),
            hook_info)


class HelmTestCase(unittest.TestCase):
    """Base class for helm module tests."""

    def setUp(self):
        """Create helm instance for tests."""
        self.helm = create_helm_instance()


class HelmPatchedTestCase(HelmTestCase):
    """Base for helm tests needing patched dependencies."""

    def setUp(self):
        """Patch common dependencies for overrides tests."""
        super().setUp()
        for attr in ('keyring', 'utils', 'constants',
                     'common', 'api'):
            setattr(self, 'mock_' + attr,
                    mock.patch.object(
                        snmp_mod, attr).start())
        self.addCleanup(mock.patch.stopall)
        self.mock_keyring.get_password.return_value = \
            tc.MOCK_DB_PASSWORD
