from django.contrib import admin
from ventas.models import Cliente, Producto, Empresa

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'codigo')
    search_fields = ['nombre']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Cliente, ClienteAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'cantidad', 'costo')
    search_fields = ['descripcion']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Producto, ProductoAdmin)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'domicilio', 'telefono')
    search_fields = []
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Empresa, EmpresaAdmin)