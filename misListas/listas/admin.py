from django.contrib import admin
from .models import Lista

# Register your models here.
class ListaAdmin(admin.ModelAdmin):
    readonly_fields = ('creado', )

admin.site.register(Lista)