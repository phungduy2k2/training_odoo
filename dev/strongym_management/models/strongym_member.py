from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re
class StrongymMember(models.Model):
    _name = 'strongym.member'
    _description = 'Strongym Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string="Tên thành viên", required=True, tracking=True, index=True)
    dob = fields.Date(string="Ngày sinh", required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ')
    ], string="Giới tính", required=True, tracking=True)
    phone = fields.Char(string="Số điện thoại", required=True, tracking=True, index=True)
    image = fields.Binary(string="Ảnh", attachment=True, required=True)
    address = fields.Text(string="Địa chỉ", required=True)
    membership_plan_id = fields.Many2one('strongym.membership.plan', string="Gói tập")
    status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired')
    ], string="Trạng thái", required=True)
    expired_date = fields.Date(string="Ngày hết hạn")

    _sql_constraints = [
        ('phone_unique', 'UNIQUE(phone)', 'This phone number is used!')
    ]

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not re.match(r'^0\d{9}$', record.phone):
                raise ValidationError(_('Số điện thoại không hợp lệ! Phải bắt đầu bằng số 0 và có 10 chữ số.'))

    @api.constrains('expired_date')
    def _check_expired_date(self):
        for record in self:
            if record.expired_date and record.expired_date < fields.Date.today():
                record.status = 'expired'
