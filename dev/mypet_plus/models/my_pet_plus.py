from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class MyPetPlus(models.Model):
    _name = 'my.pet'
    _inherit = 'my.pet'
    _description = 'Extend my pet model'

    # new field
    toy = fields.Char('Pet Toy')

    # modify old fields
    age = fields.Integer('Pet Age', default=2)
    gender = fields.Selection(selection_add=[('sterilization', 'Sterilization')])
