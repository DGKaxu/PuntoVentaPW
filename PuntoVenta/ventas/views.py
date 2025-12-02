from django.shortcuts import render, redirect
from .models import Cliente, Producto
from .forms import AddClienteForm, EditarClienteForm, AddProductoForm
from django.contrib import messages

# Create your views here.
def ventas_view(request):
    num_ventas = 156
    context = {
        'num_ventas': num_ventas
    }
    return render(request,'ventas.html', context)

def clientes_view(request):
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()

    context = {
        'clientes': clientes,
        'form_personal': form_personal,
        'form_editar': form_editar
    }
    return render(request,'clientes.html', context)

def add_cliente_view(request):
    #print("Guardar cliente")
    if request.POST:
        form = AddClienteForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages(request, "Error al guardar el cliente")
                return redirect('Clientes')
    return redirect('Clientes')

def edit_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarClienteForm(
            request.POST, request.FILES, instance= cliente)
        if form.is_valid:
            try:
                form.save()
            except:
                messages(request, "Error al guardar el cliente")
                return redirect('Clientes') 
    return redirect('Clientes')

def delete_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_eliminar'))
        cliente.delete()
    return redirect('Clientes')    

def productos_view(request):
    """
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()
    """
    productos = Producto.objects.all()
    form_add = AddProductoForm()
    context = {
            "productos" : productos,
            'form_add' : form_add
    }
    return render(request,'productos.html', context)

def add_producto_view(request):
    if request.POST:
        form = AddProductoForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages(request, "Error al guardar el producto")
                return redirect('Productos')
    return redirect('Productos')