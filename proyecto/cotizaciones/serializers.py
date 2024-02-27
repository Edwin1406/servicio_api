from rest_framework import serializers
from .models import Producto, Servicio, DetalleServicio

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'iva']

class DetalleServicioSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    precio_total = serializers.SerializerMethodField()  # Campo para almacenar el precio total

    class Meta:
        model = DetalleServicio
        fields = ['producto', 'cantidad', 'precio_total']

    def get_precio_total(self, instance):
        return instance.calcular_precio_producto()



class ServicioSerializer(serializers.ModelSerializer):
    productos_detalles = DetalleServicioSerializer(many=True, read_only=True, source='detalleservicio_set')
    precio_total_general = serializers.SerializerMethodField()  # Campo para almacenar el precio total general

    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'productos_detalles', 'precio_total_general']

    def get_precio_total_general(self, instance):
        return instance.calcular_precio_total_general()