from django.contrib import admin
from django.urls import path, include
from listas import views
from django.contrib.auth import views as auth_views
from listas.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('registro/',views.registro,name='registro'),
    
    path('listas/', views.listas, name='listas'),
    path('logout/', views.salir, name='logout'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),

    path('crear_lista/', views.crear_lista, name='crear_lista'),
    path('items/<int:pk>/create/', views.crear_item, name='crear_item'),
    path("items/<int:item_id>/modificar", views.modificar_item, name="modificar_item"),
    path('lista_nombre', views.lista_nombre, name='lista_nombre'),
    path('listas/<int:lista_id>', views.lista_cambiar_nombre, name='lista_cambiar_nombre'),
    path('listas/borrar', views.borrar_lista, name='borrar_lista'),
    path('listas/<int:lista_id>/eliminar', views.eliminar_lista, name='eliminar_lista'),
    path('items/<int:item_id>/borrar', views.borrar_item, name='borrar_item'),
    
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html')),    
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(success_url='/')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    
    path('sugerencias/', views.sugerencias, name='sugerencias'),
    path('listas/enviar', views.enviar_lista, name='enviar_lista'),
    path('enviar_lista_por_correo/<int:lista_id>/', views.enviar_lista_por_correo, name='enviar_lista_por_correo'),
    path('listas_predefinidas/', views.listas_predefinidas, name='listas_predefinidas'),
    path('importar_lista_predefinida/<str:nombre_archivo>/', views.importar_lista_predefinida, name='importar_lista_predefinida'),
   
    path('fecha_recordatorio/<int:item_id>', views.fecha_recordatorio, name='fecha_recordatorio'),
    path('hora_recordatorio/<int:item_id>', views.hora_recordatorio, name='hora_recordatorio'),
    path('set_mode/', views.set_mode, name='set_mode'),
]


