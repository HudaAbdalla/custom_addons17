from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class Medicine(models.Model):
    _name = 'hospital.medicine'
    _description = 'Medicine'
    _log_access = True
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string = 'Name', readonly=False, store=True)