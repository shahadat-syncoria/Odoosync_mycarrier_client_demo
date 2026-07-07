from odoo import api, fields, models
from odoo.exceptions import ValidationError
import copy
from logging import getLogger
import requests
from requests.auth import HTTPBasicAuth
import json
_logger = getLogger(__name__)
from random import randint
from odoo.addons.odoosync_base.utils.app_delivery import AppDelivery


class MycarrierLocationType(models.Model):
    _name = "mycarrier.location.type"

    _description = "MyCarrier Location Type"

    _order = 'sequence DESC'

    name = fields.Char(string='Name', required=True, copy=False)

    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Location Type already exists !"),
    ]


class MycarrierInstance(models.Model):
    _name = 'mycarrier.instance'

    _description = 'MyCarrier Instance'

    name = fields.Char('Instance Name')

    token = fields.Char('Service Key')

    account_id = fields.Many2one(
        string='Linked Account',
        comodel_name='omni.account',
        ondelete='restrict',
    )

    connect_state = fields.Selection([
        ('draft', 'Failed'),
        ('confirm', 'Confirmed')],
        default='draft', string='State')

    product_mapping_ids = fields.One2many('mycarrier.product.mappings', inverse_name='mycarrier_instance_id')

    registered_webhook_ids = fields.One2many('mycarrier.registered.webhooks', inverse_name='mycarrier_instance_id')

    delivery_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Delivery Product',
        domain=[('type', '=', 'service')],
        help="""Delivery product used for shipping method creation.""",
    )


class MycarrierRegisteredWebhook(models.Model):
    _name = 'mycarrier.registered.webhooks'

    _description = 'MyCarrier Register Webhooks'

    webhook_environment = fields.Char('Environment')

    webhook_username = fields.Char('Credential UserName')

    webhook_customerid = fields.Char('CustomerID')

    webhook_type = fields.Char('Webhook Type')

    webhook_uri = fields.Char('URI')

    mycarrier_instance_id = fields.Many2one('mycarrier.instance')


class MycarrierAccessorials(models.Model):
    _name = "mycarrier.accessorials"

    _description = "MyCarrier Accessorials"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Accessorial', required=True)

    color = fields.Integer('Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Accessorial already exists !"),
    ]
