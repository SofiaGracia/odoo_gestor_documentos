import os
from odoo import models, fields

# Tuve que crear esta clase heredada porque si relaciono el campo expediente_principal desde el modulo pau.documentos da un error de unknown_id


class Documentos(models.Model):  # Definir una clase de modelo en Odoo
    _name = "az_expedients.documentos"
    _inherit = "pau.documentos"
    
    expediente_principal = fields.Many2one(comodel_name="az_expedients.expedient", string='Expediente Principal')
    
    expedientes = fields.Many2many('az_expedients.expedient', 'documentos_expedientes_rela', 'documento_id', 'expediente_id', tracking = 1)
    
    interesados = fields.Many2many('res.partner', 'documentos_partners_rela', 'documento_id', 'partner_id', tracking = 1)
    
    creador = fields.Many2many('res.partner', 'documentos_creators_relacion', 'documento_id', 'partner_id', tracking = 1)
    
    documentos_relacionados = fields.Many2many('az_expedients.documentos', 'documentos_documentos_relacion', 'documento_id', 'documento_id2', tracking = 1)