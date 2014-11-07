# This file is part of product_special_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval

__all__ = ['SaleShop']
__metaclass__ = PoolMeta


class SaleShop:
    __name__ = 'sale.shop'

    special_price = fields.Boolean('Apply Special Price')
    type_special_price = fields.Selection([
            ('price', 'Special Price'),
            ('pricelist', 'Special Pricelist'),
            ], 'Special Price', states={
                'required': Eval('special_price', True),
            }, depends=['special_price'])
    special_pricelist = fields.Many2One('product.price_list', 
            'Special Pricelist', states={
                'required': Eval('type_special_price') == 'pricelist',
            }, depends=['type_special_price'])

    @staticmethod
    def default_type_special_price():
        return 'price'
