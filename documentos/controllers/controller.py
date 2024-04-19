from odoo import http
from odoo.http import request
import os
from pdfrw import PdfReader, PdfWriter
from io import BytesIO
import subprocess

class DocumentoPDFController(http.Controller):

    @http.route(['/documentos/<model("pau.documentos"):documento>'], type='http', auth="user")
    def ver_primera_pagina_pdf(self, documento, **kw):
        # Aquí asumimos que 'file_url' es una ruta absoluta al archivo en el servidor
        ruta_archivo = documento.file_url
        tipo_archivo = documento.tipo_archivo
        nombre_archivo = documento.nombre_archivo
        
        
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
