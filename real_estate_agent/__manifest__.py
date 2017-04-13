# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate Agent',
    'version': '0.1',
    'category': 'Real Estate',
    'sequence': 1000,
    'depends': ['base', 'mail'],
    'summary': 'Manage properties for sale as a Real Estate Agent.',
    'description': """
Manage properties for sale as a Real Estate Agent.
Details TBD
    """,
    'data': [
        'views/property_views.xml',
        'views/map_website_view.xml',
        'data/map_website_data.xml',
        'views/res_users_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'post_init_hook': 'set_default_map_settings',
    'installable': True,
    'application': True,
}    