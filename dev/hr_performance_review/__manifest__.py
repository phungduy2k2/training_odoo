{
    "name": "HR Performance Review",
    "version": "1.0",
    'category': 'Human Resources',
    'summary': "Manage employee performance reviews",
    'description': """
        This module allows managers to conduct and track employee performance reviews.
    """,
    'author': "Duypv",
    'depends': ['hr'],
    'data': [
        'security/hr_performance_review_security.xml',
        'security/ir.model.access.csv',

        'views/hr_performance_review_view.xml',
        'views/hr_employee_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}