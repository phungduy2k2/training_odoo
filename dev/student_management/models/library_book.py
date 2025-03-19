from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    code = fields.Char(string='Mã sách', required=True, tracking=True, readonly=True, default=lambda self: _('New'))
    name = fields.Char(string='Tên sách', required=True, tracking=True)
    publish_year = fields.Char(string='Năm xuất bản')
    author = fields.Char(string='Tác giả')
    student_id = fields.Many2one('student.student', string='Sinh viên mượn')

    @api.constrains('publish_year')
    def _check_publish_year(self):
        for rec in self:
            if rec.publish_year and not rec.publish_year.isdigit():
                raise ValidationError(_("Năm xuất bản phải là số!"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('library.book.sequence') or _('New')
        return super(LibraryBook, self).create(vals_list)
