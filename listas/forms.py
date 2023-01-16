from django.forms import ModelForm
from .models import Lista, Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class ListaForm(ModelForm):
    class Meta:
        model = Lista
        fields = ['nombre_lista']
        labels = {
            'nombre_lista': 'Título',
        }
        error_messages = []


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['descripcion_item', 'completado']
        labels = {
            'descripcion_item': 'Ítem',
        }

class RegistrarUsuarioForm(UserCreationForm):   
    user = {
        'label':'Nombre', 
        'required': True}
    email = {
        'label':'Correo electrónico', 
        'required': True}
    labels = {
            'username': 'nombre de usuario',
            'email': 'Dirección de correo',
            'password1': 'Contraseña',
            'password2': 'Repita contraseña',
        }
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        required_fields = ['username', 'email', 'password1', 'password2']

class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un username',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            raise forms.ValidationError('El usuario no existe')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


