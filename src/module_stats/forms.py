from django.forms import *
from django.template.defaulttags import register
from module_resources.models import Servicio

class SummaryForm(Form):

    start_date = DateField(
        label="Fecha de inicio",
        widget=DateInput( attrs={
        'class': 'form-control',
        'type': 'date',
    }))

    end_date = DateField(
        label="Fecha final",
        widget=DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))

    service_type =  ModelChoiceField(
        label="Tipo de servicio",
        empty_label="**Todos los servicios**",
        required=False,
        queryset=Servicio.objects.all(), 
        widget=Select(attrs={ 'class': 'form-control' })
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and (end_date < start_date):
            self.add_error('start_date',  'La fecha de finalización no puede ser anterior a la fecha de inicio.')

        return cleaned_data


    @register.filter(is_safe=True)
    def clabel(value):
        return value.label_tag(attrs={'class': 'form-label'})

