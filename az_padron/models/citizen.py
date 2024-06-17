# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class citizen(models.Model):
	_inherit = ['res.partner']

	passport = fields.Char(string = 'Pasaporte')
	birthday = fields.Date(string = 'Fecha nacimiento')
	is_padron = fields.Boolean(string = 'Es padrón')
	id_ph = fields.Char(string = 'Id Padrón')
	parents = fields.Char(string = 'Padres')
	comments = fields.Text(string = 'Observaciones')
	active_ph = fields.Boolean(string = 'Activo en padrón')
	citizen_ids = fields.Many2many('res.partner', string = 'Habitantes misma dirección', store = False, compute = '_compute_citizen_ids')
	age = fields.Char(string = 'Edad', store = False, compute = '_compute_age')
	total_views = fields.Integer(string = 'Consultas')
	comp_views = fields.Integer(string = 'Consultas', store = False, compute = '_compute_total_views')
	
	@api.depends('street')
	def _compute_citizen_ids(self):
		for res in self:
			if res.street and res.id:
				res.citizen_ids = self.env['res.partner'].search([('street', '!=', ''), ('street', '=', res.street), ('id', '!=', res.id), ('is_padron', '=', True)])
			else:
				res.citizen_ids = []
	
	@api.depends('birthday')
	def _compute_age(self):
		now = date.today()
		for res in self:
			res.age = '-'
			if(res.birthday != False):
				res.age = relativedelta(now, res.birthday).years

	def _compute_total_views(self):
		now = datetime.today()
		for res in self:
			res.comp_views = self.env['az_padron.history'].search_count([('citizen_id', '=', res.id)]) + 1
			res.total_views = res.comp_views
			self.env['az_padron.history'].create({'citizen_id': res.id, 'user_id': self.env.user.id, 'date_view': now})
