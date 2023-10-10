from django import forms
from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # Si el usuario ya existe (Hacer el campo de contraseña opcional)
            self.fields['password'].required = False


    class Meta:
        model = User
        fields = ['username','first_name','last_name','password', 'groups']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            # render_value = True,
        }

    def clean(self):
        cleaned_data = super().clean()
        new_pass = cleaned_data.get('password')
        if not new_pass:
            del cleaned_data['password']
        return cleaned_data

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("El campo de nombre es requerido")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("El campo de apellidos es requerido")
        return last_name
