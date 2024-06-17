# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import models, fields

class statetask(models.Model):
	_name = 'az_tasks.statetask'
	_description = 'Estado tarea'
	_sql_constraints = [("check_unique_name", "UNIQUE(name)", "The name must be unique")]

	name = fields.Char(string = 'Nombre', required = True)
	description = fields.Text(string = 'Descripción')
