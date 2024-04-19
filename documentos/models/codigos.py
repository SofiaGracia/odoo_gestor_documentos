import re  # Importar el módulo para operaciones de expresiones regulares
from odoo import models, fields, api  # Importar los módulos necesarios de Odoo

class Codigos(models.Model):  # Definir una clase de modelo en Odoo
    _name = 'pau.codigos'  # Nombre técnico del modelo en Odoo
    _description = 'Codigos para expedientes y documentos'  # Descripción del modelo
    
    # Definir campos del modelo
    name = fields.Char(string='Codigo', size=3, required=True)  # Campo para el código (requerido, tamaño 3)
    descripcion = fields.Text(string='Descripcion del codigo', required=True)  # Campo para la descripción del código (requerido)
    
    # Restricción para verificar que el campo 'name' solo tiene 3 numeros o/y letras en mayusculas
    @api.constrains('name')
    def _check_name_format(self):
        for record in self:
            if not re.match("^[A-Z0-9]{3}$", record.name):
                raise models.ValidationError("El código debe tener exactamente tres caracteres y solo aceptar números y letras mayúsculas.")
                # Generar un error de validación si el formato no coincide
