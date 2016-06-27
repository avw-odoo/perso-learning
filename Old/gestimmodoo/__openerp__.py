# -*- coding: utf-8 -*-
{
    'name': "gestimmodoo",

    'summary': """
        Properties management.

        """,

    'description': """
        Pay attention, this is a learning module used to test severals views
        and Odoo capacities.

    """,

    'author': "Alain vdw",
    'website': "/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Real estate',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','crm','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/data_partner_category.xml',
        'views/templates.xml',
        'data/website_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/icon.png'],
}
