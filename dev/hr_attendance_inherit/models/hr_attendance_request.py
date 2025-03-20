from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AttendanceRequest(models.Model):
    _name = 'hr.attendance.request'
    _description = 'Attendance Request'
    _rec_name = 'name'

    name = fields.Char(string='Tên phiếu yêu cầu', readonly=True)
    request_date = fields.Date(string='Ngày yêu cầu', default=fields.Date.today, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Người yêu cầu', readonly=True,
                                  default=lambda self: self.env.user.employee_id.id)
    request_type = fields.Selection([
        ('check_in_morning', "Check-in sáng"),
        ('check_out_morning', "Check-out sáng"),
        ('check_in_afternoon', "Check-in chiều"),
        ('check_out_afternoon', "Check-out chiều")
    ], string='Loại yêu cầu', required=True)
    reason = fields.Char(string='Lý do')
    state = fields.Selection([
        ('draft', "Nháp"),
        ('waiting', "Chờ duyệt"),
        ('approved', "Đã duyệt"),
        ('rejected', "Từ chối"),
    ], string='Trạng thái', default='draft')

    @api.model
    def create(self, vals):
        self._check_duplicate_request(vals)

        record = super(AttendanceRequest, self).create(vals)

        # Tạo phiếu yêu cầu theo định dạng
        employee_name = record.employee_id.name or ''
        date_str = record.request_date.strftime('%d/%m/%Y')
        record.name = f"{employee_name} yêu cầu bù công ngày {date_str}"

        record.state = 'waiting'
        return record

    def write(self, vals):
        if 'request_type' in vals:
            for record in self:
                new_vals = {
                    'employee_id': vals.get('employee_id', record.employee_id.id),
                    'request_date': vals.get('request_date', record.request_date),
                    'request_type': vals.get('request_type', record.request_type)
                }
                record._check_duplicate_request(new_vals)

        return super(AttendanceRequest, self).write(vals)

    def _check_duplicate_request(self, vals):
        employee_id = vals.get('employee_id', self.env.user.employee_id.id)
        request_date = vals.get('request_date', fields.Date.today())
        request_type = vals.get('request_type')

        domain = [
            ('employee_id', '=', employee_id),
            ('request_date', '=', request_date),
            ('request_type', '=', request_type),
            ('id', 'not in', self.ids)
        ]

        existing_request = self.search(domain, limit=1)
        if existing_request:
            raise ValidationError(_(
                "Bạn đã tạo phiếu yêu cầu tương tự cho ngày này và loại yêu cầu này."
                "\nVui lòng kiểm tra lại phiếu yêu cầu."
            ))

    def action_submit(self):
        self.write({'state': 'waiting'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})
