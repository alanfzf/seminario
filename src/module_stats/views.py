import io
import os
import calendar

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F
from django.http import FileResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone 
from django.views.generic import TemplateView, View
from django.db.models import Q
from django.urls import reverse_lazy

from pypdf import PdfReader,PdfWriter

from module_reports.models import Reporte
from module_stats.forms import SummaryForm
from module_stats.utils import *

class ViewSummary(LoginRequiredMixin, TemplateView):
    template_name = 'resumen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SummaryForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form_data = request.POST
        form = SummaryForm(form_data)
        context['form'] = form
        context['reportes'] = []

        if form.is_valid():
            query = Q()
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            service = form.cleaned_data['service_type']
            query &= Q(fecha_reporte__range=(start_date, end_date))

            if service is not None:
                query &= Q(tipo_servicio=service)
            context['reportes'] = Reporte.objects.filter(query)

        return render(request, self.template_name, context=context)


#********* PRINT VIEWS *********
class ViewPrintOne(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_to_search = kwargs.get('pk', None)

        try:
            report = Reporte.objects.get(id=id_to_search)
            form_data = get_form_data(report)
            template = os.path.join(settings.TEMPLATES_DIR, 'reporte.pdf')
            pdf_writer = PdfWriter()

            with open(template, "rb") as pdf_stream:
                pdf_reader = PdfReader(pdf_stream)
                pdf_writer.append(pdf_reader)
                pdf_writer.update_page_form_field_values(
                    pdf_writer.pages[0], 
                    form_data
                )
            output_pdf_buffer = io.BytesIO()
            pdf_writer.write(output_pdf_buffer)
            pdf_writer.close()
            output_pdf_buffer.seek(0)
            return FileResponse(
                output_pdf_buffer, 
                as_attachment=True, 
                filename=f"reporte_{report.control}.pdf")

        except Exception as e:
            print(f"ERROR: {e}")
            return HttpResponseRedirect(reverse_lazy('reports:index'))


class ViewPrintMultiple(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        rlist = request.GET.get('report_ids', "")

        if not rlist:
            raise Http404("La lista de reportes esta vacia, selecciona fechas de inicio y final!")

        try:
            # conver the list to numbers
            report_ids = list(map(int, rlist.split(',')))
            reports = Reporte.objects.filter(id__in=report_ids)
            template = os.path.join(settings.TEMPLATES_DIR, 'reporte.pdf')
            pdf_writer = PdfWriter()

            with open(template, "rb") as input_stream:
                for index, report in enumerate(reports):
                    pdf_reader = PdfReader(input_stream)
                    pdf_reader.add_form_topname(f"form{index}")
                    form_data = get_form_data(report)
                    pdf_writer.append(pdf_reader)
                    pdf_writer.update_page_form_field_values(pdf_writer.pages[index], form_data)

            # crear el buffer que contiene el pdf
            out_pdf_buffer = io.BytesIO()
            pdf_writer.write(out_pdf_buffer)
            pdf_writer.close()
            out_pdf_buffer.seek(0)
            return FileResponse(out_pdf_buffer, as_attachment=True, filename=f"reportes.pdf") 

        except Exception as e:
            print(f"ERROR: {e}")
            return HttpResponseRedirect(reverse_lazy('stats:index'))

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
    form_data['minutos'] = report.get_minutos_trabajados()
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

    # area de formalización
    form_data['formalizado'] = f"{report.formalizador.first_name } {report.formalizador.last_name}"
    form_data['conforme'] = f"{pilot.first_name} {pilot.last_name}"
    form_data['vobo'] = f"{report.jefe_servicio.first_name} {report.jefe_servicio.last_name}"
    
    return form_data
