from odoo import http
from odoo.http import request, content_disposition
import os
from pdfrw import PdfReader, PdfWriter
from io import BytesIO
import subprocess

class DocumentoPDFController(http.Controller):

    @http.route(['/documentos/preview/<string:name>'], type='http', auth="user")
    def ver_primera_pagina_pdf(self, name, **kw):
        documento = request.env['az_expedients.documentos'].sudo().search([('name', '=', name)], limit=1)
        if not documento:
            return request.not_found()
        # Aquí asumimos que 'file_url' es una ruta absoluta al archivo en el servidor
        ruta_archivo = documento.file_url
        tipo_archivo = documento.tipo_archivo
        nombre_archivo = documento.name
        
        
        if tipo_archivo == "pdf":
            if os.path.exists(ruta_archivo):
                reader = PdfReader(ruta_archivo)
                writer = PdfWriter()

                # Asumiendo que el PDF tiene al menos una página
                if len(reader.pages) > 0:
                    writer.addpage(reader.pages[0])

                    # Crear un PDF temporal en memoria
                    pdf_temporal = BytesIO()
                    writer.write(pdf_temporal)
                    pdf_temporal.seek(0)

                    headers = [
                        ('Content-Type', 'application/pdf'),
                        ('Content-Disposition', 'inline; filename="Primera_pagina_%s"' % documento.name)
                    ]
                    return request.make_response(pdf_temporal.getvalue(), headers)
            return request.not_found()
        elif tipo_archivo == "odt" or tipo_archivo == "ods":
            
            nombre_archivo_base, extension = os.path.splitext(nombre_archivo)
            
            subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", ruta_archivo, "--outdir", "/tmp"])

            ruta_archivo_pdf = os.path.join("/tmp/", nombre_archivo_base + ".pdf")

            if os.path.exists(ruta_archivo_pdf):
                reader = PdfReader(ruta_archivo_pdf)
                writer = PdfWriter()
                
                if len(reader.pages) > 0:
                    writer.addpage(reader.pages[0])
                
                    # Crear un PDF temporal en memoria
                    pdf_temporal = BytesIO()
                    writer.write(pdf_temporal)
                    pdf_temporal.seek(0)

                    headers = [
                        ('Content-Type', 'application/pdf'),
                        ('Content-Disposition', 'inline; filename="Primera_pagina_%s"' % documento.name)
                    ]
                    return request.make_response(pdf_temporal.getvalue(), headers)
            return request.not_found()

    @http.route(['/documentos/full/<string:name>'], type='http', auth="user")
    def ver_pagina_pdf(self, name, **kw):
        documento = request.env['az_expedients.documentos'].sudo().search([('name', '=', name)], limit=1)
        if not documento:
            return request.not_found()
        # Aquí asumimos que 'file_url' es una ruta absoluta al archivo en el servidor
        ruta_archivo = documento.file_url
        tipo_archivo = documento.tipo_archivo
        nombre_archivo = documento.name
        
        
        if tipo_archivo == "pdf":
            if os.path.exists(ruta_archivo):
                reader = PdfReader(ruta_archivo)
                writer = PdfWriter()

                # Add all pages to the writer
                for page in reader.pages:
                    writer.addpage(page)

                pdf_temporal = BytesIO()
                writer.write(pdf_temporal)
                pdf_temporal.seek(0)

                headers = [
                    ('Content-Type', 'application/pdf'),
                    ('Content-Disposition', f'inline; filename="{nombre_archivo}"')
                ]
                return request.make_response(pdf_temporal.getvalue(), headers)
            return request.not_found()

        elif tipo_archivo == "odt" or tipo_archivo == "ods":
            
            nombre_archivo_base, extension = os.path.splitext(nombre_archivo)
            
            subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", ruta_archivo, "--outdir", "/tmp"])
            ruta_archivo_pdf = os.path.join("/tmp", f"{nombre_archivo_base}.pdf")

            if os.path.exists(ruta_archivo_pdf):
                reader = PdfReader(ruta_archivo_pdf)
                writer = PdfWriter()
                
                # Add all pages to the writer
                for page in reader.pages:
                    writer.addpage(page)
                
                pdf_temporal = BytesIO()
                writer.write(pdf_temporal)
                pdf_temporal.seek(0)

                headers = [
                    ('Content-Type', 'application/pdf'),
                    ('Content-Disposition', f'inline; filename="{nombre_archivo}"')
                ]
                return request.make_response(pdf_temporal.getvalue(), headers)
            return request.not_found()
        
        
    @http.route(['/documentos/download/<string:nombre_documento>'], type='http', auth="user")
    def download_documento(self, name):
        documento = request.env['az_expedients.documentos'].sudo().search([('name', '=', name)], limit=1)
        with open(documento.file_url, 'rb') as file:
            file_content = file.read()
        
        return request.make_response(
            file_content,
            [
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', content_disposition(documento.nombre_archivo))
            ]
        )