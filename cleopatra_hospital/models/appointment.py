from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Name', readonly=True, default=lambda self: _('New'))
    reference = fields.Char(string='Reference', readonly=True, default=lambda self: _('New'))

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True, tracking=True)

    appointment_date = fields.Date(string='Date', required=True, tracking=True)
    appointment_time = fields.Float(string='Time', required=True, tracking=True,
                                    help="Example: 13.5 = 1:30 PM")


    medicine_line_ids = fields.One2many('appointment.medicine.line', 'appointment_id', string="Lines")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    department_id = fields.Many2one('hospital.department', string='Department')
    room_id = fields.Many2one('hospital.room', string='Room')

    notes = fields.Text(string='Doctor Notes')
    symptoms = fields.Text(string='Symptoms')
    diagnosis = fields.Text(string='Diagnosis')
    prescription = fields.Text(string='Prescription')

    total_medicine_qty = fields.Float(string = 'Total Medicines', compute="_compute_total_medicine_qty" )



    @api.depends('medicine_line_ids')
    def _compute_total_medicine_qty(self):
        print ("function _compute_total_medicine_qty called ")
        for appointment in self:
            total_qty = 0
            for line in appointment.medicine_line_ids:
                total_qty += line.quantity

            appointment.total_medicine_qty = total_qty



    # Billing
    # service_id = fields.Many2one('hospital.service', string='Medical Service')
    # service_fee = fields.Float(string='Service Fee', related='service_id.price', readonly=True)



    # Automatic Reference Number
    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        return super(Appointment, self).create(vals)

    def action_open_appointment_wizard(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("cleopatra_hospital.action_view_appointment_wizard")
        # action['res_id'] = self.id
        return action