import json
from odoo import models, fields, api, exceptions, _
import ast
import logging
import requests
from markupsafe import Markup, escape
from datetime import datetime
_logger = logging.getLogger(__name__)


def _format_mycarrier_price_breakdown_html(payload):
    """Build HTML cost breakdown from MyCarrier's ShipmentPriceDetails."""
    price_details = payload.get('ShipmentPriceDetails') or []
    if not price_details:
        return Markup("")
    li = "".join(
        "<li>%s: $%s</li>" % (escape(item.get('Description', '')), escape(item.get('Amount', '')))
        for item in price_details
    )
    total = payload.get('TotalCost')
    total_line = Markup("")
    if total is not None:
        total_line = Markup("<li><b>%s: $%s</b></li>") % (escape(_("Total")), escape(total))
    return Markup("<div><b>%s</b><ul>%s%s</ul></div>") % (escape(_("Cost breakdown")), Markup(li), total_line)


def _download_mycarrier_file(url):
    if not url:
        return None
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.content
        _logger.warning('MyCarrier file download failed (status %s) for %s', response.status_code, url)
    except Exception as e:
        _logger.warning('MyCarrier file download failed for %s: %s', url, e)
    return None


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
