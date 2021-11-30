from django.contrib import admin
from webapp.models import Categoria, Marca, DireccionEnvio, Producto, User, Carrito, CarritoItem, Orden, OrdenItem

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'precio', 'fecha_carga', 'fecha_actualizacion')
    list_filter = ('categoria','marca')
    search_fields = ('modelo', 'marca__nombre')
    list_per_page = 10
    list_max_show_all = 50  
    readonly_fields = ('fecha_carga', 'fecha_actualizacion') 
    ordering = ('-fecha_carga',)
    fields = (('marca', 'modelo'), 'categoria', 'descripcion', 'precio', 'imagen', ('fecha_carga', 'fecha_actualizacion'))


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_staff')
    list_filter = ('is_staff',)
    search_fields = ('email', 'username')
    list_per_page = 10
    list_max_show_all = 50
    readonly_fields = ('password', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active') 
    ordering = ('-last_login',)


class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'numero_productos', 'total', 'fecha_actualizacion')
    search_fields = ('usuario__email',)
    list_per_page = 10
    list_max_show_all = 50
    readonly_fields = ['usuario', 'numero_productos', 'total', 'fecha_actualizacion']
    ordering = ('-fecha_actualizacion',)
    fields = ('usuario', 'numero_productos', 'total', 'fecha_actualizacion')



class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'precio_unidad', 'cantidad', 'precio_total', 'ordenado')
    search_fields = ('carrito__usuario__email',)
    list_per_page = 10
    list_max_show_all = 50
    readonly_fields = ('carrito', 'producto', 'precio_unidad', 'cantidad', 'precio_total', 'ordenado')
    ordering = ('carrito',)
    fieldsets = (
        (None, {
            'fields': ('producto', ('precio_unidad', 'cantidad', 'precio_total', 'ordenado'))
        }),
        ('Carrito', {
            'fields': ('carrito',)
        }),
    )


class OrdenItemInline(admin.TabularInline):
    model = OrdenItem
    extra = 0
    fields = ()
    readonly_fields = ('carrito_item',)
    can_delete = False


class OrdenAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'usuario' , 'precio_total', 'fecha_de_orden', 'direccion_envio')
    list_per_page = 10
    list_max_show_all = 50
    list_filter = ('fecha_de_orden',)
    fields = ('codigo', 'precio_total', 'fecha_de_orden', ('direccion_envio', 'usuario'))
    readonly_fields = ('codigo', 'usuario', 'precio_total', 'fecha_de_orden', 'direccion_envio')
    inlines = [OrdenItemInline,]
    ordering = ('-fecha_de_orden',)


class DireccionEnvioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'direccion', 'codigo_postal', 'provincia', 'pais')
    list_per_page = 10
    list_max_show_all = 50
    list_filter = ('codigo_postal', 'provincia')
    readonly_fields = ('usuario',)
    fieldsets = (
        (None, {
            'fields': (('nombre', 'apellido'), 'telefono', ('direccion', 'codigo_postal'), ('provincia', 'pais'))
        }),
        ('Usuario', {
            'fields': ('usuario',)
        }),
    )


my_models = [Categoria, Marca]

admin.site.register(my_models)
admin.site.empty_value_display = 'Eliminado'
admin.site.register(Producto, ProductoAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(CarritoItem, CarritoItemAdmin)
admin.site.register(Orden, OrdenAdmin)
admin.site.register(DireccionEnvio, DireccionEnvioAdmin)