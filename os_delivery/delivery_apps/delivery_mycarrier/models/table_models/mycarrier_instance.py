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

    location_source = fields.Selection([
        ('warehouse', 'Warehouse'),
        ('location', 'Location')],
        string='Location ID Source', default='warehouse', required=True,
        help="Where the origin locationID sent to MyCarrier comes from:\n"
             "Warehouse: looked up in the Warehouse Mapping tab by the picking's warehouse.\n"
             "Location: looked up in the Location Mapping tab by the picking's source location.")

    warehouse_mapping_ids = fields.One2many('mycarrier.warehouse.mappings', inverse_name='mycarrier_instance_id')

    location_mapping_ids = fields.One2many('mycarrier.location.mappings', inverse_name='mycarrier_instance_id')

    auto_validate_picking = fields.Boolean(
        'Auto-Validate Picking on MyCarrier Confirmation', default=True,
        help="When MyCarrier's webhook confirms a shipment, automatically validate the picking. "
             "If off, the webhook still fills in PRO/BOL/cost and logs the update, but leaves "
             "the picking for manual validation.")

    auto_validate_timing = fields.Selection([
        ('immediate', 'Immediately on Confirmation'),
        ('pickup_date', 'Wait Until Pickup Date')],
        string='Validate Timing', default='pickup_date', required=True,
        help="Immediately: validate as soon as MyCarrier confirms the shipment.\n"
             "Wait Until Pickup Date: hold off validating until the confirmed PickupDate "
             "has actually arrived (matches physical pickup, but the picking sits in "
             "'MyCarrier' state until then). Client's call - confirm before go-live.")


class MycarrierWarehouseMappings(models.Model):
    _name = 'mycarrier.warehouse.mappings'

    _description = 'MyCarrier Warehouse Mappings'

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)

    mycarrier_location_id = fields.Char(string='MyCarrier Location ID', required=True)

    mycarrier_instance_id = fields.Many2one('mycarrier.instance')

    _sql_constraints = [
        ('warehouse_uniq', 'unique (warehouse_id, mycarrier_instance_id)', "Warehouse must be unique.")
    ]


class MycarrierLocationMappings(models.Model):
    _name = 'mycarrier.location.mappings'

    _description = 'MyCarrier Location Mappings'

    location_id = fields.Many2one('stock.location', string='Location', required=True)

    mycarrier_location_id = fields.Char(string='MyCarrier Location ID', required=True)

    mycarrier_instance_id = fields.Many2one('mycarrier.instance')

    _sql_constraints = [
        ('location_uniq', 'unique (location_id, mycarrier_instance_id)', "Location must be unique.")
    ]


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
