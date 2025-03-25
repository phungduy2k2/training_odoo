from odoo import fields, models

import logging
_logger = logging.getLogger(__name__)


class BatchUpdateWizard(models.TransientModel):
    _name = 'my.pet.batchupdate.wizard'
    _description = "Batch update for my.pet model"

    dob = fields.Date('DOB')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], 'Gender', default=False)
    owner_id = fields.Many2one('res.partner', string='Owner')
    basic_price = fields.Float('Basic Price', default=0)

    def multi_update(self):
        ids = self.env.context['active_ids']
        my_pets = self.env["my.pet"].browse(ids)
        new_data = {}

        if self.dob:
            new_data["dob"] = self.dob
        if self.gender:
            new_data["gender"] = self.gender
        if self.owner_id:
            new_data["owner_id"] = self.owner_id
        if self.basic_price > 0:
            new_data["basic_price"] = self.basic_price

        my_pets.write(new_data)
