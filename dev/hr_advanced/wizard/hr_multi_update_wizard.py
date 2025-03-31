from odoo import models, fields, api
from odoo.exceptions import UserError


class HRMultiUpdateWizard(models.TransientModel):
    _name = 'hr.multi.update.wizard'
    _description = 'Employee Bulk Update Wizard'

    certification_ids = fields.Many2many(
        'hr.employee.certification',
        string='Chứng chỉ'
    )
    skill_ids = fields.Many2many(
        'hr.employee.skill',
        string='Kỹ năng'
    )

    @api.onchange('certification_ids')
    def _onchange_certification_ids(self):
        for rec in self:
            new_skills = rec.certification_ids.mapped('skill_ids')
            skills_to_remove = rec.skill_ids.filtered(
                lambda skill: skill.certification_id.id and skill.certification_id.id not in rec.certification_ids.ids)

            rec.skill_ids = rec.skill_ids + new_skills - skills_to_remove

    def action_update_employee_records(self):
        # Check quyền
        if not (self.env.user.has_group('hr_advanced.group_hr_certification_manager') or
                self.env.user.has_group('hr_advanced.group_hr_skill_manager')):
            raise UserError('Bạn không có quyền thực hiện thao tác này.')
        # Lấy các nv đc chọn
        active_ids = self.env.context.get('active_ids', [])
        employees = self.env['hr.employee'].browse(active_ids)

        # Lọc nv có exp < 5 năm, nếu có thì thông báo warning
        unable_employees = employees.filtered(lambda emp: emp.years_of_experience < 3)
        if unable_employees:
            unable_employees_name = ', '.join(unable_employees.mapped('name'))
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thông báo',
                    'type': 'danger',
                    'message': f"Nhân viên {unable_employees_name} chưa đủ điều kiện cập nhật.",
                    'sticky': True,
                    'next': {
                        'type': 'ir.actions.act_window_close'
                    }
                }
            }
        # Duyệt danh sách, thêm chứng chỉ/kỹ năng
        for employee in employees:
            new_certifications = self.certification_ids.filtered(
                lambda cert: cert.id not in employee.certification_ids.ids
            )
            employee.certification_ids |= new_certifications

            new_skills = self.skill_ids.filtered(
                lambda skill: skill.id not in employee.skill_ids.ids
            )
            employee.skill_ids |= new_skills
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thông báo',
                'type': 'success',
                'message': "Cập nhật hoàn tất.",
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window_close'
                }
            }
        }
