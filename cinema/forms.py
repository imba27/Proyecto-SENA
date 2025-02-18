# forms.py 
from django import forms 
from.models import peliculas

class peliculasForm(forms.ModelForm): 
    class Meta: 
        model = peliculas
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']