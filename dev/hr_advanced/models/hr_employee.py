from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HREmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    years_of_experience = fields.Float('Số năm kinh nghiệm', compute='_compute_years_of_experience', store=True)
    certification_ids = fields.Many2many(
        'hr.employee.certification',
        'employee_certification_rel',
        'employee_id',
        'certification_id',
        string='Chứng chỉ')
    certification_count = fields.Integer(compute='_compute_certification_count', string='Số chứng chỉ')
    skill_ids = fields.Many2many(
        'hr.employee.skill',
        'employee_skill_rel',
        'employee_id',
        'skill_id',
        string='Kỹ năng')
    skill_count = fields.Integer(compute='_compute_skill_count', string='Số kỹ năng')
    has_certification = fields.Boolean('Has certification', compute='_compute_has_certification')
    is_manager = fields.Boolean('Is manager', compute='_compute_is_manager')

    @api.depends('certification_ids', 'skill_ids')
    def _compute_years_of_experience(self):
        for rec in self:
            cert_years = sum(cert.years_of_experience for cert in rec.certification_ids)
            skill_years = sum(skill.years_of_experience for skill in rec.skill_ids)
            rec.years_of_experience = cert_years + skill_years

    def _compute_certification_count(self):
        for employee in self:
            employee.certification_count = len(employee.certification_ids) or 0

    def _compute_skill_count(self):
        for employee in self:
            employee.skill_count = len(employee.skill_ids) or 0

    @api.depends('certification_ids')
    def _compute_has_certification(self):
        for rec in self:
            rec.has_certification = bool(rec.certification_ids)

    def _compute_is_manager(self):
        for rec in self:
            rec.is_manager = (self.env.user.has_group('hr_advanced.group_hr_certification_manager') or
                            self.env.user.has_group('hr_advanced.group_hr_skill_manager'))

    def action_view_certifications(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Chứng chỉ nhân viên',
            'res_model': 'hr.employee.certification',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.certification_ids.ids)],
        }

    def action_view_skills(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Kỹ năng nhân viên',
            'res_model': 'hr.employee.skill',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.skill_ids.ids)],
        }
