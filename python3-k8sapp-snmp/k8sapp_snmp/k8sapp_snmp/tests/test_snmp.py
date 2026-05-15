#
# Copyright (c) 2023, 2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
from k8sapp_snmp.tests import test_plugins

from sysinv.db import api as dbapi
from sysinv.tests.db import base as dbbase
from sysinv.tests.db import utils as dbutils
from sysinv.tests.helm import base


class SnmpTestCase(test_plugins.K8SAppSnmpAppMixin,
                          base.HelmTestCaseMixin):

    def setUp(self):
        """Set up SNMP test case with test app."""
        super(SnmpTestCase, self).setUp()
        self.app = dbutils.create_test_app(name='snmp')
        self.dbapi = dbapi.get_instance()


class SnmpTestCaseDummy(
        SnmpTestCase,
        dbbase.ProvisionedControllerHostTestCase):
    def test_dummy(self):
        """Placeholder test to prevent empty suite."""
        pass
