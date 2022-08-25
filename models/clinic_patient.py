from odoo import fields, models, api


class ClinicPatient(models.Model):
    _name = 'res.patient'
    _inherits = {"res.partner": "partner_id"}
    _inherit = ['mail.thread','mail.activity.mixin']
    partner_id = fields.Many2one('res.partner',string='Patient Name')
    birth_date=fields.Date(tracking=True)
    age = fields.Integer(compute='cal_age')
    gender = fields.Selection([('m', 'Male'), ('f', 'Female')])
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB')])
    height = fields.Float(tracking=True)
    weight = fields.Float()
    active=fields.Boolean(string="Active",default=True)
    # api.depends('height')
    # def _cal_weight(self):
    #     for patient in self:
    #         patient.weight = patient.height * 0.5
    total_seats = fields.Integer()
    taken_seats = fields.Integer(compute='_taken_seats')
    api.depends('birth_date')
    def cal_age(self):
        for patient in self:
            if patient.birth_date:
                    today = fields.Date.today()
                    delta = (today - patient.birth_date).days
                    patient.age = delta // 365
            else:
                patient.age = 0

    api.depends('total_seats')
    def _taken_seats(self):
        for record in self:
            if not record.total_seats:
                record.taken_seats = 0
            else:
                record.taken_seats =int (100* len(record.partner_id)/record.total_seats)

