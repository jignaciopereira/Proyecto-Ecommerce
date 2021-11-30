from django.urls import path
from django.views.decorators.http import require_POST

from . import views

app_name = 'webapp'
urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.ProductoListView.as_view(), name='index'),
    path('acerca-de/', views.acerca_de, name='acerca-de'),
    path('contacto/', views.contacto, name='contacto'),
    path('busqueda/', views.buscar_producto, name='busqueda'),
    path('categoria/<slug:slug>/', views.ProductoCategoriaListView.as_view(), name='categoria'),
    #path('categoria/<slug:slug>/', views.filtrar_categoria, name='categoria'),
    path('registro/', views.registro, name='registro'),
    path('ingresar/', views.ingresar, name='ingresar'),
    path('salir/', views.salir, name='salir'),
    path('productos/<slug:slug>/', views.ProductoDetailView.as_view(), name='detalle-producto'),
    #path('productos/<slug:slug>/', views.detalle_producto, name='detalle-producto'),
    path('productos/nuevo', views.ProductoCreateView.as_view(), name='nuevo-producto'),
    #path('productos/nuevo', views.nuevo_producto, name='nuevo-producto'),
    path('productos/actualizar/<slug:slug>/', views.ProductoUpdateView.as_view(), name='editar-producto'),
    #path('productos/actualizar/<slug:slug>/', views.editar_producto, name='editar-producto'),
    path('productos/eliminar/<slug:slug>/', require_POST(views.ProductoDeleteView.as_view()), name='eliminar-producto'),
    #path('productos/eliminar/<slug:slug>/', views.eliminar_producto, name='eliminar-producto'),
    path('mi-carrito/', views.carrito, name='mi-carrito'),
    path('agregar-al-carrito/<slug:slug>/', views.agregar_al_carrito, name='agregar-al-carrito'),
    path('eliminar-del-carrito/(?P<int:pk>\d+)$/', views.eliminar_del_carrito, name='eliminar-del-carrito'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar-carrito'),
    path('aumentar-cantidad/(?P<int:pk>\d+)$/', views.aumentar_cantidad, name='aumentar-cantidad'),
    path('restar-cantidad/(?P<int:pk>\d+)$/', views.restar_cantidad, name='restar-cantidad'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/orden-confirmada/', views.orden_confirmada, name='orden-confirmada'),
    #path('mis-ordenes/', views.mis_ordenes, name='mis-ordenes'),
    path('mis-ordenes/', views.OrdenListView.as_view(), name='mis-ordenes'),
    #path('mis-ordenes/<uuid:codigo>/', views.detalle_orden, name='detalle-orden'),
    path('mis-ordenes/<uuid:codigo>', views.OrdenDetailView.as_view(), name='detalle-orden'),
    path('json', views.marcas_json, name='json'),
]