from django import forms
from .models import Cliente, Producto

class AddClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['codigo', 'nombre', 'telefono']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control text-dark', 'placeholder': 'Ej. C001'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control text-dark', 'placeholder': 'Nombre del cliente'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control text-dark'}),
        }

class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['codigo', 'nombre', 'telefono']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class AddProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'descripcion', 'imagen', 'costo', 'precio', 'cantidad']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
        }