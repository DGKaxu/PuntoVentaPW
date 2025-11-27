from django import forms
from ventas.models import Cliente

class AddClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('codigo', 'nombre', 'telefono')
        labels = {
            'codigo': 'Codigo cliente:',
            'nombre': 'Nombre cliente: ',
            'telefono': 'Telefono cliente: '
        }

class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('codigo', 'nombre', 'telefono')
        labels = {
            'codigo': 'Codigo cliente:',
            'nombre': 'Nombre cliente: ',
            'telefono': 'Telefono cliente: '
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'type': 'text', 'id': 'codigo_editar'}),
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono_editar'}),
        }    
