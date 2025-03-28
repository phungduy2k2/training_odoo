from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HREmployeeCertification(models.Model):
    _name = 'hr.employee.certification'
    _description = 'Employee Certification'

    name = fields.Char('Tên chứng chỉ', required=True)
    issuring_organization = fields.Char('Tổ chức phát hành')
    issue_date = fields.Date('Ngày phát hành')
    expiration_date = fields.Date('Ngày hết hạn')

    years_of_experience = fields.Float('Số năm kinh nghiệm', compute='_compute_years_of_experience', store=True)

    @api.depends('issue_date', 'expiration_date')
    def _compute_years_of_experience(self):
        for rec in self:
            if rec.issue_date and rec.expiration_date:
                years = rec.expiration_date.year - rec.issue_date.year
                rec.years_of_experience = max(0.5, min(years, 3.0))
            else:
                rec.years_of_experience = 0.5

    @api.constrains('issue_date', 'expiration_date')
    def _check_date(self):
        for rec in self:
            if rec.issue_date and rec.expiration_date:
                if rec.issue_date > rec.expiration_date:
                    raise ValidationError("Ngày phát hành phải trước ngày hết hạn.")
