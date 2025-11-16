from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class Department(models.Model):
    _name = 'hospital.department'
    _description = 'Department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Department Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    description = fields.Text(string='Description')
    manager_id = fields.Many2one('hospital.doctor', string='Department Manager')
    doctor_ids = fields.One2many('hospital.doctor', 'department_id', string='Doctors')
    room_ids = fields.One2many('hospital.room', 'department_id', string='Rooms')