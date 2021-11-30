from django.forms import ModelForm
from django import forms
from .models import Producto, User, DireccionEnvio
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ProductoForm(ModelForm):
	class Meta:
		model = Producto
		fields = ('modelo', 'marca', 'categoria', 'descripcion', 'imagen', 'precio')
		widgets = {
			'modelo': forms.TextInput(attrs={'class': 'form-control'}),
			'marca': forms.Select(attrs={'class': 'form-control'}),
			'categoria': forms.Select(attrs={'class': 'form-control'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
			'imagen': forms.ClearableFileInput(attrs={'class': 'custom-file', 'onchange': "document.getElementById('imgdetalle').src = window.URL.createObjectURL(this.files[0])"}),
			'precio': forms.NumberInput(attrs={'class': 'form-control'}),	
		}


class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('email', 'username', 'password1', 'password2')
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico*'})
		}

	def __init__(self, *args, **kwargs):
		super(CustomUserCreationForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario*'})
		self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña*'})
		self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmación de contraseña*'})


class CustomAuthenticationForm(AuthenticationForm):
	class Meta:
		model = User
		fields = ("username", "password")

	def __init__(self, *args, **kwargs):
		super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico*', 'autofocus': 'autofocus'})
		self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña*'})


class ContactoForm(forms.Form):
	nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
	correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico*'}))
	asunto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto*'}))
	mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribí tu mensaje aquí...', 'maxlength': 250, 'rows': 7}))


class DireccionEnvioForm(ModelForm):
	class Meta:
		model = DireccionEnvio
		fields = ('nombre', 'apellido', 'telefono', 'direccion', 'pais', 'provincia', 'codigo_postal')
		widgets = {
			'nombre': forms.TextInput(attrs={'class': 'form-control'}),
			'apellido': forms.TextInput(attrs={'class': 'form-control'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control'}),
			'direccion': forms.TextInput(attrs={'class': 'form-control'}),
			'pais': forms.TextInput(attrs={'class': 'form-control', 'value': 'Argentina', 'readonly': 'readonly'}),
			'provincia': forms.TextInput(attrs={'class': 'form-control'}),
			'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
		}