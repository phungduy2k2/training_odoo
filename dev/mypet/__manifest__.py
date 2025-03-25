{
    'name': "My pet - duypv",
    'version': "1.0",
    'summary': "My pet module",
    'description': """Managing pet information""",
    'author': "Duypv",
    'website': "https://www.facebook.com/duy.phungvan.3152130/",
    'category': "Uncategorized",
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',

        'views/my_pet_view.xml',

        'wizard/batch_update.xml',
        'views/res_config_settings_view.xml'
    ],
    'installable': True,
    'application': True
}
