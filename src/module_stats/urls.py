from django.urls import path
from module_dashboard.views import *
from module_stats.views import *

app_name = 'stats'

urlpatterns = [
    # hospitales
    path('imprimir/<int:pk>/', ViewPrintOne.as_view(), name='print_one'),
    # path('/imprimir_varios/', ViewHospitals.as_view(), name='print_multiple'),
]
