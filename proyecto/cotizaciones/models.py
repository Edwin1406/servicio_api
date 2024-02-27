from django.db import models
from decimal import Decimal


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.IntegerField(default=0)
    servicios = models.ManyToManyField('Servicio', through='DetalleServicio', related_name='productos_servicios')


    def __str__(self):
        return f'Producto: {self.nombre}'

class Servicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    productos = models.ManyToManyField(Producto, through='DetalleServicio', related_name='servicios_productos')
    def calcular_precio_total_general(self):
        total_general = sum(detalle.calcular_precio_producto() for detalle in self.detalleservicio_set.all())
        return total_general

    def __str__(self):
        return f'Servicio: {self.nombre}'


class DetalleServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return f'Detalle de {self.servicio.nombre}: {self.producto.nombre} - Cantidad: {self.cantidad}'
    
    def calcular_precio_producto(self):
        precio_unitario = Decimal(str(self.producto.precio))  # Convierte el precio a Decimal
        iva_porcentaje = Decimal(str(self.producto.iva))  # Obtén el porcentaje de IVA del producto
        if iva_porcentaje ==Decimal(0):
            precio_total = precio_unitario * self.cantidad
        else:
            precio_sin_iva = precio_unitario * self.cantidad
            iva = (iva_porcentaje / 100) * precio_sin_iva
            precio_total = precio_sin_iva + iva
        return precio_total
    
 
   