from django.shortcuts import render


# Create your views here.

def inicio(request):
    return render (request, 'inicio.html')
def contactanos(request):
    return render (request, 'contactanos.html')
def reservas(request):
    return render (request, 'reservas.html')
def login(request):
    return render (request, 'login.html')


#contactanos

from .models import Producto
def productos(request):
    producto_lista = Producto.objects.all()
    return render(request, 'productos.html', {'productos': producto_lista})

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def reservas(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        email = request.POST['email']
        fecha = request.POST['fecha']
        personas = request.POST['personas']

        # Enviar el correo de notificación
        subject = "Nueva Reserva Recibida"
        message = f"Nombre: {nombre}\nEmail: {email}\nFecha: {fecha}\nPersonas: {personas}"
        from_email = 'tu_correo@gmail.com'
        recipient_list = ['tu_correo@gmail.com']  # Aquí coloca el correo que recibirá la notificación
        
        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, "Tu reserva ha sido enviada con éxito. ¡Nos pondremos en contacto contigo!")
        return redirect("reservas")  # Redirecciona a la página de reservas

    return render(request, "reservas.html")