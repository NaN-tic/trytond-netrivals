# This file is part netrivals module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta
from trytond.modules.product import price_digits

__all__ = ['Product', 'ProductNetrivals']


class Product:
    __name__ = 'product.product'
    __metaclass__ = PoolMeta

    netrivals = fields.One2Many('product.netrivals',
            'product', 'Netrivals')


class ProductNetrivals(ModelSQL, ModelView):
    'Product Netrivals'
    __name__ = 'product.netrivals'

    product = fields.Many2One('product.product',
        'Product', ondelete='CASCADE', required=True)
    name = fields.Char('Name', required=True)
    price = fields.Numeric('Price', digits=price_digits, required=True)

    @classmethod
    def __setup__(cls):
        super(ProductNetrivals, cls).__setup__()
        cls._order.insert(0, ('price', 'ASC'))
