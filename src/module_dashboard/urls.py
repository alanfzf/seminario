from django.urls import path
from module_dashboard.views import *

app_name = 'dashboard'

urlpatterns = [
    path('', Dashboard.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
]
