from odoo import models, fields, api
from datetime import date ,timedelta

class HrEmployee(models.Model):
    _inherit ='hr.employee'

    employee_number = fields.Char(
        string='Employee ID',
        readonly=True,
        copy=False
    )
    
    age = fields.Integer(
            string="Age",
            compute="_compute_age",
            store=True
        )
    
    iqama_end_date = fields.Date(string="Iqama End Date")
       
    @api.model
    def create(self, vals):
        if not vals.get('employee_number'):
            seq = self.env['ir.sequence'].next_by_code('hr.employee.id')
            vals['employee_number'] = seq
        return super(HrEmployee, self).create(vals)
    
    @api.depends('birthday')
    def _compute_age(self):
        for employee in self:
            if employee.birthday:
                today = date.today()
                birth = employee.birthday
                    # Calculate age in years
                age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
                employee.age = age
            else:
                employee.age = 0
 
#  notify hr iqama expiry               
    def _notify_hr_iqama_expiry(self):
        """Create HR activity for employees whose Iqama ends within 30 days"""
        today = date.today()
        one_month_later = today + timedelta(days=30)

        # Employees whose Iqama ends in the next 30 days
        expiring_employees = self.search([
            ('iqama_end_date', '>=', today),
            ('iqama_end_date', '<=', one_month_later)
        ])

        # HR users to notify
        hr_users = self.env['res.users'].search([('groups_id', 'in', self.env.ref('hr.group_hr_user').id)])

        for emp in expiring_employees:
            # Check if activity already exists for this employee and user
            existing_activity = self.env['mail.activity'].search([
                ('res_model', '=', 'hr.employee'),
                ('res_id', '=', emp.id),
                ('user_id', 'in', hr_users.ids),
                ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_warning').id),
                ('note', 'ilike', 'Iqama expiry within 30 days')
            ])
            if existing_activity:
                continue

            for user in hr_users:
                self.env['mail.activity'].create({
                    'res_model_id': self.env['ir.model']._get('hr.employee').id,
                    'res_id': emp.id,
                    'user_id': user.id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_warning').id,
                    'summary': f"Iqama of {emp.name} will expire soon",
                    'note': "Iqama expiry within 30 days",
                    'date_deadline': emp.iqama_end_date
                })