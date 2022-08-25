from odoo import fields, models, api


class Clinic(models.Model):
    _name = 'res.clinic'
    name = fields.Char()
    clinic_no=fields.Integer()
    doctors_ids=fields.Many2many("res.users")


