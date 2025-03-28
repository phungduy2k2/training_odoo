from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    skill_ids = fields.Many2many('hr.employee.skill', string="Kỹ năng", relation='employee_skill_rel')
    project_capacity = fields.Float(string="Năng lực dự án (giờ/tuần)", default=40,
                                    help="Số giờ làm việc tối đa trên dự án mỗi tuần")
    allocated_hours = fields.Float(string="Giờ đã phân bổ", compute='_compute_allocated_hours', store=True)
    available_capacity = fields.Float(string="Năng lực còn trống", compute='_compute_available_capacity', store=True)

    # @api.depends('project_capacity')
    # @api.onchange('project_capacity')
    def _compute_allocated_hours(self):
        for employee in self:
            allocations = self.env['project.allocation'].search([('employee_id', '=', employee.id)])
            employee.allocated_hours = sum(allocations.mapped('allocated_hours'))

    # @api.depends('project_capacity', 'allocated_hours')
    @api.onchange('project_capacity', 'allocated_hour')
    def _compute_available_capacity(self):
        for employee in self:
            employee.available_capacity = max(0, employee.project_capacity - employee.allocated_hours)

    @api.constrains('project_capacity')
    def _check_project_capacity(self):
        for rec in self:
            if rec.project_capacity < 0:
                raise ValidationError("Năng lực dự án không được nhỏ hơn 0.")
