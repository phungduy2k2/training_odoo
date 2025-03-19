{
    "name": "Real Estate",
    "version": "1.0",
    "author": "duypv",
    "website": "https://www.duypv.com",
    "description": """
        Real Estate module to show available properties
    """,
    "category": "Sales",
    "depends": ["base", "mail", "website"],
    "data": [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/model_access.xml',
        'security/ir_rule.xml',

        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/property_offer_view.xml',
        'views/menus.xml',

        # data files
        'data/property_type.xml',
        'data/mail_template.xml',

        # report files
        'report/report_template.xml',
        'report/property_report.xml',
    ],
    # "demo": [
    #     'demo/property_tag.xml'
    # ],
    'assets': {
        'web.assets_backend': [
            'real_estate_ads/static/src/js/my_custom_tag.js',
            'real_estate_ads/static/src/xml/my_custom_tag.xml',
        ]
    },
    "license": "LGPL-3",
    "application": True,
    "installable": True
}