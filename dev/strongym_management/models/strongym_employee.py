from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re

class StrongymEmployee(models.Model):
    _name = 'strongym.employee'
    _description = 'Strongym Employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Họ và tên', required=True, tracking=True, index=True)
    dob = fields.Date(string="Ngày sinh", required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ')
    ], string="Giới tính", required=True, tracking=True)
    phone = fields.Char(string="Số điện thoại", required=True, tracking=True, index=True)
    id_card = fields.Char(string="CCCD", required=True)
    image = fields.Binary(string="Ảnh", attachment=True, required=True)
    position = fields.Selection([
        ('manager', 'Quản lý'),
        ('trainer', 'Huấn luyện viên'),
        ('security', 'Bảo vệ'),
        ('receptionist', "Lễ tân"),
        ('cleaner', 'Lao công')
    ], string="Chức vụ", required=True, tracking=True)
    address = fields.Text(string="Địa chỉ", required=True)

    _sql_constraints = [
        ('phone_unique', 'UNIQUE(phone)', _('This phone number is used!')),
        ('id_card_uniq', 'UNIQUE(id_card)', _('CCCD/CMND này đã được đăng ký!'))
    ]

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not re.match(r'^0\d{9}$', record.phone):
                raise ValidationError(_('Số điện thoại không hợp lệ! Phải bắt đầu bằng số 0 và có 10 chữ số.'))

    @api.constrains('id_card')
    def _check_id_card(self):
        for record in self:
            if record.id_card and not re.match(r'^\d{9,12}$', record.id_card):
                raise ValidationError(_('CCCD/CMND không hợp lệ! Phải có từ 9 đến 12 chữ số.'))
