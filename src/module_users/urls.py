from django.urls import path
from .views import ViewCreateUser, ViewUpdateUser, ViewDeleteUser,ViewListUsers

app_name = 'users'

urlpatterns = [
    path('', ViewListUsers.as_view(), name='index'),
    path('crear/', ViewCreateUser.as_view(), name='create'),
    path('<int:pk>/editar/', ViewUpdateUser.as_view(), name='update'),
    path('<int:pk>/eliminar/', ViewDeleteUser.as_view(), name='delete'),
]
