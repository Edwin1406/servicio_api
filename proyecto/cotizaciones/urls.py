from django.urls import path, include
# toca importar todos las vistas
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'servicios', ServicioViewSet)



urlpatterns = [

    path('signup/', account_signup, name='account_signup'),
    path('login/', account_login, name='account_login'),
    
    
    path('', pagina_inicio, name='pagina_inicio'),
    # esta es la ruta de la api 
    path('api/', include(router.urls)),  
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # paginas del home
    path('', pagina_inicio, name='pagina_inicio'),
    # URLs para Productos
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),

    # URLs para Servicios
    path('servicios/', lista_servicios, name='lista_servicios'),
    path('servicios/<int:servicio_id>/', detalle_servicio, name='detalle_servicio'),
    path('servicios/crear/', crear_servicio, name='crear_servicio'),
    path('servicios/editar/<int:servicio_id>/', editar_servicio, name='editar_servicio'),
    path('servicios/eliminar/<int:servicio_id>/', eliminar_servicio, name='eliminar_servicio'),
]



