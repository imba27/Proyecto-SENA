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



from .forms import FormularioRegistroUsuario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
def registrarse(request):
    if request.method == "POST":
        form = FormularioRegistroUsuario(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registro exitoso, Por favor inicia sesión")
            return redirect('login')
        else:
            for field in form.errors:
                for error in form[field].errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FormularioRegistroUsuario()
    return render(request, 'registrar.html', {'register_mode': True, 'form': form})

def login(request):
    """
    Vista para el inicio de sesión.
    Autentica a los usuarios y crea su sesión.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('productos')
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'login.html', {'register_mode': False})

def logout_perfil(request):
    logout(request)
    return redirect('inicio')



from django.contrib.auth.decorators import login_required
from .models import Reserva, Datos
from .forms import ReservaForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def reservas(request):
    # Obtener el nombre y apellido del usuario
    try:
        datos_usuario = Datos.objects.get(usuario=request.user)
        nombre = datos_usuario.nombre
        apellido = datos_usuario.apellido
    except Datos.DoesNotExist:
        nombre = request.user.username
        apellido = ""
    
    # Obtener reservas previas del usuario
    reservas_usuario = Reserva.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            
            # Para guardar la relación ManyToMany
            form.save_m2m()
            
            # Enviar correo de notificación
            productos_text = ", ".join([p.nombre for p in form.cleaned_data['productos']])
            
            subject = "Nueva Reserva en Mamá Susana"
            message = f"""Se ha recibido una nueva reserva:
            
            Usuario: {request.user.username}
            Nombre: {nombre} {apellido}
            Fecha: {reserva.fecha}
            Hora: {reserva.hora}
            Personas: {reserva.personas}
            Productos: {productos_text}
            Mensaje: {reserva.mensaje or 'Ninguno'}
            """
            from_email = 'samuellemos907@gmail.com'
            recipient_list = ['samuellemos907@gmail.com']
            
            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                print(f"Error al enviar correo: {e}")
            
            messages.success(request, "Tu reserva fue separada, uno de nuestros empleados se pondrá en contacto para dar más detalles.")
            return redirect('reservas')
        else:
            for field in form.errors:
                for error in form[field].errors:
                    messages.error(request, f"{field}: {error}")
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, error)
    else:
        form = ReservaForm()
    
    return render(request, 'reservas.html', {
        'form': form,
        'nombre': nombre,
        'apellido': apellido,
        'reservas_previas': reservas_usuario
    })