# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

{
	'name': "AZ Sedipualba",

	'summary': """
		Módulo para conectar a la API de Sedipualba""",

	'description': """
		Módulo para conectar a la API de Sedipualba
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
	'application': False,

    # any module necessary for this one to work correctly
	'depends': ['base'],
	'external_dependencies': {
		'python': ['xmltodict']
	},
    # always loaded
	'data': [
		'views/settings.xml',
	],
}
