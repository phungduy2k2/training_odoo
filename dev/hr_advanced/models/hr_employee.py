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
    skill_ids = fields.Many2many(
        'hr.employee.skill',
        'employee_skill_rel',
        'employee_id',
        'skill_id',
        string='Kỹ năng')

    @api.depends('certification_ids', 'skill_ids')
    def _compute_years_of_experience(self):
        for rec in self:
            cert_years = sum(cert.years_of_experience for cert in rec.certification_ids)
            skill_years = sum(skill.years_of_experience for skill in rec.skill_ids)
            rec.years_of_experience = cert_years + skill_years

    def action_view_certifications(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Chứng chỉ nhân viên',
            'res_model': 'hr.employee.certification',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'default_employee_id': self.id
            }
        }

    def action_view_skills(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Kỹ năng nhân viên',
            'res_model': 'hr.employee.skill',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'default_employee_id': self.id
            }
        }
