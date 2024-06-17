# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.addons.az_sedipualba.models.sedipualba import Sedipualba

class expedient(models.Model):
	_name = 'az_expedients.expedient'
	_description = 'Expediente'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char(string = 'Nombre', required = True, tracking = 1)
	name_gtt = fields.Char(string = 'Nombre GTT', tracking = 1)
	name_sedipualba = fields.Char(string = 'Nombre Sedipualba', tracking = 1)
	code = fields.Char(string = 'Código', required = True, tracking = 1)
	code_sedipualba = fields.Char(string = 'Código Sedipualba', tracking = 1)
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

	message_id = fields.Char('Message ID')

	def _group_expand_types(self, states, domain, order):
		return self.env['az_expedients.etype'].search([])

	def _group_expand_states(self, states, domain, order):
		return self.env['az_expedients.state'].search([], order='sedipualba_id asc')

	def _group_expand_department(self, states, domain, order):
		return self.env['hr.department'].search([])

	@api.onchange('code_sedipualba')
	def _onchange_code_sedipualba(self):
		get_param = self.env['ir.config_parameter'].sudo().get_param

		sedi = Sedipualba(
			get_param('az_sedipualba.username'),
			get_param('az_sedipualba.password'),
			get_param('az_sedipualba.entity'),
			get_param('az_sedipualba.mode')
		)

		for res in self:
			if res.code_sedipualba:
				data = sedi.ObtenerInfoExpedienteV2(api = 'segex', 
					params = {'codigoExpediente': res.code_sedipualba}, 
					mapParams = {
						'name_sedipualba': 'NombreProcedimiento',
						'reference': 'ReferenciaInterna',
						'description': 'Descripcion',
						'code': 'CodigoProcedimiento',
						'department_id': 'DescripcionTramitador',
						'init_person': 'DescripcionIniciador',
						'state_id': 'DescripcionEstado',
						'type_id': 'CodigoSubtipo',
						'registration_date': 'FechaCreacion',
						'closing_date': 'FechaFinalizacion',
				})
				if data['result'] == 'ok' and len(data['data']) > 0:
					searchState = self.env['az_expedients.state'].search([('name', '=', data['data']['state_id'])])
					for state in searchState:
						data['data']['state_id'] = state
						break
					searchType = self.env['az_expedients.etype'].search([('sedipualba_id', '=', data['data']['type_id'])])
					for etype in searchType:
						data['data']['type_id'] = etype
						break

					for field, value in data['data'].items():
						try:
							res[field] = value if value else res[field]
						except:
							pass
					if not res.name:
						res.name = res.name_sedipualba
					if not res.init_person:
						if self.env['res.partner'].search_count([('name', '=', data['data']['init_person'])]) > 0:
							searchPerson = self.env['res.partner'].search([('name', '=', data['data']['init_person'])])
							for person in searchPerson:
								res.init_person = person
								break
						else:
							person_id = self.env['res.partner'].create({'name': data['data']['init_person']})
							res.init_person = person_id
					
					intPersons = sedi.ListarInteresadosExpedienteV3(api = 'segex', 
						params = {'codigoExpediente': res.code_sedipualba},
					)
					if intPersons['result'] == 'ok' and len(intPersons['data']) > 0:
						persons = []
						for person in intPersons['data']:
							if self.env['res.partner'].search_count([('name', '=', person)]) > 0:
								searchPerson = self.env['res.partner'].search([('name', '=', person)])
								for iperson in searchPerson:
									persons.append( iperson )
									break
							else:
								person_id = self.env['res.partner'].create({'name': person})
								persons.append( person_id )
						res.interested_persons = persons

	
	def write(self, values):
		get_param = self.env['ir.config_parameter'].sudo().get_param

		sedi = Sedipualba(
			get_param('az_sedipualba.username'),
			get_param('az_sedipualba.password'),
			get_param('az_sedipualba.entity'),
			get_param('az_sedipualba.mode')
		)

		for res in self:
			if res.code_sedipualba:
				code_sedipualba = values.get('code_sedipualba') if values.get('code_sedipualba') else res.code_sedipualba
				if values.get('description') and res.description != values.get('description'):
					result = sedi.CambiarDescripcionExpediente(api = 'segex', 
						params = {'codigoExpediente': code_sedipualba, 'descripcion': values.get('description')})

				if values.get('state_id') and res.state_id != values.get('state_id'):
					searchState = self.env['az_expedients.state'].search_read([('id', '=', values.get('state_id'))])
					for state in searchState:
						result = sedi.CambiarEstadoExpediente(api = 'segex', 
							params = {'codigoExpediente': code_sedipualba, 'pk_estado': state['sedipualba_id']})
			else:
				result = sedi.NuevoExpedienteV3(api = 'segex',
							params = {''})
		return super(expedient, self).write( values )