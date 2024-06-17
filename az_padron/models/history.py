# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import models, fields, api

class history(models.Model):
	_name = 'az_padron.history'
	_description = 'Ciudadano'

	citizen_id = fields.Many2one('res.partner', string = 'Ciudadano')
	user_id = fields.Many2one('res.users', string = 'Usuario')
	date_view = fields.Datetime(string = 'Fecha consulta')