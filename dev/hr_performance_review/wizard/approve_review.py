from odoo import models, fields
from odoo.exceptions import AccessError


class ApproveReviewWizard(models.TransientModel):
    _name = 'approve.review.wizard'
    _description = 'Approve or change status to Draft for hr.performance.review model'

    action_type = fields.Selection([
        ('approve', 'Approve'),
        ('reset', 'Reset')
    ], 'Hành động', required=True, default='approve')

    def action_apply(self):
        # Lấy các bản ghi được chọn
        review_ids = self.env.context.get('active_ids', [])
        reviews = self.env['hr.performance.review'].browse(review_ids)

        # Check quyền admin
        if not self.env.user.has_group('hr_performance_review.group_hr_performance_admin'):
            raise AccessError('Bạn hông có quyền thực hiện thao tác này!')

        # Thực hiện thay đổi trạng thái
        if self.action_type == 'approve':
            reviews.filtered(lambda r: r.state != 'approved').write({'state': 'approved'})
        elif self.action_type == 'reset':
            reviews.filtered(lambda r: r.state != 'draft').write({'state': 'draft'})

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thông báo',
                'message': 'Cập nhật hoàn tất!',
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window_close'  # Đóng wizard sau khi thông báo biến mất
                }
            }
        }
