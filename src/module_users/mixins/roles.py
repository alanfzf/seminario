from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from module_users.roles import *

from django.core.exceptions import PermissionDenied

class RolAdminMixin:

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        user = request.user
        roles = [ROL_ADMIN]

        if user.is_superuser or \
            user.groups.filter(name__in=roles):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class RolDigitalizadorMixin():

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        roles = [ROL_ADMIN, ROL_DIGITALIZADOR]

        if user.is_superuser or \
            user.groups.filter(name__in=roles):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
