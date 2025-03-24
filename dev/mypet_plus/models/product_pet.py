from odoo import models, fields, api


class ProductPet(models.Model):
    _name = "product.pet"
    _inherits = {'my.pet': 'my_pet_id'}
    _description = "Product Pet"

    my_pet_id = fields.Many2one('my.pet', string="My Pet",
                                auto_join=True, ondelete='cascade', index=True, required=True)
    pet_type = fields.Selection([
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('vip', 'VIP'),
        ('cute', 'Cute')
    ], 'Pet Type', default='basic')
    pet_color = fields.Selection([
        ('white', 'White'),
        ('black', 'Black'),
        ('grey', 'Grey'),
        ('yellow', 'Yellow')
    ], 'Pet Color', default='white')
    bonus_price = fields.Float('Bonus Price', default=0)
    final_price = fields.Float('Final Price', compute='_compute_final_price')

    @api.depends('basic_price', 'bonus_price')
    def _compute_final_price(self):
        for rec in self:
            rec.final_price = rec.basic_price + rec.bonus_price
