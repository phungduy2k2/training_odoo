from odoo import fields, models, api

class StrongymMembershipPlan(models.Model):
    _name = 'strongym.membership.plan'
    _description = 'Strongym Membership Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Tên gói tập', required=True, tracking=True)
    duration = fields.Integer(string='Thời hạn (tháng)', required=True, tracking=True)
    price = fields.Float(string='Giá', required=True, tracking=True)
    description = fields.Text(string='Mô tả')

    member_ids = fields.One2many('strongym.member', 'membership_plan_id', string='Members')
    member_count = fields.Integer(compute='_compute_member_count', string="Số thành viên")

    @api.depends('member_ids')
    def _compute_member_count(self):
        for record in self:
            record.member_count = len(record.member_ids)
