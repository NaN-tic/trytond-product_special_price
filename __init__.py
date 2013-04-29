# This file is part of product_special_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.pool import Pool
from .shop import *
from .product import *


def register():
    Pool.register(
        SaleShop,
        Template,
        Product,
        module='product_special_price', type_='model')
