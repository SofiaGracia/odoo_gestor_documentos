# -*- coding: utf-8 -*-

import os
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class gestoDocumentos(models.Model):
    _name = 'pau.documentos'  # Nombre técnico del modelo en Odoo
    _description = 'gestor'  # Descripción del modelo
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Definición de campos del modelo
    # Campo calculado para el nombre del documento
    name = fields.Char(string='Nombre del Documento', compute='_compute_name', store=True, tracking = 1)
    
    # Campo para el código de actividad (requerido, tamaño 3)
    codigoActividad = fields.Char(string='Codigo de la actividad', size=3, required=True, tracking = 1)
    
    # Campo para el ejercicio (requerido, tamaño 2)
    ejercicio = fields.Char(string='Ejercicio', size=2, required=True, tracking = 1)
    
    # Campo para el número de expediente (requerido, tamaño 4)
    numeroExpediente = fields.Char(string='Número de Expediente', size=4, required=True, tracking = 1)
    
    # Campo para el núm. orden del documento en el expediente (requerido, tamaño 3)
    numOrdenDocEnExp = fields.Char(string='Núm. orden del documento en el expediente', size=3, required=True, tracking = 1)
    
    # Campo para la abreviatura del tipo de documento (requerido, tamaño 2)
    abreviaturaTipoDocumento = fields.Char(string='Abreviatura del tipo de documento', size=2, required=True, tracking = 1)
    
    # Campo para el título (requerido, tamaño máximo 70)
    titulo = fields.Char(string='Titulo', size=70, required=True, tracking = 1)
    
    # Campo para la extensión del documento
    tipo_archivo = fields.Char(string='Tipo de Archivo', tracking = 1)
    
    # Campo para el nombre del documento
    nombre_archivo = fields.Char(string='Nombre del Archivo', tracking = 1)
    
    # Campo para la URL del documento
    file_url = fields.Char(string='URL del Fichero', tracking = 1)
    
    # Campo para la descripción del documento
    description = fields.Text(string='Descripción', tracking = 1)
    
    # Relación con el modelo 'az_expedients.expedient', no funciona, necesario heredar en el modulo de expedientes
    expediente_principal = fields.Many2one(comodel_name="az_expedients.expedient", string='Expediente Principal')
    
    # Relación con el modelo 'az_expedients.expedient'
    expedientes = fields.Many2many('az_expedients.expedient', 'documentos_expedientes_rel', 'documento_id', 'expediente_id', string='Expedientes', tracking = 1)
    
    # Relación con el modelo 'pau.codigos' para el codigo del documento
    codigo = fields.Many2one('pau.codigos', string='Codigo', tracking = 1)
    
    # Relación con el modelo 'res.partner' para la lista de interesados
    interesados = fields.Many2many('res.partner', 'documentos_partners_rel', 'documento_id', 'partner_id', string='Lista de interesados', tracking = 1)
    
    # Campo para almacenar temporalmente el documento
    documento_file = fields.Binary(string='Archivo', tracking = 1)
    
    message_id = fields.Char('Message ID')
    
    # Método para obtener el nombre del documento
    @api.depends('numeroExpediente', 'codigoActividad', 'ejercicio', 'titulo','numOrdenDocEnExp','abreviaturaTipoDocumento')
    def _compute_name(self):
        for documento in self:
            name = f"{documento.codigoActividad}{documento.ejercicio}{documento.numeroExpediente}.{documento.numOrdenDocEnExp}.{documento.abreviaturaTipoDocumento}.{documento.titulo}.{documento.tipo_archivo}"
            documento.name = name
            
    # Validación de longitud de campos
    @api.constrains('codigoActividad', 'ejercicio', 'numeroExpediente', 'titulo','numOrdenDocEnExp','abreviaturaTipoDocumento')
    def _check_field_lengths(self):
        for documento in self:
            if len(documento.codigoActividad) != 3:
                raise ValidationError("El campo 'Codigo de la actividad' debe tener exactamente 3 caracteres.")
            if len(documento.ejercicio) != 2:
                raise ValidationError("El campo 'Ejercicio' debe tener exactamente 2 caracteres.")
            if len(documento.numeroExpediente) != 4:
                raise ValidationError("El campo 'Número de Expediente' debe tener exactamente 4 caracteres.")
            if len(documento.numOrdenDocEnExp) != 3:
                raise ValidationError("El campo 'Núm. orden del documento en el expediente' debe tener exactamente 3 caracteres.")
            if len(documento.abreviaturaTipoDocumento) != 2:
                raise ValidationError("El campo 'Abreviatura del tipo de documento' debe tener exactamente 2 caracteres.")
            if len(documento.titulo) > 70:
                raise ValidationError("El campo 'Titulo' no debe tener más de 70 caracteres.")

    
    
    @api.onchange('documento_file')   
    def buscar_archivo_local(self):
        for record in self:
            if record.documento_file:
                # Nombre del archivo cargado
                nombre_archivo = record.nombre_archivo
                
                # Dividir el nombre del archivo usando '.' como separador
                parts = nombre_archivo.split('.')

                if len(parts) >= 5:
                    # Extraer el primer segmento 'AAAYYNNNN'
                    base = parts[0]
                    if len(base) == 9:
                        record.codigoActividad = base[:3]  # 'AAA'
                        record.ejercicio = base[3:5]       # 'YY'
                        record.numeroExpediente = base[5:] # 'NNNN'

                        # Extraer 'nnn' - Número de orden del documento en el expediente
                        record.numOrdenDocEnExp = parts[1] if len(parts[1]) == 3 else ''

                        # Extraer 'TD' - Abreviatura del tipo de documento
                        record.abreviaturaTipoDocumento = parts[2] if len(parts[2]) <= 2 else ''

                        # Extraer 'título' - Título del documento
                        # Unir las partes restantes excepto la última parte para la extensión
                        titulo = '.'.join(parts[3:-1])
                        record.titulo = titulo if len(titulo) <= 70 else titulo[:70]

                        # Extraer la extensión del archivo de la última parte
                        record.tipo_archivo = parts[-1]
                
                # Directorio donde buscar (sustituir por la ruta del NAS)
                directorio = '/opt/odoo/'
                
                # Recorre todos los archivos en el directorio
                for directorio_actual, subdirectorios, archivos in os.walk(directorio):
                    # Comprobar si el nombre del archivo coincide con alguno de los archivos encontrados
                    if nombre_archivo in archivos:
                        # Construir la ruta completa del archivo encontrado
                        ruta_archivo = os.path.join(directorio_actual, nombre_archivo)
                        
                        # Asociar la URL del archivo encontrado al registro actual
                        record.file_url = ruta_archivo
                        
                        # Eliminar el documento almacenado en Odoo
                        record.documento_file = None
                        return
                raise ValidationError('No se encontró ningún archivo local que coincida con el archivo proporcionado.')
            
            
    def action_preview_document(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/documentos/preview/{}'.format(self.nombre_archivo),
            'target': 'new',
        }

    def action_view_full_document(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/documentos/full/{}'.format(self.nombre_archivo),
            'target': 'new',
        }

    def action_download_document(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/documentos/download/{}'.format(self.nombre_archivo),
            'target': 'self',
        }