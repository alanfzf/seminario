import io
import os
from django.http import FileResponse, JsonResponse
from django.views.generic import View
from django.conf import settings
from pypdf import PdfReader,PdfWriter

from django.contrib.auth.mixins import LoginRequiredMixin

from module_reports.models import Reporte
from module_stats.utils import obtener_campo_accidente, obtener_campos_fallecidos, obtener_campos_pacientes, obtener_nombres_edades

def get_form_data(report: Reporte):
    form_data = {}
    soli_telefono = report.tipo_solicitud == 'telefono'
    pacientes, edades1 = obtener_nombres_edades(report.pacientes)
    fallecidos, edades2 = obtener_nombres_edades(report.fallecidos)
    listado_edades = map(str, edades1+edades2)
    hay_fallecidos = report.fallecidos is not None and len(report.fallecidos.strip()) >= 0
    campos_pc = obtener_campos_pacientes(pacientes)
    campos_fa = obtener_campos_fallecidos(fallecidos)
    servicio = report.tipo_servicio.nombre
    campos_acc = obtener_campo_accidente(servicio)
    print(servicio)

    form_data['control'] = report.control
    form_data['fecha'] = report.fecha_reporte
    form_data['minutos'] = int((report.hora_entrada - report.hora_salida).total_seconds() / 60)
    form_data['telefono'] = "X" if soli_telefono else ""
    form_data['personal'] = "" if soli_telefono else "X"
    form_data['salida'] = report.salida
    form_data['entrada'] = report.entrada
    form_data['hora_salida'] = report.hora_salida.strftime('%H:%M')
    form_data['hora_entrada'] = report.hora_entrada.strftime('%H:%M')
    form_data['direccion'] = report.direccion
    form_data['solicitantes'] = report.solicitantes
    # asignar los campos multiples
    for clave, valor in campos_pc.items():
        form_data[clave] = valor
    for clave, valor in campos_fa.items():
        form_data[clave] = valor

    form_data['si_fallecido'] = "X" if hay_fallecidos else ""
    form_data['no_fallecido'] = "X" if not hay_fallecidos else ""
    form_data['edades'] = ','.join(listado_edades)
    form_data['domicilios'] = report.domicilios
    form_data['escoltas'] = report.escoltas
    for clave, valor in campos_acc.items():
        form_data[clave] = valor

    return form_data



class ViewPrintOne(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        id_to_search = kwargs.get('pk')

        try:
            report = Reporte.objects.get(id=id_to_search)
            form_data = get_form_data(report)

            template = os.path.join(settings.TEMPLATES_DIR, 'reporte.pdf')
            input_stream = open(template, "rb")

            pdf_reader = PdfReader(input_stream, strict=False)


            pdf_writer = PdfWriter()

            pdf_writer.append(pdf_reader)
            pdf_writer.update_page_form_field_values(pdf_writer.pages[0], form_data)

            # crear el buffer que contiene el pdf
            output_pdf_buffer = io.BytesIO()
            pdf_writer.write(output_pdf_buffer)
            output_pdf_buffer.seek(0)

            return FileResponse(output_pdf_buffer, as_attachment=True, filename=f"reporte_{report.control}.pdf") 

        except Exception as e:
            return JsonResponse({ "error": str(e) }, status=500)
