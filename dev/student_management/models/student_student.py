from odoo import fields, models, api, _


class StudentStudent(models.Model):
    _name = 'student.student'
    _description = 'Student Student'

    name = fields.Char('Tên sinh viên', required=True, tracking=True)
    student_code = fields.Char('Mã sinh viên', required=True, tracking=True)
    display_name = fields.Char('Tên hiển thị', compute='_compute_display_name')
    birth = fields.Date('Ngày sinh', required=True)
    mail = fields.Char("Email", required=True)
    phone = fields.Char("Số điện thoại", required=True)

    # Liên hệ
    partner_ids = fields.One2many('res.partner', 'student_id', string="Liên hệ")
    partner_count = fields.Integer("Số liên hệ", compute="_compute_partner_count")

    # Mượn sách
    book_ids = fields.One2many('library.book', 'student_id', string="Sách đang mượn")
    book_count = fields.Integer("Số sách đang mượn", compute="_compute_book_count")

    _sql_constraints = [
        ('student_code', 'unique (student_code)', 'Mã sinh viên đã tồn tại, vui lòng nhập mã sinh viên khác!')
    ]

    @api.depends('name', 'student_code')
    def _compute_display_name(self):
        for rec in self:
            if rec.name and rec.student_code:
                rec.display_name = f"{rec.student_code} - {rec.name}"
            else:
                rec.display_name = rec.student_code or rec.name or ''

    @api.depends('partner_ids')
    def _compute_partner_count(self):
        for rec in self:
            rec.partner_count = len(rec.partner_ids)

    @api.depends('book_ids')
    def _compute_book_count(self):
        for rec in self:
            rec.book_count = len(rec.book_ids)

    def action_view_partners(self):
        self.ensure_one()
        return {
            'name': _('Liên hệ'),
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id, 'default_is_student': True}
        }

    def action_view_books(self):
        self.ensure_one()
        return {
            'name': _('Sách đang mượn'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.book',
            'view_mode': 'tree,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }
