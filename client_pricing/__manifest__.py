# -*- coding: utf-8 -*-
{
    'name': "Client Pricing",

    'summary': """
        Client pricing app and web page, estimates Odoo costs given
        by selected modules and number of users.""",

    'author': "Chandler Calderon <chandler.calderon@captivea.com>",
    'website': "http://www.captivea.us",

    'category': 'Web',
    'version': '0.1',
    'application': True,

    'depends': ['base', 'website'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

}
