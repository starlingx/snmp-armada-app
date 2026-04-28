#
# Copyright (c) 2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Shared test constants for k8sapp_snmp tests."""

import os

# Project root directory
PROJECT_ROOT = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..', '..'))

# Helm test defaults
HELM_UNDEFINED_CONF_VALUE = '?'
HELM_SERVICE_FM_NAME = 'fm'
HELM_DB_FM_ADMIN = 'admin-fm'
HELM_SERVICE_FM_PORT = 18002
HELM_KERNEL_RELEASE_IDX = 2
HELM_CHART_NAME = 'snmp'
HELM_SUPPORTED_NAMESPACES = ['kube-system']

# Mock system object defaults
MOCK_SYSTEM_CONTACT = 'admin'
MOCK_SYSTEM_LOCATION = 'lab'
MOCK_SYSTEM_NAME = 'test-system'
MOCK_SYSTEM_SOFTWARE_VERSION = '1.0'
MOCK_DB_PASSWORD = 'test_password'
MOCK_CONTROLLER_FQDN = 'controller.fqdn'
MOCK_MANAGEMENT_IP = '10.0.0.1'

# Lifecycle constants
LIFECYCLE_TYPE_OPERATION = 'operation'
LIFECYCLE_TYPE_RESOURCE = 'resource'
LIFECYCLE_TIMING_POST = 'post'
LIFECYCLE_TIMING_PRE = 'pre'
LIFECYCLE_OP_APPLY = 'apply'
LIFECYCLE_OP_REMOVE = 'remove'
LIFECYCLE_CONTROLLER = 'controller'
