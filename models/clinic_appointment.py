from odoo import fields, models, api
from odoo.fields import Date
from odoo.exceptions import UserError


class PatientAppointment(models.Model):
    _name = 'patient.appointment'
    _description = 'Clinic Appointment Model'
    name = fields.Char(readonly=True)
    patient_id = fields.Many2one("res.patient")
    clinic_id = fields.Many2one("res.clinic")
    doctor_id = fields.Many2one("res.users")
    notes = fields.Text()
    date = fields.Date(default=Date.today())
    state = fields.Selection(
        [('new', 'new'), ('confirmed', 'confirmed'), ('cancelled', 'cancelled'), ('draft', 'draft')], default='new')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    pharmacy_ids=fields.One2many('patient.pharmacy','appointment_id')
    hide_price=fields.Boolean(string='Hide Price')
    @api.onchange("clinic_id")
    def change_clinic_doctors(self):
        return {"domain": {"doctor_id": [('id', 'in', self.clinic_id.doctors_ids.ids)]}}

    def change_state_new(self):
        self.state = "new"

    def change_state_confirm(self):
        self.state = "confirmed"

    def change_state_cancel(self):
        self.state = "cancelled"

    def change_state_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('clinic.appointment')
        return super(PatientAppointment, self).create(vals)

    def unlink(self):
        for record in self:
            if record.state:
                if not record.state == "confirmed":
                    super().unlink()
                else:
                    raise UserError("You Can not delete Patient related with  Confirmed Appointment ")
    def rainbow_effect_action(self):
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'message',
                    'type': 'rainbow_man',
                }
            }

class PatientPharmacy(models.Model):
    _name = 'patient.pharmacy'
    _description = 'Clinic Pharmacy Model'
    product_id=fields.Many2one('product.product',required=True)
    qty=fields.Integer(string='Quantity')
    price=fields.Float(string='Price',related='product_id.list_price')
    appointment_id=fields.Many2one('patient.appointment')
