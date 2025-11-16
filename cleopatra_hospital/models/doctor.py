from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Doctor Name', required=True, tracking=True)
    license_number = fields.Char(string='License Number', required=True, tracking=True)
    specialization = fields.Char(string='Specialization', tracking=True)
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    department_id = fields.Many2one('hospital.department', string='Department', tracking=True)
    available_from = fields.Float(string='Available From (HH.MM)', help="Example: 9.5 means 9:30 AM")
    available_to = fields.Float(string='Available To (HH.MM)', help="Example: 17.0 means 5:00 PM")

    image = fields.Binary(string="Doctor Image")

    # appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string='Appointments')