import json
from datetime import date, datetime
from decimal import Decimal

#Django Core
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction, IntegrityError
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView

#Modelos y Formularios
from .forms import AddClienteForm, AddProductoForm, EditarClienteForm, EditarProductoForm
from .models import Cliente, Egreso, Producto, ProductosEgreso

# Funcion para verificar si es Admin
def es_administrador(user):
    return user.groups.filter(name='Administrador').exists() or user.is_superuser

@login_required(login_url='login')
def ventas_view(request):
    ventas = Egreso.objects.all()
    num_ventas = len(ventas)
    context = {
        'ventas': ventas,
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
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Cliente guardado.")
            except IntegrityError:
                messages.error(request, "Error: El Código de este cliente YA EXISTE.")
            except Exception as e:
                messages.error(request, f"Error desconocido: {e}")
                return redirect('Clientes')
    return redirect('Clientes')

@login_required(login_url='login')
@user_passes_test(es_administrador, login_url='Clientes')
def edit_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarClienteForm(
            request.POST, request.FILES, instance= cliente)
        if form.is_valid():
            try:
                form.save()
            except:
                messages.error(request, "Error al guardar el cliente")
                return redirect('Clientes') 
    return redirect('Clientes')

@login_required(login_url='login')
@user_passes_test(es_administrador, login_url='Clientes')
def delete_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_eliminar'))
        cliente.delete()
    return redirect('Clientes')    

def productos_view(request):
    productos = Producto.objects.all()
    form_add = AddProductoForm()
    form_editar = EditarProductoForm()
    context = {
            "productos" : productos,
            'form_add' : form_add,
            'form_editar': form_editar

    }
    return render(request,'productos.html', context)

def add_producto_view(request):
    if request.POST:
        form = AddProductoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Producto guardado.")
            except IntegrityError:
                messages.error(request, "Error: El Código de este producto YA EXISTE.")
            except Exception as e:
                messages.error(request, f"Error desconocido: {e}")
                return redirect('Productos')
    return redirect('Productos')

@login_required(login_url='login')
@user_passes_test(es_administrador, login_url='Productos')
def edit_producto_view(request):
    if request.POST: 
        producto = Producto.objects.get(pk=request.POST.get('id_producto_editar'))
        form = EditarProductoForm(
            request.POST, request.FILES, instance= producto)
        if form.is_valid():
            try:
                form.save()
            except:
                messages.error(request, "Error al guardar el producto")
                return redirect('Productos') 
    return redirect('Productos')

@login_required(login_url='login')
@user_passes_test(es_administrador, login_url='Productos')
def delete_producto_view(request):
    if request.POST:
        product = Producto.objects.get(pk=request.POST.get('id_producto_eliminar'))
        product.delete()
    return redirect('Productos')  

@method_decorator(login_required, name='dispatch')
class add_ventas(ListView):
    template_name = 'add_ventas.html'
    model = Egreso

    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    item['stock_actual'] = float(i.cantidad)
                    data.append(item)
            elif action == 'save':
                #Guardado de datos
                with transaction.atomic():
                    #Recuperamos datos
                    datos = json.loads(request.POST["verts"])
                    if not datos['products']: # Si la lista está vacía
                        raise Exception("No puedes guardar una venta sin productos.")

                    fecha_str = request.POST["fecha"]
                    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                    hoy = date.today()
                    if fecha_obj > hoy:
                        raise Exception(f"Error: Hoy es {hoy}.")
                    
                    id_cliente = int(request.POST["id_cliente"])
                    cliente_obj = Cliente.objects.get(pk=id_cliente)
                    
                    ticket_num = int(request.POST["ticket"])
                    ticket = True if ticket_num == 1 else False
                    
                    desglosar_num = int(request.POST["desglosar"])
                    desglosar_iva = True if desglosar_num == 1 else False
                    
                    comentarios = request.POST["comentarios"]
                    
                    # Totales
                    total_pagado = Decimal(request.POST["efectivo"]) + Decimal(request.POST["tarjeta"]) + Decimal(request.POST["transferencia"]) + Decimal(request.POST["vales"]) + Decimal(request.POST["otro"])
                    total_venta = Decimal(datos["total"])

                    if total_pagado < total_venta:
                        falta = total_venta - total_pagado
                        raise Exception(f"Pago insuficiente. Faltan ${falta:.2f} para cubrir el total de ${total_venta:.2f}")

                    nueva_venta = Egreso(
                        fecha_pedido=fecha_str, 
                        cliente=cliente_obj, 
                        total=total_venta, 
                        pagado=total_pagado, 
                        comentarios=comentarios, 
                        ticket=ticket, 
                        desglosar=desglosar_iva
                    )
                    nueva_venta.save()

                    for producto_json in datos['products']:
                        prod_id = int(producto_json['id'])
                        producto_db = Producto.objects.select_for_update().get(pk=prod_id) 
                        cantidad_vendida = Decimal(producto_json['cantidad'])
                        precio = Decimal(producto_json['precio'])
                        if cantidad_vendida <= 0:
                            raise Exception(f"Error: La cantidad del producto {producto_json['descripcion']} debe ser mayor a 0.")

                        if precio < 0:
                            raise Exception(f"Error: El precio no puede ser negativo.")
                        
                        if producto_db.cantidad < cantidad_vendida:
                            raise Exception(f"Stock insuficiente para: {producto_db.descripcion}. Disponible: {producto_db.cantidad}")
                        
                        producto_db.cantidad = Decimal(producto_db.cantidad) - cantidad_vendida
                        producto_db.save()
                        
                        subtotal = Decimal(producto_json['subtotal'])
                        
                        iva = 0
                        if desglosar_iva:
                            iva = subtotal * 0.16
                        
                        total_producto = subtotal + iva

                        detalle = ProductosEgreso(
                            egreso=nueva_venta,
                            producto=producto_db,
                            cantidad=cantidad_vendida,
                            precio=precio,
                            subtotal=subtotal,
                            iva=iva,
                            total=total_producto
                        )
                        detalle.save()
                data = [nueva_venta.id, True, desglosar_iva]
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data = {}
            data['error'] = str(e)

        return JsonResponse(data,safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos_lista"] = Producto.objects.all()
        context["clientes_lista"] = Cliente.objects.all()

        return context

@login_required(login_url='login')
@user_passes_test(es_administrador, login_url='Ventas')
def delete_venta_view(request):
    if request.POST:
        venta = Egreso.objects.get(pk=request.POST.get('id_producto_eliminar'))
        venta.delete()
    return redirect('Ventas')   

def export_pdf_view(request, id, iva):
    # 1. Recuperamos los datos (Igual que antes)
    venta = Egreso.objects.get(pk=int(id))
    datos = ProductosEgreso.objects.filter(egreso=venta)
    
    subtotal = 0 
    iva_suma = 0 
    for i in datos:
        subtotal += float(i.subtotal)
        iva_suma += float(i.iva)

    empresa = "Mi empresa S.A. De C.V"
    
    context = {
        'num_ticket': id,
        'iva': iva,
        'fecha': venta.fecha_pedido,
        'cliente': venta.cliente.nombre,
        'items': datos, 
        'total': venta.total, 
        'empresa': empresa,
        'comentarios': venta.comentarios,
        'subtotal': subtotal,
        'iva_suma': iva_suma,
    }

    # 2. EN LUGAR DE GENERAR PDF, SOLO MOSTRAMOS EL HTML
    return render(request, 'ticket.html', context)

@login_required(login_url='login')
@user_passes_test(es_administrador, login_url='Ventas')
def dashboard_view(request):
    hoy = date.today()
    
    total_ventas = Egreso.objects.aggregate(Sum('total'))['total__sum'] or 0
    
    ventas_hoy = Egreso.objects.filter(fecha_pedido=hoy).aggregate(Sum('total'))['total__sum'] or 0
    
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()

    year_actual = hoy.year
    ventas_por_mes = Egreso.objects.filter(fecha_pedido__year=year_actual)\
        .values('fecha_pedido__month')\
        .annotate(total_mes=Sum('total'))\
        .order_by('fecha_pedido__month')

    data_grafica = [0] * 12 
    
    for v in ventas_por_mes:
        mes_index = v['fecha_pedido__month'] - 1
        data_grafica[mes_index] = float(v['total_mes'])

    context = {
        'total_ventas': total_ventas,
        'ventas_hoy': ventas_hoy,
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'data_grafica': data_grafica,
        'year': year_actual
    }
    
    return render(request, 'dashboard.html', context)

def exit_view(request):
    logout(request)
    return redirect('login')