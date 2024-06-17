# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

{
	'name': "AZ Padrón",

	'summary': """
		Módulo para gestionar el padrón municipal""",

	'description': """
		Módulo para gestionar el padrón municipal
	""",

	'author': "Rolan Benavent Talens",
	'website': "https://dulasoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
	'category': 'Administration',
	'version': '0.1',
	'license': 'OPL-1',
	'installable': True,
	'auto_install': False,
	'application': True,

    # any module necessary for this one to work correctly
	'depends': ['base', 'partner_external_map'],
    # always loaded
	'data': [
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/citizen.xml',
		'views/history.xml',
		'views/templates.xml',
		'views/menu.xml',
	],
    # only loaded in demonstration mode
	'demo': [
	],
}
