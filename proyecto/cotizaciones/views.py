
from django.shortcuts import render, redirect
from .models import Producto, Servicio,DetalleServicio
from .forms import ProductoForm, ServicioForm
from .serializers import ServicioSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework import serializers  
from rest_framework import viewsets
from .serializers import ProductoSerializer, ServicioSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import ensure_csrf_cookie
# import requests
# import requests_cache


# cache_dir = '/path/to/cache/directory'
# requests_cache.install_cache('cache_nombre', cache_dir=cache_dir, expire_after=200)


# vista del api rest_framework
# LoginRequiredMixin esto es para que no puedan entarr si no estan logueados
class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/login/?next=/api/servicios/'
@api_view()
@ensure_csrf_cookie
def inicio(request):
    cotizaciones = Servicio.objects.all()
    serializer = ServicioSerializer(cotizaciones, many=True)
    return Response(serializer.data)
# mostrar los productos rest
class ProductoViewSet(CustomLoginRequiredMixin,viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
# mostrar los servicios rest
class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer


# esto es para que no me deje entrar si no estoy logueado
@login_required
#----------------------------------------------- crear usuario------------.------------------------------------------------------
def account_logout(request):
    logout(request)
    return render(request, '/')
def account_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}. Puedes iniciar sesión ahora.')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup_template.html', {'form': form})

#----------------------------------------------- login para el administrador------------------------------------------------------
def account_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
    return render(request, 'iniciar_sesion.html')

#----------------------------------------------- editar producto------------.------------------------------------------------------

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('detalle_producto', producto_id=producto_id)
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})


#----------------------------------------------- Eliminar Producto------------.------------------------------------------------------
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        try:
            producto.delete()
            messages.success(request, 'Producto eliminado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el producto: {str(e)}')
        return redirect('lista_productos')

    return render(request, 'eliminar_producto.html', {'producto': producto})

#----------------------------------------------- Editar Servicio------------.------------------------------------------------------

def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            servicio = form.save()
            productos_cantidades = form.cleaned_data.get('cantidades', {})
            servicio.detalleservicio_set.exclude(producto__in=productos_cantidades.keys()).delete()
            for producto, cantidad in productos_cantidades.items():
                if cantidad > 0:
                    detalle_servicio, created = DetalleServicio.objects.get_or_create(servicio=servicio, producto=producto)
                    detalle_servicio.cantidad = cantidad
                    detalle_servicio.save()
                else:
                    DetalleServicio.objects.filter(servicio=servicio, producto=producto).delete()
            return redirect('detalle_servicio', servicio_id=servicio_id)
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'editar_servicio.html', {'form': form, 'servicio': servicio})


#----------------------------------------------- Eliminar Servicio------------.------------------------------------------------------
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        servicio.delete()
        return redirect('lista_servicios')
    return render(request, 'eliminar_servicio.html', {'servicio': servicio})


#----------------------------------------------- Inicio -------------------.------------------------------------------------------
def pagina_inicio(request):
    return render(request, 'index.html')


#----------------------------------------------- Detalle Producto------------.------------------------------------------------------
def detalle_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})


#----------------------------------------------- Lista Servicios------------.------------------------------------------------------
def lista_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'lista_servicios.html', {'servicios': servicios})

#----------------------------------------------- Detalle de Servicio------------.------------------------------------------------------
def detalle_servicio(request, servicio_id):
    servicio = Servicio.objects.get(id=servicio_id)
    return render(request, 'detalle_servicio.html', {'servicio': servicio})

#----------------------------------------------- Lista Producto------------.------------------------------------------------------
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})


#----------------------------------------------- crear producto------------.------------------------------------------------------
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

#----------------------------------------------- Crea Servicio------------.------------------------------------------------------
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            productos_cantidades = form.cleaned_data.get('cantidades', {})
            for producto, cantidad in productos_cantidades.items():
                if cantidad > 0:
                    detalle_servicio, created = DetalleServicio.objects.get_or_create(
                        servicio=servicio,
                        producto=producto
                    )
                    detalle_servicio.cantidad = cantidad
                    detalle_servicio.save()
            return redirect('lista_servicios')
    else:
        form = ServicioForm()
    return render(request, 'crear_servicio.html', {'form': form})
#--------------------------------------------------------------------------.------------------------------------------------------
