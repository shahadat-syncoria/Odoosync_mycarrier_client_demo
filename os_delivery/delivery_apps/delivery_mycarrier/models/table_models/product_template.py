from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    mycarrier_commodity_class = fields.Char('MyCarrier Freight Class')

    mycarrier_commodity_nmfc = fields.Char('MyCarrier NMFC')

    mycarrier_commodity_sub = fields.Char('MyCarrier NMFC Sub')
