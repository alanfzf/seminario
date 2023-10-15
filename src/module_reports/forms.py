from django import forms
from django.utils import timezone
from .models import Reporte
from module_reports.utils import valid_names, valid_names_and_ages

ERROR_NAMES = "El formato debe ser ➡️ Nombres Apellidos, Otros Nombres Otros Apellidos, ..."
ERROR_AGES =  "El formato debe ser ➡️ Nombres Apellidos, Otros Nombres Otros Apellidos, ..."

class ReporteForm(forms.ModelForm):

    def clean_solicitantes(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('solicitantes')
        if not valid_names(data):
            raise forms.ValidationError(ERROR_NAMES)
        return data

    def clean_escoltas(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('escoltas')
        if data and not valid_names(data):
            raise forms.ValidationError(ERROR_NAMES)
        return data

    def clean_fallecidos(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('fallecidos')
        if data and not valid_names_and_ages(data):
            raise forms.ValidationError(ERROR_AGES)
        return data


    class Meta:
        model = Reporte
        fields = '__all__'
        widgets = {
            # GRUPO1: DETALLES GENERALES DEL REPORTE
            'control': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '0'
            }),
            'fecha_reporte': forms.DateInput( 
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'value': timezone.now().date()
                }
            ),
            'hora_salida': forms.DateTimeInput(
                format='%Y-%m-%d %H:%m',
                attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'hora_entrada': forms.DateTimeInput(
                format='%Y-%m-%d %H:%m',
                attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'salida': forms.TextInput(attrs={
                'class': 'form-control',
                'value': '36 CIA'
            }),
            'entrada': forms.TextInput(attrs={
                'class': 'form-control',
                'value': '36 CIA'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            # grupo2
            'radiotelefonista': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'pilotos': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'multiple': 'multiple'
            }),
            'unidades': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'multiple': "multiple"
            }),
            'personal_destacado': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'multiple': "multiple"
            }),
            # grupo 3
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'tipo_servicio': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'hospital': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'tipo_solicitud': forms.Select(attrs={
                'class': 'form-control',
            }),
            'solicitantes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'spellcheck': "false"
            }),
            'pacientes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'fallecidos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'escoltas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'domicilios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
        }



