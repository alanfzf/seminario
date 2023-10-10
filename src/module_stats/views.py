import io
import os
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect, FileResponse
from django.views.generic import View
from django.urls import reverse_lazy
from django.conf import settings
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject, BooleanObject

from django.contrib.auth.mixins import LoginRequiredMixin


class ViewPrintOne(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        template = os.path.join(settings.TEMPLATES_DIR, 'reporte.pdf')
        input_stream = open(template, "rb")

        pdf_reader = PdfReader(input_stream, strict=False)
        pdf_writer = PdfWriter()

        form_data = {
            "control": "2023",
            "minutos": "test"
        }

        pdf_writer.append(pdf_reader)
        pdf_writer.update_page_form_field_values(pdf_writer.pages[0], form_data)

        # crear el buffer que contiene el pdf
        output_pdf_buffer = io.BytesIO()
        pdf_writer.write(output_pdf_buffer)
        output_pdf_buffer.seek(0)

        return FileResponse(output_pdf_buffer, as_attachment=True, filename='nuevo_archivo.pdf') 
