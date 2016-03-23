# This file is part netrivals module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class NetrivalsTestCase(ModuleTestCase):
    'Test Netrivals module'
    module = 'netrivals'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            NetrivalsTestCase))
    return suite
