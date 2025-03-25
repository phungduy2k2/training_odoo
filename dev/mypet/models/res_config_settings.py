from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_basic_price = fields.Float('Default Pet\'s Basic Price', default_model='my.pet')
    mypet_is_check_duplicated_pet_name = fields.Boolean('Check duplicated pet name', config_parameter='mypet.is_check_duplicated_pet_name')
