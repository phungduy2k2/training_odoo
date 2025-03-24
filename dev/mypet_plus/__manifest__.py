{
    'name': "My pet (+) - duypv",
    'summary': """My pet plus""",
    'description': """Managing pet information""",
    'author': "duypv",
    'website': "https://www.facebook.com/duy.phungvan.3152130/",
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': [
        'mypet',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/my_pet_plus_view.xml',
        'views/super_pet_view.xml',
        'views/product_pet_view.xml',
    ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}