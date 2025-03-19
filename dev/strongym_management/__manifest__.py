{
    "name": "Strongym Management",
    "version": "16.0.1.0.0",
    "author": "duypv",
    "website": "https://www.duypv.com",
    "description": """
        StronGym information management module
    """,
    "summary": "Strongym management module",
    "category": "Website",
    "depends": ['base', 'mail'],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/strongym_member_view.xml',
        'views/strongym_membership_plan_view.xml',
        'views/strongym_employee_view.xml',
        'views/menus.xml',
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}