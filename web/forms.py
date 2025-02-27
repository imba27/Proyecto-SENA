from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Datos

class FormularioRegistroUsuario(UserCreationForm):
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado. Por favor utiliza otro o recupera tu contraseña.")
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if commit:
            usuario.save()
            Datos.objects.create(
                usuario=usuario,
                nombre=self.cleaned_data.get('nombre'),
                apellido=self.cleaned_data.get('apellido')
            )
        return usuario
    

from .models import Reserva, Producto
import datetime

class ReservaForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora', 'personas', 'productos', 'mensaje']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'mensaje': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Mensaje adicional (opcional)'}),
        }
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        hoy = datetime.date.today()
        
        if fecha < hoy:
            raise forms.ValidationError("No puedes hacer reservas en fechas pasadas")
        
        return fecha
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if fecha and hora and not self.instance.pk:
            if Reserva.objects.filter(fecha=fecha, hora=hora).exists():
                raise forms.ValidationError("Ya existe una reserva para esta fecha y hora. Por favor, selecciona otro horario.")
                
        return cleaned_data
    
from .models import Orden

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['nombre', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de teléfono'})
        }

