# Generated by Django 4.2.5 on 2023-10-01 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module_resources', '0002_alter_hospital_nombre_alter_servicio_nombre_and_more'),
        ('module_reports', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporte',
            name='unidades',
        ),
        migrations.AddField(
            model_name='reporte',
            name='unidades',
            field=models.ManyToManyField(to='module_resources.vehiculo'),
        ),
    ]
