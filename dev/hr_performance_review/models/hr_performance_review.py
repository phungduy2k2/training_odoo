from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError


class HrPerformanceReview(models.Model):
    _name = 'hr.performance.review'
    _description = 'HR Performance Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Tên", required=True)
    employee_id = fields.Many2one('hr.employee', string="Nhân viên", required=True)
    review_date = fields.Date("Ngày đánh giá", default=fields.Date.today, tracking=True)
    reviewer_id = fields.Many2one('res.users', string="Người đánh giá", required=True, tracking=True,
        domain=lambda self: [('groups_id', 'in', [self.env.ref('hr_performance_review.group_hr_performance_manager').id])]
    )
    performance_score = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Average'),
        ('3', 'Good'),
        ('4', 'Excellent')
    ], "Điểm hiệu suất", tracking=True)
    comments = fields.Text("Nhận xét")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved')
    ], "Trạng thái", default='draft', required=True, tracking=True)

    is_admin = fields.Boolean(compute="_compute_is_admin")

    @api.constrains('review_date')
    def _check_review_date(self):
        for rec in self:
            if rec.review_date and rec.review_date < fields.Date.today():
                raise ValidationError(_("Ngày đánh giá không thể trong quá khứ!"))

    def _compute_is_admin(self):
        for rec in self:
            rec.is_admin = self.env.user.has_group('hr_performance_review.group_hr_performance_admin')

    def action_submit(self):
        # Check người đánh giá
        if (self.reviewer_id.id != self.env.user.id and
                not self.env.user.has_group('hr_performance_review.group_hr_performance_admin')):
            raise AccessError(_("Bạn không phải người đánh giá."))
        # Sửa trạng thái draft -> submitted
        self.write({'state': 'submitted'})
        # Ghi log
        self.message_post(body=_("Phiếu đánh giá hiệu suất được submit bởi %s") % self.env.user.name)
        return True

    def action_approve(self): 
        # Check quyền
        if (self.reviewer_id.id != self.env.user.id and
                not self.env.user.has_group('hr_performance_review.group_hr_performance_admin')):
            raise AccessError(_("Bạn không có quyền phê duyệt phiếu đánh giá này."))
        # Sửa trạng thái submitted -> approved
        self.write({'state': 'approved'})
        # Ghi log
        self.message_post(body=_("Phiếu đánh giá này được phê duyệt bởi %s") % self.env.user.name)
        return True

    def action_reset_to_draft(self):
        # Check quyền
        if not self.env.user.has_group('hr_performance_review.group_hr_performance_admin'):
            raise AccessError(_("Bạn không có quyền thực hiện thao tác này."))
        self.write({
            'state': 'draft'
        })
        # Ghi log
        self.message_post(body=_("Phiếu đánh giá này quay lại trạng thái DRAFT bởi %s") % self.env.user.name)
        return True

    def write(self, vals):
        # Check trạng thái trước khi cho phép cập nhật
        for rec in self:
            if rec.state != 'draft' and not self.env.user.has_group('hr_performance_review.group_hr_performance_manager'):
                raise AccessError(_("Bạn không có quyền sửa một đánh giá đã submit hoặc approve."))
        return super(HrPerformanceReview, self).write(vals)

    def unlink(self):
        # Nếu là admin, có thể xóa bất kỳ bản ghi
        if self.env.user.has_group('hr_performance_review.group_hr_performance_admin'):
            return super(HrPerformanceReview, self).unlink()
        # Còn nếu là nhân viên hoặc quản lý, chỉ có thể xóa bản ghi draft
        elif self.state != 'draft':
            raise AccessError(_("Bạn không có quyền xóa bản ghi không ở trạng thái Draft."))
        return super(HrPerformanceReview, self).unlink()
