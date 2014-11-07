#!/usr/bin/env python
# This file is part of product_special_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends


class ProductSpecialPriceTestCase(unittest.TestCase):
    'Test SalePriceList module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('product_special_price')

    def test0005views(self):
        'Test views'
        test_view('product_special_price')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductSpecialPriceTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
