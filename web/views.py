from django.shortcuts import render



# Create your views here.

def inicio(request):
    return render (request, 'inicio.html')
def contactanos(request):
    return render (request, 'contactanos.html')


from .models import Producto, CarritoItem
def productos(request):
    producto_lista = Producto.objects.all()

    if request.method == "POST" and 'producto_id' in request.POST:
        producto_id = request.POST.get('producto_id')
        try:
            producto = Producto.objects.get(id=producto_id)
            
            if not request.user.is_authenticated:
                if not request.session.session_key:
                    request.session.create()
                sesion_id = request.session.session_key
                
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    sesion_id=sesion_id,
                    usuario=None
                )
                
                if not created:
                    carrito_item.cantidad += 1
                    carrito_item.save()
            else:
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    usuario=request.user,
                    sesion_id=None
                )
                
                if not created:
                    carrito_item.cantidad += 1
                    carrito_item.save()
            
            messages.success(request, f"{producto.nombre} añadido al carrito")
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")
    
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

        subject = "Nueva Reserva Recibida"
        message = f"Nombre: {nombre}\nEmail: {email}\nFecha: {fecha}\nPersonas: {personas}"
        from_email = 'imbachi@gmail.com'
        recipient_list = ['imbachi@gmail.com'] 
        
        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, "Tu reserva ha sido enviada con éxito. ¡Nos pondremos en contacto contigo!")
        return redirect("reservas")  

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
    try:
        datos_usuario = Datos.objects.get(usuario=request.user)
        nombre = datos_usuario.nombre
        apellido = datos_usuario.apellido
    except Datos.DoesNotExist:
        nombre = request.user.username
        apellido = ""

    reservas_usuario = Reserva.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            
            form.save_m2m()
            
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

def ver_carrito(request):
    carrito_items = []
    total = 0
    
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)
    
    for item in carrito_items:
        total += item.subtotal()
    
    return render(request, 'carrito.html', {
        'carrito_items': carrito_items,
        'total': total
    })

def actualizar_carrito(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
            else:
                item.delete()
            
            messages.success(request, "Carrito actualizado")
        else:
            messages.error(request, "No tienes permiso para modificar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')

def eliminar_item(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            item.delete()
            messages.success(request, "Item eliminado del carrito")
        else:
            messages.error(request, "No tienes permiso para eliminar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')

<<<<<<< HEAD



from django.contrib.auth.models import User 
from django.contrib.auth.tokens import default_token_generator 
from django.core.mail import send_mail 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes, force_str

def restablecer(request): 
    if request.method == "POST": 
        email = request.POST["email"] 
        user = User.objects.filter(email=email).first() 
    if user: 
        token = default_token_generator.make_token(user) 
        uid = urlsafe_base64_encode(force_bytes(user.pk)) 
        enlace = request.build_absolute_uri(f"/cambiar_contraseña/{uid}/{token}/") 
        send_mail( 
            "Restablecimiento de contraseña", 
            f"Haz clic en el siguiente enlace para cambiar tu contraseña: {enlace}", 
            "jalmpa77@gmail.com", 
            [email], 
            fail_silently=False, 
        )
        messages.success (request, "Se ha enviado un enlace de restablecimiento a su correo.") 
        return redirect("home") 
    else: 
        messages.error(request, "No se encontró un usuario con ese correo electrónico.") 
        return redirect("restablecer") # Redirige de nuevo a la página de restablecimiento 
    
    return render(request, "restablecer.html")


def cambiar_contraseña (request, uidb64, token): 
    try: 
        uid = force_str(urlsafe_base64_decode (uidb64)) 
        user = User.objects.get(pk=uid) 
    except (TypeError, ValueError, OverflowError, User.DoesNotExist): 
         user = None 
    if user and default_token_generator.check_token(user, token): 
        if request.method == "POST": 
            nueva_contraseña = request.POST["password"] 
            user.set_password(nueva_contraseña) 
            user.save() 
            return redirect("password_changed") 

        return render(request, "cambiar_contraseña.html") 
        
    return redirect("login") 
    

def password_changed(request):
    return render(request, "password_changed.html") 
=======
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarritoItem, Orden, OrdenItem
from .forms import OrdenForm

def pasarela(request):
    carrito_items = []
    total = 0
    
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)
    
    if not carrito_items:
        messages.warning(request, "Tu carrito está vacío")
        return redirect('ver_carrito')
    
    for item in carrito_items:
        total += item.subtotal()
    
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            
            if request.user.is_authenticated:
                orden.usuario = request.user
            else:
                orden.sesion_id = request.session.session_key
            
            orden.total = total
            orden.save()
            
            for item in carrito_items:
                OrdenItem.objects.create(
                    orden=orden,
                    producto=item.producto,
                    precio=item.producto.precio,
                    cantidad=item.cantidad
                )
            
            carrito_items.delete()
            
            messages.success(request, "Tu pedido ha sido procesado con éxito")
            return redirect('confirmacion', orden_id=orden.id)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            try:
                datos = Datos.objects.get(usuario=request.user)
                initial_data = {
                    'nombre': f"{datos.nombre} {datos.apellido}",
                    'email': request.user.email
                }
            except Datos.DoesNotExist:
                initial_data = {
                    'nombre': request.user.username,
                    'email': request.user.email
                }
        
        form = OrdenForm(initial=initial_data)
    
    return render(request, 'pasarela.html', {
        'form': form,
        'carrito_items': carrito_items,
        'total': total
    })

def confirmacion(request, orden_id):
    try:
        if request.user.is_authenticated:
            orden = Orden.objects.get(id=orden_id, usuario=request.user)
        else:
            orden = Orden.objects.get(id=orden_id, sesion_id=request.session.session_key)
        
        items = OrdenItem.objects.filter(orden=orden)
        
        return render(request, 'confirmacion.html', {
            'orden': orden,
            'items': items
        })
    except Orden.DoesNotExist:
        messages.error(request, "Orden no encontrada")
        return redirect('productos')
>>>>>>> fa38a925adb451552b05c173be6edfa9c1c7f45e
