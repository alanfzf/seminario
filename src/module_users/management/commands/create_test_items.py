from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from module_users.roles import *
from django.contrib.auth.models import User
from module_resources.models import *


class Command(BaseCommand):
    help = 'Crea los items para hacer pruebas'

    def handle(self, *args, **kwargs):

        # crear superusuario
        user = User.objects.create_superuser(
            'admin', 
            'admin@admin.com', 
            'admin'
        )

        user.first_name = 'Nombre'
        user.last_name = 'Apellido'
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Se creo al superusuario'))

        # crear items de recursos
        hospital = Hospital(nombre='General')
        hospital.save()
        self.stdout.write(self.style.SUCCESS(f'Se creo al hospital'))

        servicio = Servicio(nombre='Caida casual')
        servicio.save()
        self.stdout.write(self.style.SUCCESS(f'Se creo el tipo de servicio'))

        vehiculo = Vehiculo(nombre='Ambulancia')
        vehiculo.save()
        self.stdout.write(self.style.SUCCESS(f'Se creo el vehiculo'))
