from odoo import fields, models, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer Model'

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False

    name = fields.Char(string='Description', compute='_compute_name')
    price = fields.Monetary(string='Price')
    status = fields.Selection(selection=[('accepted', 'Accepted'),
                                         ('refused', 'Refused')
                                         ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer')  ### required=True
    partner_email = fields.Char(related='partner_id.email', string='Customer Email')
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    create_date = fields.Date(string='Create Date', default=fields.Date.today())
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for rec in self:
            if rec.create_date and rec.validity:
                rec.date_deadline = rec.create_date + timedelta(days=rec.validity)
            else:
                rec.date_deadline = False

    def _inverse_date_deadline(self):
        for rec in self:
            if rec.create_date and rec.date_deadline:
                rec.validity = (rec.date_deadline - rec.create_date).days
            else:
                rec.validity = False

    # @api.autovacuum
    # def _clean_offers(self):
    #     self.search([('status', '=', 'refused')]).unlink()

    # _sql_constraints = [
    #     ('check_validity', 'check(validity > 0)', 'Deadline cannot be before creation date.')
    # ]
    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.date_deadline <= rec.create_date:
                raise ValidationError(_('Deadline cannot be before creation date.'))

    # def write(self, vals):
    #     print(vals)
    #     res_partner = self.env['res.partner'].search([
    #         ('is_company', '=', True)
    #     ]).mapped('phone')
    #     print(res_partner)
    #     return super(PropertyOffer, self).write(vals)

    def accept_offer(self):
        if self.property_id:
            if self.env['estate.property.offer'].search([
                ('property_id', '=', self.property_id.id),
                ('status', '=', 'accepted')
            ]):
                raise ValidationError('You have an accepted offer already.')

            self.property_id.write({
                'selling_price': self.price,
                'state': 'accepted'
            })
            self.status = 'accepted'

    def refuse_offer(self):
        if self.status == 'refused':
            raise ValidationError('You have refused this offer already.')
        self.status = 'refused'
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received'
            })

    def extend_offer_deadline(self):
        activ_ids = self._context.get('active_ids', [])
        if activ_ids:
            offer_ids = self.env['estate.property.offer'].browse(activ_ids)
            for offer in offer_ids:
                offer.validity = 10

    def _extend_offer_deadline(self):
        offer_ids = self.env['estate.property.offer'].search([])
        for offer in offer_ids:
            offer.validity += 1

