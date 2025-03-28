from odoo import fields, models, api


class HREmployeeSkill(models.Model):
    _name = 'hr.employee.skill'
    _description = 'HR Employee Skill'

    name = fields.Char('Tên kỹ năng', required=True)
    category = fields.Selection([
        ('technical', 'Kỹ thuật'),
        ('soft', 'Kỹ năng mềm'),
        ('management', 'Quản lý')
    ], "Loại kỹ năng", required=True)
    level = fields.Selection([
        ('basic', 'Cơ bản'),
        ('intermediate', 'Trung bình'),
        ('advanced', 'Nâng cao'),
        ('expert', 'Chuyên gia')
    ], "Mức độ", required=True)

    _sql_constraints = [
        ('unique_skill', 'unique (name,category,level)', "Kỹ năng với loại và trình độ này đã tồn tại.")
    ]
