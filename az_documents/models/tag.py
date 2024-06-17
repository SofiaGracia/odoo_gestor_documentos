# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

import random
from odoo import models, fields

class tag(models.Model):
	_name = 'az_documents.tag'
	_description = 'Etiqueta'
	_sql_constraints = [("check_unique_name", "UNIQUE(name)", "The name must be unique")]

	name = fields.Char(string = 'Etiqueta', required = True)
	color = fields.Integer(string="Color Index")

	def create(self, values):
		values['color'] = random.randint(1, 11)

		return super(tag, self).create(values)
		