from .models import Categoria

def menu_categoria(request):
    categorias = Categoria.objects.all().order_by('nombre')
    context = {'categorias': categorias}
    return (context)