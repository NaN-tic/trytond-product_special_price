# This file is part of product_special_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.pyson import Eval
from trytond.transaction import Transaction

__all__ = ['Template', 'Product']
__metaclass__ = PoolMeta

STATES = {
    'readonly': ~Eval('active', True),
    }
DEPENDS = ['active']


class Template:
    __name__ = 'product.template'
    special_price = fields.Property(fields.Numeric('Special Price',
            states=STATES, digits=(16, 4), depends=DEPENDS))


class Product:
    __name__ = 'product.product'

    @classmethod
    def get_sale_price(cls, products, quantity=0):
        User = Pool().get('res.user')
        PriceList = Pool().get('product.price_list')
        prices = super(Product, cls).get_sale_price(products, quantity)
        if (Transaction().context.get('customer')):
            user = User(Transaction().user)
            if user.shop and user.shop.special_price:
                for product in products:
                    special_price = 0.0
                    if user.shop.type_special_price == 'pricelist':
                        print "dins2"
                        special_price = PriceList.compute(
#                                Transaction().context['price_list'],
                                user.shop.special_pricelist,
                                Transaction().context['customer'],
                                product,
                                product.list_price,
                                quantity,
                                Transaction().context.get('uom',
                                        product.default_uom))
                    else:
                        special_price = product.special_price
                    if special_price != 0.0 and special_price != None and \
                            special_price < prices[product.id]:
                        prices[product.id] = special_price
        return prices
