from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render (request, 'inicio.html')
def contactanos(request):
    return render (request, 'contactanos.html')


from .models import Producto
def productos(request):
    producto_lista = Producto.objects.all()
    return render(request, 'productos.html', {'productos': producto_lista})