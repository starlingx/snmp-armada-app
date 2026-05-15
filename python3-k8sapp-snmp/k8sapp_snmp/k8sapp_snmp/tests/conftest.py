#
# Copyright (c) 2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Centralized mock setup for k8sapp_snmp tests.

This conftest runs before any test module is imported
by pytest, ensuring all heavy dependencies are mocked
consistently.
"""

import sys
from unittest import mock


def _needs_mocking():
    """Check if real dependencies are available.

    Returns:
        bool: True if mocking is needed, False otherwise.
    """
    try:
        import keyring  # noqa: F401
        import oslo_log  # noqa: F401
        from sysinv.helm.base import BaseHelm
        # keyring and oslo_log are imported only to check
        # availability; suppress unused-import warnings
        del keyring, oslo_log
        if isinstance(BaseHelm, mock.MagicMock):
            return True
        return False
    except Exception:  # noqa: H202
        return True


NEED_MOCK = _needs_mocking()

if NEED_MOCK:
    class FakeBaseHelm(object):
        """Fake BaseHelm for testing."""

        SUPPORTED_NAMESPACES = ['kube-system']

        def __init__(self, *args, **kwargs):
            """Initialize fake BaseHelm."""

    class FakeAppLifecycleOperator(object):
        """Fake AppLifecycleOperator for testing."""

        def app_lifecycle_actions(self, *args, **kwargs):
            """Perform lifecycle actions (no-op stub)."""

    # Build sysinv mock hierarchy
    mock_sysinv = mock.MagicMock()
    mock_helm = mock.MagicMock()
    mock_helm_base = mock.MagicMock()
    mock_helm_base.BaseHelm = FakeBaseHelm
    mock_lifecycle_base = mock.MagicMock()
    mock_lifecycle_base.AppLifecycleOperator = \
        FakeAppLifecycleOperator
    mock_lifecycle_constants = mock.MagicMock()
    mock_lifecycle_constants \
        .LifecycleConstants \
        .APP_LIFECYCLE_TYPE_OPERATION = 'operation'
    mock_lifecycle_constants \
        .LifecycleConstants \
        .APP_LIFECYCLE_TYPE_RESOURCE = 'resource'
    mock_lifecycle_constants \
        .LifecycleConstants \
        .APP_LIFECYCLE_TIMING_POST = 'post'
    mock_lifecycle_constants \
        .LifecycleConstants \
        .APP_LIFECYCLE_TIMING_PRE = 'pre'
    mock_lifecycle_utils = mock.MagicMock()

    mock_sysinv.common.constants.APP_APPLY_OP = 'apply'
    mock_sysinv.common.constants.APP_REMOVE_OP = 'remove'
    mock_sysinv.common.constants.CONTROLLER = 'controller'
    mock_sysinv.helm = mock_helm
    mock_helm.base = mock_helm_base
    mock_helm.lifecycle_base = mock_lifecycle_base
    mock_helm.lifecycle_utils = mock_lifecycle_utils
    mock_helm.lifecycle_constants = mock_lifecycle_constants

    sys.modules['keyring'] = mock.MagicMock()
    sys.modules['oslo_log'] = mock.MagicMock()
    sys.modules['oslo_log.log'] = mock.MagicMock()
    sys.modules['sysinv'] = mock_sysinv
    sys.modules['sysinv.common'] = \
        mock_sysinv.common
    sys.modules['sysinv.common.constants'] = \
        mock_sysinv.common.constants
    sys.modules['sysinv.common.exception'] = \
        mock_sysinv.common.exception
    sys.modules['sysinv.common.utils'] = \
        mock_sysinv.common.utils
    sys.modules['sysinv.db'] = mock_sysinv.db
    sys.modules['sysinv.db.api'] = mock_sysinv.db.api
    sys.modules['sysinv.helm'] = mock_helm
    sys.modules['sysinv.helm.base'] = mock_helm_base
    sys.modules['sysinv.helm.common'] = mock_helm.common
    sys.modules['sysinv.helm.lifecycle_base'] = \
        mock_lifecycle_base
    sys.modules['sysinv.helm.lifecycle_utils'] = \
        mock_lifecycle_utils
    sys.modules['sysinv.helm.lifecycle_constants'] = \
        mock_lifecycle_constants

    # Mock sysinv.tests for existing test files
    mock_tests = mock.MagicMock()
    sys.modules['sysinv.tests'] = mock_tests
    sys.modules['sysinv.tests.db'] = mock_tests.db
    sys.modules['sysinv.tests.db.base'] = \
        mock_tests.db.base
    sys.modules['sysinv.tests.db.utils'] = \
        mock_tests.db.utils
    sys.modules['sysinv.tests.helm'] = mock_tests.helm
    sys.modules['sysinv.tests.helm.base'] = \
        mock_tests.helm.base
    sys.modules['sysinv.tests.base'] = mock_tests.base

    # Clear cached imports to pick up mocks
    for mod_name in list(sys.modules):
        if mod_name.startswith('k8sapp_snmp.helm') \
                or mod_name.startswith(
                    'k8sapp_snmp.lifecycle'):
            del sys.modules[mod_name]
