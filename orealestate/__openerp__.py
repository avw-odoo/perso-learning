# -*- coding: utf-8 -*-

{
    'name': 'Real Estate',
    'version': '0.1',
    'sequence': 1300,
    'depends': ['base', 'mail', 'crm'],
    'summary': 'Property management',
    'description': """
This will be a full-featured property management system.
========================================================

Pay attention, this is a continuous learning module used to test severals views
and Odoo capacities.

    """,

    'author': "Alain vdw",
    'license': 'LGPL-3',
    'website': "/",
    'category': 'Real Estate',

    'data': [
        'security/orealestate_security.xml',
        'security/ir.model.access.csv',
        'views/orealestate_views.xml',
        'data/orealestate_data.xml',
    ],

    'demo': [
        'demo/orealestate_demo.xml',
    ],

    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}