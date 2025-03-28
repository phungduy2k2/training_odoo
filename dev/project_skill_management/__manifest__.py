{
    'name': 'Project Skill Management',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Quản lý kỹ năng và phân bổ nhân sự cho dự án',
    'description': """
        Môđun giúp quản lý kỹ năng và phân bổ nhân sự cho các dự án
    """,
    'author': 'Duypv',
    'website': '',
    'depends': ['hr','project'],
    'data': [
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_skill_view.xml',
        'views/hr_employee_view.xml',
        'views/project_allocation_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
