import os
from odoo import models, fields

# Tuve que crear esta clase heredada porque si relaciono el campo expediente_principal desde el modulo pau.documentos da un error de unknown_id


class Documentos(models.Model):  # Definir una clase de modelo en Odoo
    _name = "az_expedients.documentos"
    _inherit = "pau.documentos"
    
    expediente_principal = fields.Many2one(comodel_name="az_expedients.expedient", string='Expediente Principal')
    
    expedientes = fields.Many2many('az_expedients.expedient', 'documentos_expedientes_rela', 'documento_id', 'expediente_id', string='Expedientes', tracking = 1)
    
    interesados = fields.Many2many('res.partner', 'documentos_partners_rela', 'documento_id', 'partner_id', string='Lista de interesados', tracking = 1)