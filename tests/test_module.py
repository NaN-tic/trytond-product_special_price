
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.modules.sale_shop.tests import SaleShopCompanyTestMixin
from trytond.tests.test_tryton import ModuleTestCase


class ProductSpecialPriceTestCase(SaleShopCompanyTestMixin, ModuleTestCase):
    'Test ProductSpecialPrice module'
    module = 'product_special_price'
    extras = ['product_esale']


del ModuleTestCase
