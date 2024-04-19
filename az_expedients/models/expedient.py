# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import api, fields, models

class expedient(models.Model):
	_name = 'az_expedients.expedient'
	_description = 'Expediente'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char(string = 'Nombre', required = True, tracking = 1)
	name_gtt = fields.Char(string = 'Nombre GTT', tracking = 1)
	name_sedipualba = fields.Char(string = 'Nombre Sedipualba', tracking = 1)
	code = fields.Char(string = 'Código', required = True, tracking = 1)
	reference = fields.Char(string = 'Referencia interna', tracking = 1)
	parent_expedient_id = fields.Many2one('az_expedients.expedient', string = 'Expediente padre', tracking = 1)
	init_person = fields.Many2one('res.partner', string = 'Persona iniciadora', tracking = 1)
	registration_date = fields.Date(string = 'Fecha creación', tracking = 1)
	closing_date = fields.Date(string = 'Fecha cierre', tracking = 1)
	type_id = fields.Many2one('az_expedients.etype', string = 'Tipo', tracking = 1, group_expand='_group_expand_types')
	color = fields.Integer(related = 'type_id.color')
	state_id = fields.Many2one('az_expedients.state', string = 'Estado', tracking = 1, group_expand='_group_expand_states')
	department_id = fields.Many2one('hr.department', string = 'Departamento gestor', tracking = 1, group_expand='_group_expand_department')
	processing_person = fields.Many2one('res.partner', string = 'Persona tramitadora', tracking = 1)
	description = fields.Text(string = 'Descripción', tracking = 1)
	observations = fields.Text(string = 'Observaciones', tracking = 1)
	interested_persons = fields.Many2many('res.partner', string = 'Interesados')
	codigos = fields.One2many('az_expedients.documentos', 'expediente_principal', string = 'Documentos')
	tasks_ids = fields.One2many('az_expedients.task', 'expedient_id', string = 'Tareas')

	message_id = fields.Char('Message ID')
 
	documents_ids2 = fields.Many2many('az_expedients.documentos', 'documentos_expedientes_rel', 'expediente_id', 'documento_id', string = 'Documentos')

	def _group_expand_types(self, states, domain, order):
		return self.env['az_expedients.etype'].search([])

	def _group_expand_states(self, states, domain, order):
		return self.env['az_expedients.state'].search([])

	def _group_expand_department(self, states, domain, order):
		return self.env['hr.department'].search([])