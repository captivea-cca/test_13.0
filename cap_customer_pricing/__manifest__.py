# -*- coding: utf-8 -*-
{
    'name': "Cap Client Pricing app",

    'summary': """
        Client pricing app and web page, estimates Odoo costs given
        by selected modules and number of users.""",

    'author': 'Captivea',
    'website': 'www.captivea.us',
    'version': '13.0.1.0.0',
    'category': 'Web',

    'application': True,

    'depends': ['base', 'website'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

}
