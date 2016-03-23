# This file is part netrivals module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .netrivals import *
from .product import *

def register():
    Pool.register(
        Netrivals,
        Product,
        ProductNetrivals,
        module='netrivals', type_='model')
