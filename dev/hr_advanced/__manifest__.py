{
    "name": "HR Advanced Management",
    "version": "1.0",
    "author": "Duypv",
    "category": "Human Resources",
    "summary": "Advanced HR Employee Management System",
    "description": """
        Mở rộng module HR với nhiều tính năng nâng cao
    """,
    "depends": ['hr'],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/hr_employee_inherit_view.xml',
        'views/hr_employee_certification_view.xml',
        # 'views/hr_employee_skill_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
