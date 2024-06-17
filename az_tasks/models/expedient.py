# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from odoo import api, fields, models

class expedient(models.Model):
	_inherit = ['az_expedients.expedient']

	tasks_ids = fields.One2many('az_tasks.task', 'expedient_id', string = 'Tareas')
