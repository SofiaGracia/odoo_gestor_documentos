# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import api, fields, models

class task(models.Model):
	_name = 'az_tasks.task'
	_description = 'Tarea'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char(string = 'Nombre', required = True, tracking = 1)
	state_id = fields.Many2one('az_tasks.statetask', string = 'Estado tarea', tracking = 1, group_expand='_group_expand_states')
	expedient_id = fields.Many2one('az_expedients.expedient', string = 'Expediente', tracking = 1)
	assigned_persons = fields.Many2many('res.partner', string = 'Asignados')
	description = fields.Text(string = 'Descripción', tracking = 1)
	
	message_id = fields.Char('Message ID')

	def _group_expand_states(self, states, domain, order):
		return self.env['az_tasks.statetask'].search([])
