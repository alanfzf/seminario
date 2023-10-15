from django.forms import *

class SummaryForm(Form):

    date_start = DateField(widget=DateInput(attrs={
        'class': 'form-control',
    }))

    date_end = DateField(widget=DateInput(attrs={
        'class': 'form-control'
    }))
