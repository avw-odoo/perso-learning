# -*- coding: utf-8 -*-

{
    'name': 'Real Estate',
    'version': '0.1',
    'sequence': 1300,
    'depends': ['base', 'mail', 'crm'],
    'summary': 'Property management',
    'description': """
Real Estate management
======================

What am i doing here ?
---------------------

- I'm doing some odoo v9.0 (saas-11) modules for my personal learning purposes (as i'm not a developer...).
- You’ll certainly not find anything useful here, sorry for that... :-)

The first module "orealestate"
------------------------------

The goal of orealestate is « Real Estate management » basics.

- Property management (kind, areas surface, google map geolocalization...)
- Mandate (contract) management (based on opportunity (CRM) with specifics needs)
- Link to potential acquirers (based on opportunies (CRM)
- ...


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