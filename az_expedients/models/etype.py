# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import models, fields

class etype(models.Model):
	_name = 'az_expedients.etype'
	_description = 'Tipo'
	_sql_constraints = [("check_unique_name", "UNIQUE(name)", "The name must be unique")]

	name = fields.Char(string = 'Nombre', required = True)
	color = fields.Integer(string = 'Color')
	description = fields.Text(string = 'Descripción')
