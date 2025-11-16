from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class MedclineLines(models.Model):
    _name = 'appointment.medicine.line'
    _description = 'Medcline Lines'
    _log_access = True
    _inherit = ['mail.thread', 'mail.activity.mixin']

    medicine_id = fields.Many2one('hospital.medicine', string = 'Medicine')
    quantity = fields.Float(string = 'quantity', digits =(20,2))
    doze_per_day = fields.Float(string = 'Doze Per Day', digits =(20,2))
    appointment_id = fields.Many2one('hospital.appointment', string='appointments')


