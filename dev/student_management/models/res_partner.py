from odoo import fields,models,api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean("Là sinh viên")
    student_id = fields.Many2one('student.student', string='Sinh viên')
