import uuid
from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	email = models.EmailField(max_length=254, unique=True)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	class Meta:
		verbose_name = 'usuario'
		verbose_name_plural = 'usuarios'
	
	def __str__(self):
		return self.email


class Categoria(models.Model):
	nombre = models.CharField(unique=True, max_length=30)
	slug = AutoSlugField(populate_from='nombre', unique=True, always_update=False)
	fecha_carga = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name = 'categoría'
		verbose_name_plural = 'categorías'

	def __str__(self):
		return self.nombre
	
	def get_absolute_url(self):
		return reverse('webapp:categoria', kwargs={'slug': self.slug})


class Marca(models.Model):
	nombre = models.CharField(unique=True, max_length=30)
	slug = AutoSlugField(populate_from='nombre', unique=True, always_update=False)
	fecha_carga = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'marca'
		verbose_name_plural = 'marcas'

	def __str__(self):
		return self.nombre


class Producto(models.Model):
	modelo = models.CharField(unique=True, max_length=100)
	marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
	slug = AutoSlugField(populate_from='titulo', unique=True, always_update=False)
	precio = models.DecimalField(max_digits=10, decimal_places=2)
	descripcion = models.TextField(max_length=1000)
	imagen = models.ImageField(upload_to='productos/')
	fecha_carga = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'producto'
		verbose_name_plural = 'productos'

	def __str__(self):
		return '%s - %s (%s)' % (self.marca, self.modelo, self.categoria)

	def get_absolute_url(self):
		return reverse('webapp:detalle-producto', kwargs={'slug': self.slug})

	def titulo(self):
		return '%s %s' % (self.marca, self.modelo)


class Carrito(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	numero_productos = models.PositiveIntegerField(default=0)
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'carrito'
		verbose_name_plural = 'carritos'

	def __str__(self):
		return  str(self.usuario)


class CarritoItem(models.Model):
	carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
	precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)
	cantidad = models.IntegerField(default=1)
	precio_total = models.DecimalField(max_digits=10, decimal_places=2)
	ordenado = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'carrito item'
		verbose_name_plural = 'carritos items'

	def __str__(self):
		return '%s' % (self.producto)

	def get_absolute_url(self):
		return reverse('webapp:detalle-producto', kwargs={'slug': self.producto.slug})

	def set_precio_unidad(self):
		self.precio_unidad = self.producto.precio
		self.save()

	def set_precio_total(self):
		self.precio_total = self.precio_unidad * self.cantidad
		self.save()

	def aumentar_cantidad(self):
		self.cantidad += 1
		self.set_precio_total()
		
	def restar_cantidad(self):
		self.cantidad -= 1
		self.set_precio_total()


class DireccionEnvio(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	nombre = models.CharField(max_length=150, verbose_name='nombre')
	apellido = models.CharField(max_length=50, verbose_name='apellido')
	telefono = models.CharField(max_length=30, verbose_name='teléfono')
	direccion = models.CharField(max_length=150, verbose_name='dirección')
	pais = models.CharField(max_length=20, verbose_name='país')
	provincia = models.CharField(max_length=50, verbose_name='provincia')
	codigo_postal = models.CharField(max_length=20, verbose_name='código postal')

	class Meta:
		verbose_name = 'dirección de envío'
		verbose_name_plural = 'direcciones de envío'

	def __str__(self):
		return '(%s) - %s, %s' % (self.direccion, self.provincia, self.codigo_postal)


class Orden(models.Model):
	codigo = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	precio_total = models.DecimalField(max_digits=10, decimal_places=2)
	fecha_de_orden = models.DateTimeField(auto_now_add=True)
	direccion_envio = models.ForeignKey(DireccionEnvio, on_delete=models.SET_NULL, null=True)

	class Meta:
		verbose_name = 'orden'
		verbose_name_plural = 'ordenes'

	def __str__(self):
		return 'Esta orden pertenece a %s' % (self.usuario)

	def get_absolute_url(self):
		return reverse('webapp:detalle-orden', kwargs={'codigo': self.codigo})

	def get_orden_items(self):
		return self.ordenitem_set.all()


class OrdenItem(models.Model):
	orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
	carrito_item = models.ForeignKey(CarritoItem, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'orden item'
		verbose_name_plural = 'orden items'

	def __str__(self):
		return '%s' % (self.carrito_item)

	def get_absolute_url(self):
		return reverse('webapp:detalle-producto', kwargs={'slug': self.carrito_item.producto.slug})
	
	def get_precio_unidad(self):
		return self.carrito_item.precio_unidad
	
	def get_precio_total(self):
		return self.carrito_item.precio_total

	def get_cantidad(self):
		return self.carrito_item.cantidad