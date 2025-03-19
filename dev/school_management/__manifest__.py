# -*- coding: utf-8 -*-
{
    'name': 'School Management',

    'summary': """School Management Software""",
    'description': """
        Treating Schools
    """,
    'author': 'duypv',
    'website': 'https://github.com/duypv',

    'category': 'Tools',
    'version': '16.0.1.0.0',

    'depends': ['base', 'contacts', 'hr', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/school.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'school_management/static/src/js/test.js',
        ],
    },

    'demo': [

    ],
    'images': ['static/description/icon.png'],
    "application": True,
    "installable": True,
    "auto_install": False
}