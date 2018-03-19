# This file is part of product_special_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.product_special_price.tests.test_product_special_price import suite
except ImportError:
    from .test_product_special_price import suite

__all__ = ['suite']
