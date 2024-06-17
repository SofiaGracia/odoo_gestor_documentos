# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import models, fields

class etype(models.Model):
	_name = 'az_expedients.etype'
	_description = 'Tipo'
	_sql_constraints = [
		("check_unique_name", "UNIQUE(name)", "The name must be unique"), 
		("check_unique_sedipualba_id", "UNIQUE(sedipualba_id)", "The sedipualba_id must be unique")
	]

	name = fields.Char(string = 'Nombre', required = True)
	sedipualba_id = fields.Integer(string = 'Id Sedipualba')
	color = fields.Integer(string = 'Color')
	description = fields.Text(string = 'Descripción')
