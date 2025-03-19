from odoo import fields, models, api


class Property(models.Model):
    _name = 'estate.property'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'website.published.mixin', "website.seo.metadata"]
    _description = 'Estate Property Model'

    name = fields.Char(string='Name', required=True, tracking=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available from')
    expected_price = fields.Monetary(string='Expected price', tracking=True)
    best_offer = fields.Monetary(string='Best Offer', compute='_compute_best_offer')
    selling_price = fields.Monetary(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage', default=False)
    garden = fields.Boolean(string='Garden', default=False)
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(selection=[
                                              ('north', 'North'),
                                              ('south', 'South'),
                                              ('east', 'East'),
                                              ('west', 'West')
                                          ], string='Garden Orientation', default='north')
    state = fields.Selection(selection=[
                                ('new', 'New'),
                                ('received', 'Offer Received'),
                                ('accepted', 'Offer Accepted'),
                                ('sold', 'Sold'),
                                ('cancel', 'Cancel')
                            ], string='Status', default='new', tracking=True)
    type_id = fields.Many2one('estate.property.type', string='Property Type', tracking=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tags', tracking=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Property Offers')
    sales_id = fields.Many2one('res.users', string='Salesman')  #### default=lambda self: self.env.user
    buyer_id = fields.Many2one('res.partner', string='Buyer')  ### copy=False, domain=[('is_companies', '=', True)]
    buyer_phone = fields.Char(string="Phone", related='buyer_id.phone')
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    def action_sold(self):
        for rec in self:
            rec.state = 'sold'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = max(rec.offer_ids.mapped('price'), default=0)

    def action_url_action(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://odoo.com',
            'target': 'new'
        }

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Estate Property - %s' % self.name

    def _compute_website_url(self):
        for rec in self:
            rec.website_url = "/properties/%s" % rec.id

    def action_send_email(self):
        mail_template = self.env.ref("real_estate_ads.offer_mail_template")
        mail_template.send_mail(self.id, force_send=True)

    def _get_emails(self):
        return ','.join(self.offer_ids.mapped('partner_email'))
