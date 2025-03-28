from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HREmployeeSkill(models.Model):
    _name = 'hr.employee.skill'
    _description = 'HR Employee Skills'

    name = fields.Char(string='Tên kỹ năng', required=True)
    skill_type = fields.Selection([
        ('technical', 'Kỹ thuật'),
        ('soft','Kỹ năng mềm'),
        ('language', 'Ngôn ngữ'),
    ], 'Loại kỹ năng', default='technical')

    level = fields.Selection([
        ('0', 'Cơ bản'),
        ('1', 'Trung bình'),
        ('2', 'Nâng cao'),
        ('3', 'Chuyên gia')
    ], 'Trình độ', default='1')

    years_of_experience = fields.Float('Số năm kinh nghiệm', compute='_compute_years_of_experience', store=True)

    @api.depends('level')
    def _compute_years_of_experience(self):
        experience_mapping = {
            '0': 0.5,
            '1': 1.0,
            '2': 2.0,
            '3': 3.0
        }
        for rec in self:
            rec.years_of_experience = experience_mapping.get(rec.level, 0)
