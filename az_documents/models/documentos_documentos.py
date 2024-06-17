# -*- coding: utf-8 -*-

import os
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Documentos(models.Model):
    _name = 'az_documents.document'  # Nombre técnico del modelo en Odoo
    _description = 'gestor'  # Descripción del modelo
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Definición de campos del modelo
    # Campo calculado para el nombre del documento
    name = fields.Char(compute='_compute_name', store=True, tracking = 1)
    
    # Campo para el código de actividad (requerido, tamaño 3)
    codigoActividad = fields.Char(size=3, required=True, tracking = 1)
    
    # Campo para el ejercicio (requerido, tamaño 2)
    ejercicio = fields.Char(size=2, required=True, tracking = 1)
    
    # Campo para el número de expediente (requerido, tamaño 4)
    numeroExpediente = fields.Char(size=4, required=True, tracking = 1)
    
    # Campo para el núm. orden del documento en el expediente (requerido, tamaño 3)
    numOrdenDocEnExp = fields.Char(size=3, required=True, tracking = 1)
    
    # Campo para la abreviatura del tipo de documento (requerido, tamaño 2)
    abreviaturaTipoDocumento = fields.Char(size=2, required=True, tracking = 1)
    
    # Campo para el título (requerido, tamaño máximo 70)
    titulo = fields.Char(size=70, required=True, tracking = 1, )
    
    # Campo para la extensión del documento
    tipo_archivo = fields.Char(tracking = 1)
    
    # Campo para el nombre del documento
    nombre_archivo = fields.Char()
    
    # Campo para la URL del documento
    file_url = fields.Char(tracking = 1)
    
    # Campo para la descripción del documento
    description = fields.Text(tracking = 1)
    
    alcance = fields.Text('Alcance y contenido del documento')
    
    # Relación con el modelo 'az_expedients.expedient', no funciona, necesario heredar en el modulo de expedientes
    expedient_id = fields.Many2one('az_expedients.expedient')
    
    # Relación con el modelo 'az_expedients.expedient'
    expedientes = fields.Many2many('az_expedients.expedient', 'documentos_expedientes_rel', 'documento_id', 'expediente_id', tracking = 1)
    
    # Relación con el modelo 'pau.codigos' para el codigo del documento
    # codigo = fields.Many2one('pau.codigos', tracking = 1, string="Código del documento")
    
    # Relación con el modelo 'res.partner' para la lista de interesados
    interesados = fields.Many2many('res.partner', 'documentos_partners_rel', 'documento_id', 'partner_id', tracking = 1)
    
    # Campo para almacenar temporalmente el documento
    documento_file = fields.Binary(tracking = 1)
    
    message_id = fields.Char('Message ID')
    
    registration_date = fields.Date(tracking = 1) # (ISAD(G))
    
    register = fields.Many2one('res.partner')
    
    notas_adicionales = fields.Text(tracking = 1)
    
    documentos_relacionados = fields.Many2one('az_documents.document')

    tag_ids = fields.Many2many('az_documents.tag', string="Etiqueta")
    
    # biografica/historia administrativa: no se que hacer aqui de momento (ISAD(G))
    
    # Proceso de descripción del documento: Esto lo tenemos implementado en odoo, pero si queremos migrarlo en algun momento posterior igual deberia hacerse un log que guarde los cambios del documento
    
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

                if len(parts) >= 4:
                    # Extraer el primer segmento 'AAAYYNNNN'
                    base = parts[0]
                    record.codigoActividad = base[:3]  # 'AAA'
                    record.ejercicio = base[3:5]       # 'YY'
                    record.numeroExpediente = base[5:] # 'NNNN'

                    # Extraer 'nnn' - Número de orden del documento en el expediente
                    record.numOrdenDocEnExp = parts[1]

                    # Extraer 'TD' - Abreviatura del tipo de documento
                    record.abreviaturaTipoDocumento = parts[2] if len(parts[2]) <= 2 else ''

                    # Extraer 'título' - Título del documento
                    # Unir las partes restantes excepto la última parte para la extensión
                    titulo = '.'.join(parts[3:-1])
                    record.titulo = titulo if len(titulo) <= 70 else titulo[:70]

                    # Extraer la extensión del archivo de la última parte
                    record.tipo_archivo = parts[-1]
                
                # Directorio donde buscar (sustituir por la ruta del NAS)
                directorio = '/mnt/'
                
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
        
        if self.file_url and self.name:
            return {
                'type': 'ir.actions.act_url',
                'url': '/documentos/preview/{}'.format(self.name),
                'target': 'new',
            }
        else:
            raise ValidationError('No ha proporcionado una url o nombre validos')

    def action_view_full_document(self):
        if self.file_url and self.name:
            return {
                'type': 'ir.actions.act_url',
                'url': '/documentos/full/{}'.format(self.name),
                'target': 'new',
            }
        else:
            raise ValidationError('No ha proporcionado una url o nombre validos')

    def action_download_document(self):
        if self.file_url and self.name:
            return {
                'type': 'ir.actions.act_url',
                'url': '/documentos/download/{}'.format(self.name),
                'target': 'self',
            }
        else:
            raise ValidationError('No ha proporcionado una url o nombre validos')