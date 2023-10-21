from django.urls import reverse_lazy
from django.views.generic import  View, FormView, ListView, UpdateView
from django.contrib.auth.models import User
from django.http import JsonResponse

from module_users.mixins.roles import RolAdminMixin
from .forms import UsuarioForm

class ViewListUsers( ListView):
    context_object_name = 'usuarios'
    template_name = 'all_users.html'
    model = User

class ViewCreateUser(RolAdminMixin, FormView):
    template_name = 'form_create_user.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('users:index')
    context_object_name = 'usuario'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class ViewUpdateUser(RolAdminMixin, UpdateView):
    model = User
    template_name = 'form_update_user.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('users:index')
    context_object_name = 'usuario'

    def form_valid(self, form):
        user = form.save(commit=False)
        new_pass = form.cleaned_data.get('password', None)
        # save password as it changed!
        if new_pass:
            user.set_password(new_pass)
        user.save()
        return super().form_valid(form)

class ViewDeleteUser(RolAdminMixin, View):

    def delete(self, request, *args, **kwargs):
        logged_id = self.request.user.id
        id_to_delete = kwargs.get('pk')
        resp = {}
        status = 200
        try:
            if id_to_delete == logged_id:
                raise Exception("No puedes eliminar al usuario que tiene iniciado sesión")
            usuario = User.objects.get(id=id_to_delete)
            usuario.delete()
        except Exception as e:
            resp['errors'] = str(e)
            status = 400
        return JsonResponse(resp, status=status)
