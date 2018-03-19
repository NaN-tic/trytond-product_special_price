# This file is part of product_special_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond import backend
from trytond.pool import Pool, PoolMeta
from trytond.model import ModelSQL, fields
from trytond.pyson import Eval
from trytond.transaction import Transaction
from trytond.tools.multivalue import migrate_property

from trytond.modules.product.product import price_digits
from trytond.modules.company.model import CompanyValueMixin

__all__ = ['Template', 'Product']

STATES = {
    'readonly': ~Eval('active', True),
    }
DEPENDS = ['active']


class Template:
    __metaclass__ = PoolMeta
    __name__ = 'product.template'
    special_price = fields.MultiValue(fields.Numeric(
            "Special Price", digits=price_digits,
            states=STATES, depends=DEPENDS))
    special_price_from = fields.Date('Special Price From')
    special_price_to = fields.Date('Special Price To')

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'special_price':
            return pool.get('product.special_price')
        return super(Template, cls).multivalue_model(field)


class ProductSpecialPrice(ModelSQL, CompanyValueMixin):
    "Product Special Price"
    __name__ = 'product.special_price'

    template = fields.Many2One(
        'product.template', "Template", ondelete='CASCADE', select=True)
    special_price = fields.Numeric("Special Price", digits=price_digits)

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(ProductSpecialPrice, cls).__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.append('special_price')
        value_names.append('special_price')
        fields.append('company')
        migrate_property(
            'product.template', field_names, cls, value_names,
            parent='template', fields=fields)


class Product:
    __metaclass__ = PoolMeta
    __name__ = 'product.product'

    @classmethod
    def get_sale_price(cls, products, quantity=0):
        pool = Pool()
        Date = pool.get('ir.date')
        User = pool.get('res.user')
        Uom = pool.get('product.uom')

        prices = super(Product, cls).get_sale_price(products, quantity)

        if Transaction().context.get('without_special_price'):
            return prices

        today = Date.today()
        user = User(Transaction().user)
        if user.shop and user.shop.special_price:
            for product in products:
                if (product.special_price_from and
                        today < product.special_price_from):
                    continue
                if (product.special_price_to and
                        today > product.special_price_to):
                    continue
                special_price = 0.0
                if user.shop.type_special_price == 'pricelist':
                    price_list = user.shop.special_pricelist
                    customer = Transaction().context.get('customer', None)
                    uom_id = Transaction().context.get('uom', None)
                    if uom_id:
                        uom = Uom(uom_id)
                    else:
                        uom = product.default_uom
                    special_price = price_list.compute(customer, product,
                        prices[product.id], quantity, uom)
                else:
                    special_price = product.special_price

                if (special_price != 0.0
                        and special_price is not None
                        and special_price < prices[product.id]):
                    prices[product.id] = special_price
        return prices
