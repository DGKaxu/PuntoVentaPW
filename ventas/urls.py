from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.exit_view, name='logout'),

    path('ventas/', views.ventas_view, name='Ventas'),

    path('clientes/', views.clientes_view, name='Clientes'),
    path('add_cliente/', views.add_cliente_view, name='AddCliente'), 
    path('edit_cliente/', views.edit_cliente_view, name='EditCliente'),
    path('delete_cliente/', views.delete_cliente_view, name='DeleteCliente'),

    path('productos/', views.productos_view, name='Productos'),
    path('add_producto/', views.add_producto_view, name='AddProducto'),
    path('edit_producto/', views.edit_producto_view, name='EditProduct'),
    path('delete_producto/', views.delete_producto_view, name='DeleteProduct'),

    path('add_venta/', views.add_ventas.as_view(), name='AddVenta'),
    path('delete_venta/', views.delete_venta_view, name='DeleteVenta'),
    
    path('export/', views.export_pdf_view, name="ExportPDF"),
    path('export/<id>/<iva>', views.export_pdf_view, name="ExportPDF"),

    path('dashboard/', views.dashboard_view, name='Dashboard'),
]