from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='miembro_grupo')
def miembro_grupo(usuario, nombre_grupo):
    grupo = Group.objects.get(name=nombre_grupo)
    return True if grupo in usuario.groups.all() else False