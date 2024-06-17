# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import models, fields

class state(models.Model):
	_name = 'az_expedients.state'
	_description = 'Estado'
	_sql_constraints = [
		("check_unique_name", "UNIQUE(name)", "The name must be unique"),
		("check_unique_sedipualba_id", "UNIQUE(sedipualba_id)", "The sedipualba_id must be unique")
		]

	sedipualba_id = fields.Integer(string = 'Id Sedipualba', required = True)
	name = fields.Char(string = 'Nombre', required = True)
	description = fields.Text(string = 'Descripción')
