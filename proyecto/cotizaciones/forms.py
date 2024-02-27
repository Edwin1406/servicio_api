from django import forms
from .models import Producto, Servicio,DetalleServicio


# --------------------------------------------------------Formulario de productos--------------------------------------------------

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio','iva']


# ---------------------------------para el formulario de servicios donde extraigo los productos de ese servicio-----------------------
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'productos']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        servicio_productos = Producto.objects.all()
        self.fields['productos'] = forms.ModelMultipleChoiceField(
            queryset=servicio_productos,
            widget=forms.CheckboxSelectMultiple
        )
        for producto in servicio_productos:
            cantidad_key = f'cantidad_{producto.id}'
            initial_cantidad = 0
            if self.instance and self.instance.pk:
                try:
                    initial_cantidad = self.instance.detalleservicio_set.get(producto=producto).cantidad
                except DetalleServicio.DoesNotExist:
                    pass
            self.fields[cantidad_key] = forms.IntegerField(
                widget=forms.NumberInput(attrs={'min': 0}),
                label=f'Cantidad para {producto.nombre}',
                initial=initial_cantidad,
            )
# -------------------------esto es para validar y limpiar  los datos ingresados por el formulario antes de procesarlos 
    def clean(self):
        cleaned_data = super().clean()
        cantidades = {}
        for producto in self.fields['productos'].queryset:
            cantidad_key = f'cantidad_{producto.id}'
            cantidad_value = cleaned_data.get(cantidad_key)
            # Permitir cualquier cantidad (incluyendo cero)
            if cantidad_value is not None:
                cantidades[producto] = cantidad_value
        cleaned_data['cantidades'] = cantidades
        return cleaned_data
    
    

  