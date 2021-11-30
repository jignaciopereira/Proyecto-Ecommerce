from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, AccessMixin
from django.contrib.auth.models import Group
from .models import CarritoItem, Marca, Producto, Carrito, Orden, OrdenItem, Categoria
from .forms import ProductoForm, ContactoForm, CustomUserCreationForm, CustomAuthenticationForm, DireccionEnvioForm


'''
def index(request, template_name='webapp/index.html'):
    productos = Producto.objects.order_by('-fecha_carga')[:10]
    context = {'productos': productos}
    return render(request, template_name, context)
'''


class ProductoListView(ListView):
    template_name = 'webapp/index.html'
    context_object_name = 'productos'

    def get_queryset(self):
        return Producto.objects.order_by('-fecha_carga')[:10]


def buscar_producto(request, template_name='webapp/busqueda.html'):
    if 'search' in request.GET and request.GET['search']:
        consulta = request.GET['search']
        productos = Producto.objects.filter(slug__icontains=consulta.replace(' ', '-')).order_by('modelo')
        paginator = Paginator(productos, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'consulta': consulta}
        return render(request, template_name, context)
    else:
        return render(request, template_name)


'''
def filtrar_categoria(request, slug, template_name='webapp/productos-por-categoria.html'):
    categoria = Categoria.objects.get(slug=slug)
    productos = categoria.producto_set.all().order_by('modelo')
    paginator = Paginator(productos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'categoria': categoria}
    return render(request, template_name, context)
'''


class ProductoCategoriaListView(ListView):
    template_name = 'webapp/productos-por-categoria.html'
    paginate_by = 6

    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, slug=self.kwargs.get('slug'))
        return Producto.objects.filter(categoria=self.categoria).order_by('modelo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        return context


'''
def detalle_producto(request, slug, template_name='webapp/detalle-producto.html'):
    if request.user.is_staff:
        return redirect(reverse('webapp:editar-producto', kwargs={'slug': slug}))
    else:
        producto = get_object_or_404(Producto, slug=slug)
        context = {'producto': producto}
        return render(request, template_name, context)
'''


class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'webapp/detalle-producto.html'



@permission_required('webapp.add_producto', raise_exception=True)
def nuevo_producto(request, template_name='webapp/nuevo-producto.html'):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            extension = producto.imagen.name.split('.')[-1]
            producto.imagen.name = f'{producto.titulo().replace(" ", "-").lower()}.{extension}'
            producto.save()
            return redirect('webapp:index')
    else:
        form = ProductoForm()
    context = {'form': form}
    return render(request, template_name, context)



class ProductoCreateView(PermissionRequiredMixin, AccessMixin, CreateView):
    model = Producto
    template_name = 'webapp/nuevo-producto.html'
    form_class = ProductoForm
    permission_required = 'webapp.add_producto'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            extension = producto.imagen.name.split('.')[-1]
            producto.imagen.name = f'{producto.titulo().replace(" ", "-").lower()}.{extension}'
            producto.save()
            return redirect('webapp:index')
        return render(request, self.template_name, {'form': form})



@permission_required('webapp.change_producto', raise_exception=True)
def editar_producto(request, slug, template_name='webapp/editar-producto.html'):
    producto = get_object_or_404(Producto, slug=slug)    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if request.FILES:   
            nueva_imagen = request.FILES.get('imagen')
            extension = nueva_imagen.name.split('.')[-1]
            if extension == 'jpg' or extension == 'png':
                producto.imagen.delete()
                nueva_imagen.name = f'{producto.titulo().replace(" ", "-").lower()}.{extension}'
        if form.is_valid():
            form.save(commit=True)
            return redirect((reverse('webapp:detalle-producto', kwargs={'slug': slug})))
    else:
        form = ProductoForm(instance=producto)
    context = {'form': form}
    return render(request, template_name, context)



class ProductoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Producto
    template_name = 'webapp/editar-producto.html'
    form_class = ProductoForm
    permission_required = 'webapp.change_producto'

    def post(self, request, *args, **kwargs):
        if request.FILES:
            nueva_imagen = request.FILES.get('imagen')
            extension = nueva_imagen.name.split('.')[-1]
            if extension == 'jpg' or extension == 'png':
                self.object = self.get_object()
                self.object.imagen.delete()
                nueva_imagen.name = f'{self.object.titulo().replace(" ", "-").lower()}.{extension}'
        return super().post(request, *args, **kwargs)

    

@require_POST
@permission_required('webapp.delete_producto', raise_exception=True)
def eliminar_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    if request.method == 'POST':
        producto.imagen.delete()
        producto.delete() 
        return redirect('webapp:index')



class ProductoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Producto
    permission_required = 'webapp.delete_producto'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.imagen.delete()
        self.object.delete()
        return redirect('webapp:index')


def contacto(request, template_name='webapp/contacto.html'):
    form = ContactoForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            correo_rtte = form.cleaned_data['correo']
            asunto = form.cleaned_data['asunto']
            body = form.cleaned_data['mensaje']
            mensaje = f'De {nombre} <{correo_rtte}> \n\n{body}'
            email = EmailMessage(subject=asunto, body=mensaje, reply_to=[correo_rtte], to=['mi_correo@gmail.com'])           
            try:
                email.send()
                context = {'form': form, 'correo_enviado': True}
                print(mensaje)
            except:
                context = {'form': form, 'correo_enviado': False}
    return render(request, template_name, context)


def registro(request, template_name='webapp/registro.html'):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            usuario = form.save(commit=True)
            grupo = Group.objects.get(name='Cliente')
            usuario.groups.add(grupo)
            login(request, usuario)
            Carrito.objects.get_or_create(usuario=request.user)
            return redirect('webapp:index')
    return render(request, template_name, {'form': form})
   

def ingresar(request, template_name='webapp/ingresar.html'):
    form = CustomAuthenticationForm(request, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = authenticate(username=user, password=password)
            if usuario is not None:
                login(request, usuario)
                if 'next' in request.GET and request.GET['next']:
                    url = request.GET['next']
                    return redirect(url)
                else:
                    return redirect('webapp:index')
    return render(request, template_name, {'form': form})


def salir(request):
    logout(request)
    return redirect('webapp:index')


@login_required
@permission_required('webapp.view_carrito', raise_exception=True)
def carrito(request, template_name='webapp/mi-carrito.html'):
    carrito = Carrito.objects.get(usuario=request.user)
    items = carrito.carritoitem_set.filter(ordenado=False)
    if items:
        for item in items:
            item.set_precio_unidad()
            item.set_precio_total()
        precio_total = items.aggregate(Sum('precio_total'))
        items_total = items.aggregate(Sum('cantidad'))
        carrito.total = precio_total['precio_total__sum']
        carrito.numero_productos = items_total['cantidad__sum']
        carrito.save(update_fields=['total', 'numero_productos'])
    else:
        carrito.total = 0
        carrito.numero_productos = 0
        carrito.save(update_fields=['total', 'numero_productos'])
    context = {'items': items, 'carrito_total': carrito.total}
    return render(request, template_name, context)


@login_required
@permission_required('webapp.add_carritoitem', raise_exception=True)
def agregar_al_carrito(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    try: 
        item_existente = CarritoItem.objects.get(producto=producto, carrito__usuario=request.user, ordenado=False)
        item_existente.aumentar_cantidad()
    except ObjectDoesNotExist: 
        carrito = Carrito.objects.get(usuario=request.user)
        CarritoItem.objects.create(carrito=carrito, producto=producto, precio_unidad=producto.precio, precio_total=producto.precio)
    finally:
        return redirect('webapp:mi-carrito')


@require_POST
@login_required
def eliminar_del_carrito(request, pk):
    get_object_or_404(CarritoItem, pk=pk).delete()
    return redirect('webapp:mi-carrito')


@require_POST
@login_required
def vaciar_carrito(request):
    CarritoItem.objects.filter(carrito__usuario=request.user, ordenado=False).delete()
    return redirect('webapp:mi-carrito')


@login_required
def aumentar_cantidad(request, pk):
    producto = get_object_or_404(CarritoItem, pk=pk)
    producto.aumentar_cantidad()
    return redirect('webapp:mi-carrito')


@login_required
def restar_cantidad(request, pk):
    producto = get_object_or_404(CarritoItem, pk=pk)
    if producto.cantidad == 1:
        return redirect('webapp:mi-carrito')
    else:
        producto.restar_cantidad()
        return redirect('webapp:mi-carrito')


def acerca_de(request, template_name='webapp/acerca-de.html'):
    return render(request, template_name)


@login_required
def checkout(request, template_name='webapp/checkout.html'):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    productos = CarritoItem.objects.filter(carrito__usuario=request.user, ordenado=False)
    if productos:
        form = DireccionEnvioForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                direccion_envio = form.save(commit=False)
                direccion_envio.usuario = request.user
                direccion_envio.save()
                orden = Orden.objects.create(usuario=request.user, direccion_envio=direccion_envio, precio_total=carrito.total)
                for producto in productos:
                    OrdenItem.objects.create(orden=orden, carrito_item=producto)            
                productos.update(ordenado=True)
                return redirect('webapp:orden-confirmada')
        context = {'form':form, 'productos': productos, 'carrito': carrito}
        return render(request, template_name, context)
    else:
        return redirect('webapp:mi-carrito')


def orden_confirmada(request, template_name='webapp/orden-confirmada.html'):
    return render(request, template_name)


'''
@login_required
def mis_ordenes(request, template_name='webapp/mis-ordenes.html'):
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha_de_orden')
    context = {'ordenes': ordenes}
    return render(request, template_name, context)
'''


class OrdenListView(PermissionRequiredMixin, ListView):
    context_object_name = 'ordenes'
    template_name = 'webapp/mis-ordenes.html'
    permission_required = 'webapp.view_orden'

    def get_queryset(self):
        return Orden.objects.filter(usuario=self.request.user).order_by('-fecha_de_orden')


'''
@login_required
def detalle_orden(request, codigo, template_name='webapp/detalle-orden.html'):
    orden = Orden.objects.get(codigo__exact=codigo)
    context = {'orden': orden}
    return render(request, template_name, context)
'''


class OrdenDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'webapp/detalle-orden.html'
    permission_required = 'webapp.view_orden'

    def get_object(self, queryset=None):
        return Orden.objects.get(codigo=self.kwargs.get('codigo'))


def marcas_json(request):
    data = serializers.serialize('jsonl', Marca.objects.all())
    print(data)
    return HttpResponse(data)