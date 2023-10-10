from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Crea los grupos por defecto'

    def handle(self, *args, **kwargs):
        # Lista de nombres de grupos por defecto
        default_groups = ['Administrador', 'Digitalizador']

        for group_name in default_groups:
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Se creó el grupo: {group_name}'))
            else:
                self.stdout.write(self.style.ERROR(f'El grupo ya existe: {group_name}'))
