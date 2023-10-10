from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from django.http import JsonResponse
from module_reports.forms import ReporteForm
from module_reports.models import Reporte

class ViewReports(LoginRequiredMixin, ListView):
    context_object_name = 'reportes'
    template_name = 'all_reports.html'
    model = Reporte

class ViewCreateReport(LoginRequiredMixin, CreateView):
    model = Reporte
    template_name = 'form_create_report.html'
    form_class = ReporteForm
    success_url = reverse_lazy('reports:index')

class ViewUpdateReport(LoginRequiredMixin, UpdateView):
    model = Reporte
    template_name = 'form_update_report.html'
    form_class = ReporteForm
    success_url = reverse_lazy('reports:index')


class ViewDeleteReport(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        id_to_delete = kwargs.get('pk')
        status = 200
        resp = {}
        try:
            report = Reporte.objects.get(id=id_to_delete);
            report.delete()
        except Exception as e:
            status = 400
            resp['errors'] = str(e)
        return JsonResponse(resp, status=status)
