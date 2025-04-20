from odoo import models, fields, api
from odoo.exceptions import UserError
import re
class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    name = fields.Char(compute='_compute_name', store=True)
    email = fields.Char()
    birth_date = fields.Date()
    age = fields.Integer(compute='_compute_age')
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ], string='Blood Type')
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    history = fields.Html()
    _rec_name = 'name'
    department_id = fields.Many2one('hms.department', string='Department', domain="[('is_opened', '=', True)]")
    department_capacity = fields.Integer(related='department_id.capacity', readonly=True)
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors')

    STATE_SELECTION = [
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ]
    state = fields.Selection(STATE_SELECTION, string='State', default='undetermined')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Logs')
    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email address must be unique!')
    ]


    @api.onchange('age', 'birth_date')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR Check',
                    'message': 'PCR has been automatically checked as patient age is below 30.'
                }
            }
    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}" if record.first_name and record.last_name else 'No Name'
    @api.model
    def write(self, vals):
        res = super(Patient, self).write(vals)
        if 'state' in vals:
            self.env['hms.patient.log'].create({
                'patient_id': self.id,
                'description': f'Patient state changed to {vals["state"]}.',
                'created_by': self.env.user.id
            })
        return res

    @api.constrains('email')
    def _check_email_validity(self):
        for record in self:
            if record.email:
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, record.email):
                    raise UserError("Invalid email format. Please enter a valid email address.")

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                birth_date = fields.Date.from_string(record.birth_date)
                record.age = (today - birth_date).days // 365
            else:
                record.age = 0

    def set_good(self):
        self.state = 'good'

    def set_fair(self):
        self.state = 'fair'

    def set_serious(self):
        self.state = 'serious'

    def set_undetermined(self):
        self.state = 'undetermined'


class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'

    patient_id = fields.Many2one('hms.patient', string='Patient')
    description = fields.Text(string='Description')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
