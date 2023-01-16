from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Lista(models.Model):
    nombre_lista = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
      def __str__(self):
        return self.nombre_lista + ' - ' + self.user.username

class Item(models.Model):
  item = models.ForeignKey(Lista, on_delete=models.CASCADE)
  descripcion_item = models.CharField(max_length=1000)
  creado = models.DateTimeField(auto_now_add=True)
  fechacompletado = models.DateTimeField(null=True, blank=True)
  fecha_recordatorio = models.DateField(null=True, blank=True)
  hora_recordatorio = models.TimeField(null=True, blank=True)
  completado = models.BooleanField(default=False)