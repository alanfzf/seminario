import io
import os
import calendar

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F
from django.http import FileResponse, JsonResponse
from django.utils import timezone 
from django.views.generic import TemplateView, View
from pypdf import PdfReader,PdfWriter

from module_reports.models import Reporte
from module_stats.forms import SummaryForm
from module_stats.utils import obtener_campo_accidente, obtener_campo_personal, obtener_campos_hospital, obtener_campos_fallecidos, obtener_campos_pacientes, obtener_nombres_edades


class ViewSummary(LoginRequiredMixin, TemplateView):
    template_name = 'resumen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SummaryForm()
        return context


#********* PRINT VIEWS *********
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


class ViewPrintMultiple(LoginRequiredMixin, View):
    pass


class ViewStatsServicesTypes(LoginRequiredMixin, View):
    # esta vista sirve para visualizar la cantidad de los servicios atendidos por categoria
    # en el mes actual
    def get(self, request, *args, **kwargs):
        today = timezone.now()
        cal_lastday = calendar.monthrange(today.year, today.month)[1]
        first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day = today.replace(day=cal_lastday, hour=23, minute=59, second=59, microsecond=9999)
        estadistica = {}

        top_servicios = Reporte.objects.\
        filter(fecha_reporte__range=(first_day, last_day)).\
        values('tipo_servicio__nombre').annotate(cantidad=Count('tipo_servicio')).\
        order_by('-cantidad')[:5]

        for servicio in top_servicios:
            nombre = servicio['tipo_servicio__nombre']
            qty = servicio['cantidad']
            estadistica[nombre] = qty

        return JsonResponse(estadistica)


class ViewStatsServicesDone(LoginRequiredMixin, View):
    # esta vista sirve para visualizar la cantidad de servicios atendidos por cada dia en el mes actual

    def get(self, request, *args, **kwargs):
        today = timezone.now()
        cal_lastday = calendar.monthrange(today.year, today.month)[1]
        first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day = today.replace(day=cal_lastday, hour=23, minute=59, second=59, microsecond=9999)

        servicios_por_dia = Reporte.objects.filter(fecha_reporte__range=(first_day, last_day)) \
                             .annotate(dia=F('fecha_reporte__day')) \
                             .values('dia') \
                             .annotate(total=Count('id')) \
                             .order_by('dia')
        resultados = {servicio['dia']: servicio['total'] for servicio in servicios_por_dia}

        for dia in range(1, cal_lastday+1):
            resultados.setdefault(dia, 0)

        resultados = dict(sorted(resultados.items()))
        return JsonResponse(resultados)

# UTIL FUNCTIONS
def get_form_data(report: Reporte):
    form_data = {}
    soli_telefono = report.tipo_solicitud == 'telefono'
    pacientes, edades1 = obtener_nombres_edades(report.pacientes)
    fallecidos, edades2 = obtener_nombres_edades(report.fallecidos)
    listado_edades = map(str, edades1+edades2)
    hay_fallecidos = report.fallecidos is not None and len(report.fallecidos.strip()) > 0
    campos_pc = obtener_campos_pacientes(pacientes)
    campos_fa = obtener_campos_fallecidos(fallecidos)
    servicio = report.tipo_servicio.nombre
    campos_acc = obtener_campo_accidente(servicio)
    hospital = report.hospital.nombre
    campos_hosp = obtener_campos_hospital(hospital)

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
    for clave, valor in campos_hosp.items():
        form_data[clave] = valor

    telf = report.radiotelefonista
    pilot = report.pilotos.first()
    unidades = report.unidades.all()
    nombres_uni = [unidad.nombre for unidad in unidades]
    personas = report.personal_destacado.all()
    nombres_personal = [f"{personal.first_name} {personal.last_name}" for personal in personas]
    campos_personal = obtener_campo_personal(nombres_personal)

    form_data['radiotelefonista'] = f"{telf.first_name } {telf.last_name}"
    form_data['pilotos'] = f"{pilot.first_name} {pilot.last_name}"
    form_data['unidades'] = ", ".join(nombres_uni)
    for clave, valor in campos_personal.items():
        form_data[clave] = valor
    form_data['observaciones'] = report.observaciones
    
    return form_data
