#
# Copyright (c) 2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Integration tests for snmp-armada-app project structure."""

import os
import unittest
import yaml

from k8sapp_snmp.tests.test_helpers import project_path

# Check for docker subdirectory specifically - the top-level
# stx-snmp-helm dir may exist in Zuul but docker/ content
# is not always present.
_STX_DOCKER_AVAILABLE = os.path.isfile(
    project_path('stx-snmp-helm', 'docker', 'stx-snmp',
                 'Dockerfile.debian'))

_PKG_BASE = ('python3-k8sapp-snmp', 'k8sapp_snmp',
             'k8sapp_snmp')


class _FileExistenceTestCase(unittest.TestCase):
    """Base class for file existence tests (DRY pattern).

    Subclasses define FILE_PATHS as a list of tuples
    passed to project_path().
    """

    FILE_PATHS = []

    def _check_files_exist(self):
        """Assert all FILE_PATHS exist."""
        for parts in self.FILE_PATHS:
            path = project_path(*parts)
            self.assertTrue(
                os.path.isfile(path),
                msg="%s not found" % path)


class TestProjectStructure(_FileExistenceTestCase):
    """Validate project file structure and config."""

    FILE_PATHS = [
        ('tox.ini',),
        ('python3-k8sapp-snmp', 'k8sapp_snmp', 'tox.ini'),
        ('.zuul.yaml',),
        ('python3-k8sapp-snmp', 'k8sapp_snmp', 'setup.cfg'),
        ('python3-k8sapp-snmp', 'k8sapp_snmp',
         'requirements.txt'),
        ('python3-k8sapp-snmp', 'k8sapp_snmp',
         'test-requirements.txt'),
    ]

    def test_expected_files_exist(self):
        """Test all expected project files exist."""
        self._check_files_exist()


class TestHelmChartStructure(unittest.TestCase):
    """Validate helm chart structure."""

    _CHART_BASE = ('helm-charts', 'custom', 'snmp-helm',
                   'snmp-helm', 'snmp')

    def test_chart_yaml_exists(self):
        """Test Chart.yaml exists."""
        path = project_path(*(self._CHART_BASE +
                              ('Chart.yaml',)))
        self.assertTrue(os.path.isfile(path))

    def test_values_yaml_exists(self):
        """Test values.yaml exists."""
        path = project_path(*(self._CHART_BASE +
                              ('values.yaml',)))
        self.assertTrue(os.path.isfile(path))

    def test_metadata_yaml_valid(self):
        """Test metadata.yaml is valid YAML."""
        path = project_path(
            'stx-snmp-helm', 'stx-snmp-helm',
            'files', 'metadata.yaml')
        self.assertTrue(
            os.path.isfile(path),
            "Required file not found: %s" % path)
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        self.assertIsNotNone(data)


class TestFluxCDManifests(unittest.TestCase):
    """Validate FluxCD manifest structure."""

    _FLUX_BASE = ('stx-snmp-helm', 'stx-snmp-helm',
                  'fluxcd-manifests')

    def test_kustomization_exists(self):
        """Test kustomization.yaml exists."""
        path = project_path(*(self._FLUX_BASE +
                              ('kustomization.yaml',)))
        self.assertTrue(os.path.isfile(path))

    def test_kustomization_valid_yaml(self):
        """Test kustomization.yaml is valid YAML."""
        path = project_path(*(self._FLUX_BASE +
                              ('kustomization.yaml',)))
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        self.assertIsNotNone(data)

    def test_helmrelease_exists(self):
        """Test helmrelease.yaml exists."""
        path = project_path(*(self._FLUX_BASE +
                              ('snmp', 'helmrelease.yaml')))
        self.assertTrue(os.path.isfile(path))


@unittest.skipUnless(
    _STX_DOCKER_AVAILABLE,
    'stx-snmp-helm/docker not available')
class TestDockerfileStructure(_FileExistenceTestCase):
    """Validate Dockerfile structure."""

    FILE_PATHS = [
        ('stx-snmp-helm', 'docker', d, 'Dockerfile.debian')
        for d in ('stx-fm-subagent',
                  'stx-fm-trap-subagent', 'stx-snmp')
    ]

    def test_all_dockerfiles_exist(self):
        """Test all Dockerfiles exist."""
        self._check_files_exist()


@unittest.skipUnless(
    _STX_DOCKER_AVAILABLE,
    'stx-snmp-helm/docker not available')
class TestCSourceFiles(_FileExistenceTestCase):
    """Validate C source files exist and are non-empty."""

    FILE_PATHS = [
        ('stx-snmp-helm', 'docker', 'stx-fm-subagent',
         'src', f) for f in (
            'snmpAgentPlugin.c', 'snmpActiveAlarms.c',
            'snmpEventLogs.c', 'snmpSubAgent.c')
    ] + [
        ('stx-snmp-helm', 'docker',
         'stx-fm-trap-subagent', 'src', f) for f in (
            'wrsAlarmMIBServer.c',
            'wrsAlarmMIBSubagent.c',
            'wrsAlarmMIBTrap.c')
    ] + [
        ('stx-snmp-helm', 'docker', 'stx-snmp',
         'src', 'snmpAuditPlugin.c'),
    ]

    def test_all_c_sources_exist(self):
        """Test all C source files exist and non-empty."""
        for parts in self.FILE_PATHS:
            full_path = project_path(*parts)
            self.assertTrue(
                os.path.isfile(full_path),
                msg="%s not found" % '/'.join(parts))
            self.assertGreater(
                os.path.getsize(full_path), 0)


@unittest.skipUnless(
    _STX_DOCKER_AVAILABLE,
    'stx-snmp-helm/docker not available')
class TestShellScripts(_FileExistenceTestCase):
    """Validate shell scripts."""

    FILE_PATHS = [
        ('stx-snmp-helm', 'docker', d, 'bootstrap.sh')
        for d in ('stx-fm-subagent',
                  'stx-fm-trap-subagent')
    ]

    def test_all_bootstrap_scripts_exist(self):
        """Test all bootstrap.sh scripts exist."""
        self._check_files_exist()


class TestPythonPackageStructure(_FileExistenceTestCase):
    """Validate Python package structure."""

    FILE_PATHS = [
        _PKG_BASE + sub for sub in (
            ('__init__.py',),
            ('helm', '__init__.py'),
            ('lifecycle', '__init__.py'),
            ('common', '__init__.py'),
            ('common', 'constants.py'),
            ('helm', 'snmp.py'),
            ('lifecycle', 'lifecycle_snmp.py'),
        )
    ]

    def test_all_package_files_exist(self):
        """Test all package files exist."""
        self._check_files_exist()
