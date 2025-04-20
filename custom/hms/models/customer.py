from odoo import models, fields, api
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        comodel_name='hms.patient',
        string='Related Patient',
    )

    @api.constrains('email', 'related_patient_id')
    def _check_patient_email_unique(self):
        for record in self:
            if record.email:
                if record.related_patient_id:
                    patient = self.env['hms.patient'].search([
                        ('email', '=', record.email)
                    ], limit=1)
                    if patient:
                        raise UserError(
                            f"Cannot link this customer! Another patient with email '{record.email}' already exists."
                        )

    def unlink(self):
        for partner in self:
            if partner.related_patient_id:
                raise UserError("You cannot delete a customer that is linked to a patient.")
        return super(ResPartner, self).unlink()