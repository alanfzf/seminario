from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import  CreateView, ListView, UpdateView, View
from .models import Vehiculo, Hospital, Servicio
from .forms import HospitalForm, ServicioForm, VehiculoForm

#***** APARTADO DE VEHICULOS *****
class ViewVehicles(ListView):
    context_object_name = 'vehiculos'
    template_name = 'vehiculos/all.html'
    model = Vehiculo

class ViewVehicleCreate(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculos/create.html'
    success_url = reverse_lazy('resources:vehicles')

class ViewVehicleUpdate(UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculos/update.html'
    success_url = reverse_lazy('resources:vehicles')

class ViewVehicleDelete(View):
    def delete(self, request, *args, **kwargs):
        id_to_delete = kwargs.get('pk')
        status = 200
        resp = {}
        try:
            vehiculo = Vehiculo.objects.get(id=id_to_delete);
            vehiculo.delete()
        except Exception as e:
            status = 400
            resp['errors'] = str(e)
        return JsonResponse(resp, status=status)

#***** APARTADO DE SERVICIOS *****
class ViewServices(ListView):
    context_object_name = 'servicios'
    template_name = 'servicios/all.html'
    model = Servicio

class ViewServiceCreate(CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicios/create.html'
    success_url = reverse_lazy('resources:services')

class ViewServiceUpdate(UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicios/update.html'
    success_url = reverse_lazy('resources:services')

class ViewServiceDelete(View):
    def delete(self, request, *args, **kwargs):
        id_to_delete = kwargs.get('pk')
        status = 200
        resp = {}
        try:
            servicio = Servicio.objects.get(id=id_to_delete);
            servicio.delete()
        except Exception as e:
            status = 400
            resp['errors'] = str(e)
        return JsonResponse(resp, status=status)

#***** APARTADO DE HOSPITALES *****
class ViewHospitals(LoginRequiredMixin, ListView):
    template_name = 'hospitales/all.html'
    context_object_name = 'hospitales'
    model = Hospital

class ViewHospitalCreate(LoginRequiredMixin, CreateView):
    model = Hospital
    form_class = HospitalForm
    template_name = 'hospitales/create.html'
    success_url = reverse_lazy('resources:hospitals')

class ViewHospitalUpdate(LoginRequiredMixin, UpdateView):
    model = Hospital
    form_class = HospitalForm
    template_name = 'hospitales/update.html'
    success_url = reverse_lazy('resources:hospitals')

class ViewHospitalDelete(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        id_to_delete = kwargs.get('pk')
        status = 200
        resp = {}
        try:
            hospital = Hospital.objects.get(id=id_to_delete);
            hospital.delete()
        except Exception as e:
            status = 400
            resp['errors'] = str(e)

        return JsonResponse(resp, status=status)
