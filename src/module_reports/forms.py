from django import forms
from django.utils import timezone
from .models import Reporte
from module_reports.utils import valid_names, valid_names_and_ages
from django.template.defaulttags import register

ERROR_NAMES = "El formato debe ser ➡️ Nombres Apellidos, Otros Nombres Otros Apellidos, ..."
ERROR_AGES =  "El formato debe ser ➡️ Nombres Apellidos: Edad, Otros Nombres Otros Apellidos: Edad, ..."

class ReporteForm(forms.ModelForm):

    @register.filter(is_safe=True)
    def clabel(value):
        return value.label_tag(attrs={'class': 'form-label'})

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

    def clean(self):
        cleaned_data = super().clean()

        fecha = cleaned_data.get('fecha_reporte')
        salida = cleaned_data.get('hora_salida')
        entrada = cleaned_data.get('hora_entrada')

        if entrada and salida:
            if fecha != salida.date():
                raise forms.ValidationError(
                    "La fecha del reporte no coincide con la hora de salida"
                )
            if salida > entrada:
                raise forms.ValidationError(
                    "La hora de salida no puede ser mayor a la hora de entrada"
                )

        return cleaned_data;


    class Meta:
        model = Reporte
        fields = '__all__'
        widgets = {
            # GRUPO1: DETALLES GENERALES DEL REPORTE
            'control': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '0',
                'placeholder': 'Dato numérico (Ej, 2560)'
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
                'rows': 3,
                'spellcheck': "false",
                'placeholder': "Juan Caal, Pedro Caal..."
            }),
            'pacientes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Juan Caal: 30, Pedro Caal: 59...'
            }),
            'fallecidos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Juan Caal: 30, Pedro Caal: 59...'
            }),
            'escoltas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Juan Caal, Pedro Caal..."
            }),
            'domicilios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),

            # formalizacion
            'jefe_servicio': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'formalizador': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            
        }
