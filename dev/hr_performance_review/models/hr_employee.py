from odoo import models, fields, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    performance_review_count = fields.Integer(
        compute='_compute_performance_review_count',
        string='Số đánh giá'
    )
    average_performance_score = fields.Float(
        string='Điểm đánh giá trung bình',
        compute='_compute_performance_score',
        help="The average score from all approved performance reviews",
        digits=(2, 1)
    )

    def _compute_performance_review_count(self):
        for employee in self:
            reviews_count = self.env['hr.performance.review'].search_count([('employee_id', '=', employee.id)])
            employee.performance_review_count = reviews_count

    def _compute_performance_score(self):
        for employee in self:
            approved_reviews = self.env['hr.performance.review'].search([
                ('employee_id', '=', employee.id),
                ('state', '=', 'approved')
            ])
            if approved_reviews:
                total_score = 0
                for review in approved_reviews:
                    total_score += int(review.performance_score)
                    employee.average_performance_score = round(total_score / len(approved_reviews), 1)
            else:
                employee.average_performance_score = 0.0

    def action_view_performance_reviews(self):
        self.ensure_one()
        return {
            'name': _('Phiếu đánh giá'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.performance.review',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }
