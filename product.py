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
    special_price_from = fields.Date('Special Price From')
    special_price_to = fields.Date('Special Price To')


class Product:
    __name__ = 'product.product'

    @classmethod
    def get_sale_price(cls, products, quantity=0):
        Date = Pool().get('ir.date')

        prices = super(Product, cls).get_sale_price(products, quantity)
        today = Date.today()

        if (Transaction().context.get('customer')):
            User = Pool().get('res.user')
            PriceList = Pool().get('product.price_list')

            user = User(Transaction().user)
            if user.shop and user.shop.special_price:
                for product in products:
                    if product.special_price_from and product.special_price_to:
                        if not (product.special_price_from <= today <= product.special_price_to):
                            continue
                    special_price = 0.0
                    if user.shop.type_special_price == 'pricelist':
                        price_list = PriceList(user.shop.special_pricelist)
                        customer = Transaction().context['customer']
                        uom = Transaction().context.get('uom', product.default_uom)

                        special_price = price_list.compute(customer, product,
                            prices[product.id], quantity, uom)
                    else:
                        special_price = product.special_price

                    if special_price != 0.0 and special_price != None and \
                            special_price < prices[product.id]:
                        prices[product.id] = special_price

        return prices
