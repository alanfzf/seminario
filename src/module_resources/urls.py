from django.urls import path
from module_dashboard.views import *
from module_resources.views import ViewHospitalCreate, ViewHospitalDelete, ViewHospitalUpdate, ViewHospitals, ViewServiceCreate, ViewServiceDelete, ViewServices, ViewVehicleDelete, ViewVehicleUpdate, ViewVehicles, ViewServiceUpdate, ViewVehicleCreate

app_name = 'resources'

urlpatterns = [
    # hospitales
    path('hospitales/', ViewHospitals.as_view(), name='hospitals'),
    path('hospitales/crear/', ViewHospitalCreate.as_view(), name='hospital_create'),
    path('hospitales/<int:pk>/editar/', ViewHospitalUpdate.as_view(), name='hospital_update'),
    path('hospitales/<int:pk>/eliminar/', ViewHospitalDelete.as_view(), name='hospital_delete'),

    # servicios
    path('servicios/', ViewServices.as_view(), name='services'),
    path('servicios/crear/', ViewServiceCreate.as_view(), name='service_create'),
    path('servicios/<int:pk>/editar/', ViewServiceUpdate.as_view(), name='service_update'),
    path('servicios/<int:pk>/eliminar/', ViewServiceDelete.as_view(), name='service_delete'),

    # vehiculos
    path('vehiculos/', ViewVehicles.as_view(), name='vehicles'),
    path('vehiculos/crear/', ViewVehicleCreate.as_view(), name='vehicle_create'),
    path('vehiculos/<int:pk>/editar/', ViewVehicleUpdate.as_view(), name='vehicle_update'),
    path('vehiculos/<int:pk>/eliminar/', ViewVehicleDelete.as_view(), name='vehicle_delete'),
]
