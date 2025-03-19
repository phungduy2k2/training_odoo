{
    "name": "Student Management",
    "version": "16.0.1.0.0",
    "author": "duypv",
    "website": "https://www.duypv.com",
    "description": """
        Training Odoo module at AUM
    """,
    "summary": "Student management module",
    "category": "Website",
    "depends": ['base'],
    "data": [
        'security/ir.model.access.csv',

        'data/ir.sequence.xml',

        'views/student_student_view.xml',
        'views/res_partner_view.xml',
        'views/library_book_view.xml',
        'views/menus.xml'
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}