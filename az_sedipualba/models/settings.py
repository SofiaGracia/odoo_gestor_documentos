# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import api, fields, models

class settings(models.TransientModel):
	_inherit = 'res.config.settings'

	username = fields.Char(string = 'Usuario', config_parameter = 'az_sedipualba.username')
	password = fields.Char(string = 'Contraseña', config_parameter = 'az_sedipualba.password')
	entity = fields.Char(string = 'Entidad', config_parameter = 'az_sedipualba.entity')
	mode = fields.Boolean(string='Modo de pruebas', config_parameter = 'az_sedipualba.mode')