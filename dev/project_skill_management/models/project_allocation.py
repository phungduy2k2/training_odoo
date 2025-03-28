from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProjectAllocation(models.Model):
    _name = 'project.allocation'
    _description = 'Phân bổ nguồn lực dự án'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', "Nhân viên", required=True)
    project_id = fields.Many2one('project.project', 'Dự án', required=True)
    allocated_hours = fields.Float('Số giờ phân bổ', required=True)
    start_date = fields.Date('Ngày bắt đầu', default=fields.Date.today)
    end_date = fields.Date('Ngày kết thúc')
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã Xác Nhận'),
        ('completed', 'Hoàn Thành')
    ], default='draft', string='Trạng Thái')

    @api.constrains('allocated_hours')
    def _check_allocated_hours(self):
        for rec in self:
            if rec.allocated_hours <= 0:
                raise ValidationError("Số giờ phân bổ phải lớn hơn 0.")
            employee = rec.employee_id
            if rec.allocated_hours > employee.available_capacity:
                raise ValidationError(f"Nhân viên {employee.name} không đủ thời gian trống. "
                                      f"Còn trống {employee.available_capacity} giờ.")

    @api.constrains('start_date', 'end_date')
    def _check_date(self):
        for rec in self:
            if rec.end_date and rec.start_date > rec.end_date:
                raise ValidationError("Ngày bắt đầu phải trước ngày kết thúc.")
