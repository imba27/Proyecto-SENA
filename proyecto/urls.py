"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.inicio, name='inicio') ,
    path('productos/', views.productos, name='productos'),
    path('contactanos', views.contactanos, name='contactanos'),
    path('reservas/', views.reservas, name='reservas'),
    path('login/', views.login, name='login'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('logout/', views.logout_perfil, name='logout'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('restablecer/', views.restablecer, name='restablecer'),
    path("cambiar_contraseña/<uidb64>/<token>/", views.cambiar_contraseña, name="cambiar_contraseña"),
    path("password_changed/", views.password_changed, name="pasword_changed"),
    path('perfil/', views.perfil, name='perfil'),
    path('logout/', views.logout, name='logout'),



    

    
    path('pasarela/', views.pasarela, name='pasarela'),
    path('confirmacion/<int:orden_id>/', views.confirmacion, name='confirmacion'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
