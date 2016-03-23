# This file is part netrivals module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import urllib2
from xml.dom import minidom
from decimal import Decimal
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool

__all__ = ['Netrivals']


class Netrivals(ModelSQL, ModelView):
    'Netrivals'
    __name__ = 'netrivals'

    name = fields.Char('Name', required=True)
    api_uri = fields.Char('Api URI', required=True)
    scheduler = fields.Boolean('Scheduler',
        help='Active by crons (import)')

    @classmethod
    def __setup__(cls):
        super(Netrivals, cls).__setup__()
        cls._buttons.update({
            'update_prices': {},
            })

    @staticmethod
    def default_scheduler():
        return True

    @classmethod
    @ModelView.button
    def update_prices(cls, netrivals):
        pool = Pool()
        Product = pool.get('product.product')
        ProductNetrivals = pool.get('product.netrivals')

        values = {}
        to_create = []
        to_write = []
        for n in netrivals:
            usock = urllib2.urlopen(n.api_uri) 
            xmldoc = minidom.parse(usock)

            for e in xmldoc.getElementsByTagName('Product'):
                name = e.getElementsByTagName('Title')[0].firstChild.data
                # price = e.getElementsByTagName('Price')[0].firstChild.data
                rivals = {}
                for r in e.getElementsByTagName('Rivals')[0].getElementsByTagName('Rival'):
                    rival_name = r.getElementsByTagName('Name')[0].firstChild.data
                    rival_price = r.getElementsByTagName('Price')[0].firstChild.data
                    rivals[rival_name] = rival_price
                values[name] = rivals

        names = values.keys()
        products = Product.search([
            ('name', 'in', names),
            ])
    
        for p in products:
            if p.name in values:
                rivals = values[p.name]
                product_rivals = {}
                for n in p.netrivals:
                    product_rivals[n.name] = n

                for rival in rivals:
                    if rival in product_rivals: # write
                        to_write.extend(([product_rivals[rival]], {
                            'price': Decimal(rivals[rival]),
                            }))
                    else: # create
                        to_create.append({
                            'product': p,
                            'name': rival,
                            'price': Decimal(rivals[rival]),
                            })

        if to_create:
            ProductNetrivals.create(to_create)
        if to_write:
            ProductNetrivals.write(*to_write)

    @classmethod
    def cron_update_netrivals(cls):
        """
        Cron update netrivals:
        """
        netrivals = cls.search([
            ('scheduler', '=', True),
            ])
        cls.update_prices(netrivals)
        return True
