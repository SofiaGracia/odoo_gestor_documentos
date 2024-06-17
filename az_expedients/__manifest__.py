# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

{
	'name': "AZ Expedientes",

	'summary': """
		Módulo para la gestión de expedientes""",

	'description': """
		Módulo para la gestión de expedientes
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
	'depends': ['base', 'hr', 'az_sedipualba'],
	'external_dependencies': {
		'python': ['xmltodict']
	},
    # always loaded
	'data': [
		'security/ir.model.access.csv',
		'views/expedient.xml',
		'views/etype.xml',
		'views/state.xml',
		'views/templates.xml',
		'views/menu.xml',
		'data/etype.xml',
		'data/state.xml',
	],
    # only loaded in demonstration mode
	'demo': [
		'demo/demo.xml',
	],
}
