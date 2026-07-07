import json
from odoo import models, fields, api, exceptions, _
import ast
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime


class MycarrierWebhook(models.Model):
    _name = 'mycarrier.webhook'

    _description = 'MyCarrier Webhook'

    _order = 'id desc'

    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('mycarrier.webhook'))

    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'), ('done', 'Done'), ('error', 'Error')],
        default='draft',
    )

    data = fields.Char('Data')
