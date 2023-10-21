from django.urls import path
from module_dashboard.views import *
from module_stats.views import *

app_name = 'stats'

urlpatterns = [
    # hospitales
    path('', ViewSummary.as_view(), name='index'),
    path('imprimir/<int:pk>/', ViewPrintOne.as_view(), name='print_one'),
    path('imprimir_varios/', ViewPrintMultiple.as_view(), name='print_multiple'),
    # path('informes/', ViewPrintMultiple.as_view(), name='print_multiple'),
    path('servicios_atendidos_categoria', ViewStatsServicesTypes.as_view(), name='services_types'),
    path('servicios_atendidos', ViewStatsServicesDone.as_view(), name='services_done'),
]
