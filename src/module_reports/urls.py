from django.urls import path
from module_reports.views import *

app_name = 'reports'

urlpatterns = [
    path('', ViewReports.as_view(), name='index'),
    path('crear/', ViewCreateReport.as_view(), name='create'),
    path('<int:pk>/editar/', ViewUpdateReport.as_view(), name='update'),
    path('<int:pk>/eliminar/', ViewDeleteReport.as_view(), name='delete'),
]
