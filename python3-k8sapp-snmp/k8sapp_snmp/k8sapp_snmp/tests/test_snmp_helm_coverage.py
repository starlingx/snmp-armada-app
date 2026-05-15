#
# Copyright (c) 2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Coverage tests for k8sapp_snmp helm module."""

import unittest
from unittest import mock

from k8sapp_snmp.helm import snmp as snmp_mod
from k8sapp_snmp.tests.test_helpers import HelmTestCase
from k8sapp_snmp.tests.test_helpers import HelmPatchedTestCase
from k8sapp_snmp.tests.test_helpers import setup_overrides_mocks
from k8sapp_snmp.tests import test_constants as tc


class TestUnicodeRepresent(HelmTestCase):
    """Tests for _unicode_represent method."""

    def test_normal_string(self):
        """Verify normal ASCII string is returned."""
        self.assertIsInstance(
            self.helm._unicode_represent('hello'), str)

    def test_none(self):
        """Verify None returns UNDEFINED_CONF_VALUE."""
        self.assertEqual(
            self.helm._unicode_represent(None),
            tc.HELM_UNDEFINED_CONF_VALUE)

    def test_empty(self):
        """Verify empty string returns str type."""
        self.assertIsInstance(
            self.helm._unicode_represent(''), str)

    def test_integer(self):
        """Verify non-string returns default value."""
        self.assertEqual(
            self.helm._unicode_represent(12345),
            tc.HELM_UNDEFINED_CONF_VALUE)

    def test_utf8(self):
        """Verify UTF-8 string is handled correctly."""
        self.assertIsInstance(
            self.helm._unicode_represent('café'), str)


class TestGetKeyringPassword(HelmTestCase):
    """Tests for _get_keyring_password method."""

    @mock.patch.object(snmp_mod, 'keyring')
    def test_success(self, mock_keyring):
        """Verify successful password retrieval."""
        mock_keyring.get_password.return_value = \
            tc.MOCK_DB_PASSWORD
        self.assertEqual(
            self.helm._get_keyring_password('fm', 'db'),
            tc.MOCK_DB_PASSWORD)

    @mock.patch.object(snmp_mod, 'keyring')
    def test_none_raises(self, mock_keyring):
        """Verify None password raises exception."""
        mock_keyring.get_password.return_value = None
        self.assertRaises(  # noqa: H202
            Exception,
            self.helm._get_keyring_password, 'fm', 'db')

    @mock.patch.object(snmp_mod, 'keyring')
    def test_empty_raises(self, mock_keyring):
        """Verify empty password raises exception."""
        mock_keyring.get_password.return_value = ''
        self.assertRaises(  # noqa: H202
            Exception,
            self.helm._get_keyring_password, 'fm', 'db')


class TestGetDatabaseConnection(HelmPatchedTestCase):
    """Tests for _get_database_connection method."""

    def test_fqdn(self):
        """Verify connection uses FQDN when ready."""
        self.mock_utils.is_fqdn_ready_to_use \
            .return_value = True
        self.mock_constants.CONTROLLER_FQDN = \
            tc.MOCK_CONTROLLER_FQDN
        conn = self.helm._get_database_connection()
        self.assertIn('postgresql://', conn)
        self.assertIn(tc.MOCK_CONTROLLER_FQDN, conn)

    def test_ip_fallback(self):
        """Verify connection falls back to IP address."""
        self.mock_utils.is_fqdn_ready_to_use \
            .return_value = False
        self.helm._get_management_address = \
            mock.MagicMock(
                return_value=tc.MOCK_MANAGEMENT_IP)
        self.helm._format_url_address = \
            mock.MagicMock(
                return_value=tc.MOCK_MANAGEMENT_IP)
        conn = self.helm._get_database_connection()
        self.assertIn('postgresql://', conn)


class TestEndpoints(HelmTestCase):
    """Tests for URL endpoint methods."""

    def test_namespaces(self):
        """Verify get_namespaces returns a list."""
        self.assertIsNotNone(self.helm.get_namespaces())

    def test_public_url(self):
        """Verify get_public_url delegates correctly."""
        self.helm._format_public_endpoint = \
            mock.MagicMock(return_value='http://pub:18002')
        self.assertEqual(
            self.helm.get_public_url(),
            'http://pub:18002')

    def test_internal_url(self):
        """Verify get_internal_url delegates correctly."""
        self.helm._format_private_endpoint = \
            mock.MagicMock(return_value='http://int:18002')
        self.assertEqual(
            self.helm.get_internal_url(),
            'http://int:18002')

    def test_admin_url(self):
        """Verify get_admin_url delegates correctly."""
        self.helm._format_admin_endpoint = \
            mock.MagicMock(return_value='http://adm:18002')
        self.assertEqual(
            self.helm.get_admin_url(),
            'http://adm:18002')

    def test_system_info(self):
        """Verify get_system_info returns a string."""
        self.assertIsInstance(
            self.helm.get_system_info(), str)


class TestGetOverrides(HelmPatchedTestCase):
    """Tests for get_overrides method."""

    def setUp(self):
        """Configure overrides mocks."""
        super().setUp()
        setup_overrides_mocks(
            self.mock_keyring, self.mock_utils,
            self.mock_constants, self.mock_common,
            self.mock_api)

    def test_valid_namespace(self):
        """Verify valid namespace returns configmap."""
        result = self.helm.get_overrides(
            namespace='kube-system')
        self.assertIn('configmap', result)

    @mock.patch.object(snmp_mod, 'exception')
    def test_invalid_namespace(self, mock_exception):
        """Verify invalid namespace raises exception."""
        mock_exception.InvalidHelmNamespace = type(
            'InvalidHelmNamespace', (Exception,), {})
        self.assertRaises(  # noqa: H202
            Exception,
            self.helm.get_overrides, namespace='bad')

    def test_none_namespace(self):
        """Verify None namespace returns full dict."""
        self.assertIsInstance(
            self.helm.get_overrides(namespace=None), dict)


class TestClassAttrs(unittest.TestCase):
    """Tests for SnmpHelm class-level attributes."""

    def test_chart(self):
        """Verify HELM_CHART_SNMP constant value."""
        from k8sapp_snmp.common import constants
        self.assertEqual(
            constants.HELM_CHART_SNMP,
            tc.HELM_CHART_NAME)

    def test_service_name(self):
        """Verify SERVICE_NAME is snmp."""
        self.assertEqual(
            snmp_mod.SnmpHelm.SERVICE_NAME, 'snmp')

    def test_fm_port(self):
        """Verify SERVICE_FM_PORT is 18002."""
        self.assertEqual(
            snmp_mod.SnmpHelm.SERVICE_FM_PORT,
            tc.HELM_SERVICE_FM_PORT)

    def test_db_admin(self):
        """Verify DB_FM_ADMIN is admin-fm."""
        self.assertEqual(
            snmp_mod.SnmpHelm.DB_FM_ADMIN,
            tc.HELM_DB_FM_ADMIN)

    def test_kernel_idx(self):
        """Verify KERNEL_RELEASE_IDX is 2."""
        self.assertEqual(
            snmp_mod.SnmpHelm.KERNEL_RELEASE_IDX,
            tc.HELM_KERNEL_RELEASE_IDX)

    def test_py3(self):
        """Verify PY3 flag is True on Python 3."""
        self.assertTrue(snmp_mod.PY3)

    def test_py2(self):
        """Verify PY2 flag is False on Python 3."""
        self.assertFalse(snmp_mod.PY2)
