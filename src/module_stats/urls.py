from django.urls import path
from module_dashboard.views import *
from module_stats.views import *

app_name = 'stats'

urlpatterns = [
    # hospitales
    path('imprimir/<int:pk>/', ViewPrintOne.as_view(), name='print_one'),
    path('servicios_atendidos_categoria', ViewStatsServicesTypes.as_view(), name='services_types'),
    path('servicios_atendidos', ViewStatsServicesDone.as_view(), name='services_done'),
]
