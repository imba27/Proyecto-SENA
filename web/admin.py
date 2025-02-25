from django.contrib import admin
from .models import(Producto, Datos, Reserva)
from django.contrib.admin.sites import AlreadyRegistered
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    model = Producto
    list_display = ('nombre', 'precio', 'fecha_creacion','foto')
    list_display_links = ('nombre',)

admin.site.register(Producto, ProductoAdmin)

class AdminPerfilUsuario(admin.ModelAdmin):
    model = Datos
    list_display = ('usuario', 'nombre', 'apellido')    

admin.site.register(Datos, AdminPerfilUsuario)

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'hora', 'personas', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha')
    search_fields = ('usuario__username', 'usuario__email')
    readonly_fields = ('fecha_creacion',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('usuario')

# Intentamos registrar cada modelo solo si no está ya registrado
try:
    admin.site.register(Producto)
except AlreadyRegistered:
    pass

try:
    admin.site.register(Datos)
except AlreadyRegistered:
    pass

try:
    admin.site.register(Reserva, ReservaAdmin)
except AlreadyRegistered:
    # Si ya está registrado, podemos actualizar la configuración
    admin.site.unregister(Reserva)
    admin.site.register(Reserva, ReservaAdmin)