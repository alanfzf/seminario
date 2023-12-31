# Generated by Django 4.2.5 on 2023-10-16 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('module_resources', '0002_alter_hospital_nombre_alter_servicio_nombre_and_more'),
        ('module_reports', '0005_rename_acompaniantes_reporte_escoltas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='escoltas',
            field=models.TextField(blank=True, verbose_name='Acompañantes'),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='module_resources.hospital', verbose_name='Hospital de traslado'),
        ),
    ]
