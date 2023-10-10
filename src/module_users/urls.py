from django.urls import path
from .views import VistaCrearUsuario, VistaEditarUsuario, VistaEliminarUsuario,VistaListarUsuarios

app_name = 'users'

urlpatterns = [
    path('', VistaListarUsuarios.as_view(), name='index'),
    path('crear/', VistaCrearUsuario.as_view(), name='create'),
    path('<int:pk>/editar/', VistaEditarUsuario.as_view(), name='update'),
    path('<int:pk>/eliminar/', VistaEliminarUsuario.as_view(), name='delete'),
]
