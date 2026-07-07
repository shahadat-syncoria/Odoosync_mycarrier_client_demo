from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    dest_delivery_appointment = fields.Boolean('Delivery Appointment', tracking=True)

    dest_inside_delivery = fields.Boolean('Inside Delivery', tracking=True)

    dest_liftgate_delivery = fields.Boolean('Liftgate Delivery', tracking=True)

    dest_notify_delivery = fields.Boolean('Notify Before Delivery', tracking=True)

    dest_sort_segregate_delivery = fields.Boolean('Sort/Segregate Delivery', tracking=True)

    dest_location_type = fields.Many2one('mycarrier.location.type', string='Destination Location Type', tracking=True)

    origin_inbond_freight = fields.Boolean('In Bond Freight', tracking=True)

    origin_inside_pickup = fields.Boolean('Inside Pickup', tracking=True)

    origin_liftgate_pickup = fields.Boolean('Liftgate Pickup', tracking=True)

    origin_protect_from_freeze = fields.Boolean('Protect From Freeze', tracking=True)

    origin_single_shipment = fields.Boolean('Single Shipment', tracking=True)

    origin_location_type = fields.Many2one('mycarrier.location.type', string='Origin Location Type', tracking=True)

    total_weight_done = fields.Float(compute='_cal_total_weight_done', digits='Stock Weight', help="This field is for MyCarrier", compute_sudo=True, string='Total Weight Done')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('mycarrier', 'MyCarrier'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")

    pushed_to_mycarrier = fields.Boolean('Pushed To MyCarrier', copy=False)

    mycarrier_shipment_id = fields.Char('ShipmentId', tracking=True, copy=False)

    mycarrier_customer_bol_number = fields.Char('CustomerBOLNumber', tracking=True, copy=False)

    mycarrier_po_number = fields.Char('PONumber', tracking=True, copy=False)

    mycarrier_ref_number = fields.Char('ReferenceNumber', tracking=True, copy=False)

    mycarrier_pickup_number = fields.Char('PickupNumber', tracking=True, copy=False)

    mycarrier_carrier_code = fields.Char('CarrierCode', tracking=True, copy=False)

    mycarrier_carrier_name = fields.Char('CarrierName', tracking=True, copy=False)

    mycarrier_pro_number = fields.Char('CarrierPRONumber', tracking=True, copy=False)

    mycarrier_total_cost = fields.Float('TotalCost', tracking=True, copy=False)

    mycarrier_pickup_date = fields.Char('Pickup Date', tracking=True, copy=False)

    @api.depends('move_ids.weight_done')
    def _cal_total_weight_done(self):
        for picking in self:
            picking.total_weight_done = sum(move.weight_done for move in picking.move_ids)
