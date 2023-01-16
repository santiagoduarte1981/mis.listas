from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Lista, Item
from django.urls import reverse
from django.contrib import messages
from .forms import *
from .forms import ListaForm, ItemForm

from django.shortcuts import render, redirect
from django.http import HttpResponse

#sugerencias
from django.conf import settings
import smtplib
from email.mime.text import MIMEText

#enviar lista por mail
import chardet
from io import BytesIO
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet

import os
       
def home(request):
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()    
            return redirect('iniciar_sesion')
    else:
        form = RegistrarUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'iniciar_sesion.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'iniciar_sesion.html', {"form": AuthenticationForm, "error": "Usuario o contraseña incorrecta"})

        login(request, user)
        return redirect('home')

@login_required
def salir(request):
    logout(request)
    messages.info(request, "Cerraste sesión exitosamente")
    return redirect('/')
    
@login_required
def listas(request):
    listas = Lista.objects.filter(user=request.user)
    items = Item.objects.all()
    context = {
        'listas': listas,
        'items': items
    }
    return render(request, 'listas.html', context)


@login_required
def crear_lista(request):
    if request.method == "GET":
        return render(request, 'crear_lista.html', {"form": ListaForm})
    else:
        try:
            form = ListaForm(request.POST)
            new_lista = form.save(commit=False)
            new_lista.user = request.user
            new_lista.save()
            return redirect('listas')
        except ValueError:
            return render(request, 'crear_lista.html', {"form": ListaForm, "error": "Error creating lista."})

@login_required
def crear_item(request, pk):
    lista = get_object_or_404(Lista, pk=pk)
    if request.method == "GET":
        return render(request, 'crear_item.html', {"form": ItemForm, "lista": lista})
    else:
        try:
            form = ItemForm(request.POST)
            new_item = form.save(commit=False)
            new_item.item = lista
            new_item.save()
            url = reverse('crear_item', kwargs={'pk': lista.pk})
            return redirect('listas')
        except ValueError:
            return render(request, 'crear_item.html', {"form": ItemForm, "error": "Error creating item.", "lista": lista})

@login_required    
def modificar_item(request, item_id):
    if request.method == 'GET':
        item = get_object_or_404(Item, pk=item_id)
        form = ItemForm(instance=item)
        return render(request, 'modificar_item.html', {'item': item, 'form': form})
    else:
        try:
            item = get_object_or_404(Item, pk=item_id)
            form = ItemForm(request.POST, instance=item)
            form.save()
            return redirect('listas')
        except ValueError:
            return render(request, 'modificar_item.html', {'item': item, 'form': form, 'error': 'Error modificando el ítem.'})

@login_required
def borrar_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('listas')
    
@login_required
def lista_cambiar_nombre(request, lista_id):
    if request.method == 'GET':
        lista = get_object_or_404(Lista, pk=lista_id, user=request.user)
        form = ListaForm
        return render(request, 'lista_cambiar_nombre.html', {'lista': lista, 'form': form})
    else:
        try:
            lista = get_object_or_404(Lista, pk=lista_id, user=request.user)
            form = ListaForm(request.POST, instance=lista)
            form.save()
            return redirect('listas')
        except ValueError:
            return render(request, 'lista_cambiar_nombre.html', {'lista': lista, 'form': form, 'error': 'Error cambiando el nombre de la lista.'})

@login_required
def lista_nombre(request):
    listas = Lista.objects.filter(user=request.user)
    context = {
        'listas': listas,
    }
    return render(request, 'lista_nombre.html', context)

@login_required
def eliminar_lista(request, lista_id):
    lista = get_object_or_404(Lista, pk=lista_id, user=request.user)
    if request.method == 'POST':
        lista.delete()
        return redirect('/')

@login_required
def borrar_lista(request):
    listas = Lista.objects.filter(user=request.user)
    context = {
        'listas': listas,
    }
    return render(request, 'borrar_lista.html', context)


def sugerencias(request):
    if request.method == 'POST':
        email_to = "mis.listas@outlook.com"
        subject = request.POST['subject']
        message = request.POST['message']

        try:
            mail_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mail_server.starttls()
            mail_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            mensaje = MIMEText(message)
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = subject

            mail_server.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
            render(request, 'listas.html', {'alert': 'swal("Mensaje enviado exitosamente!", "Muchas gracias por escribirnos", "success")'})
            return redirect('listas')

        except Exception as e:
            print(e)
            render(request, 'listas.html', {'alert': 'swal("El mensaje no ha podido enviarse", "Prueba otra vez por favor", "error")'})
            return redirect('listas')
    else:
        return render(request, 'sugerencias.html')

@login_required
def enviar_lista(request):
    listas = Lista.objects.filter(user=request.user)
    context = {
        'listas': listas,
    }
    return render(request, 'enviar_lista.html', context)

@login_required
def enviar_lista_por_correo(request, lista_id):
    lista = get_object_or_404(Lista, pk=lista_id)
    items = Item.objects.filter(item=lista_id)
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 12
    style.leading = 18


    # Crear el pdf
    pdf = BytesIO()
    doc = SimpleDocTemplate(pdf, pagesize=letter, fontSize = 12)
    elements = []

    # Crear el mensaje por mail
    mensaje_lista = 'Hola.' + "\n" + 'Encontrará su lista también como archivo adjunto' + "\n" + "\n" + lista.nombre_lista + "\n"
    for item in items:
        if item.completado==True:
            mensaje_lista += '- ' + item.descripcion_item + " ✔" + "\n"
        else:
            mensaje_lista += '- ' + item.descripcion_item + "\n"

    # Estilos pdf
    elements.append(Paragraph('<b>' + lista.nombre_lista + '</b>', style))
    elements.append(Spacer(1, 12))
    for item in items:
        if item.completado:
            elements.append(Paragraph("- <strike>" + item.descripcion_item + "</strike>" + " ✔", style))
        else:
            elements.append(Paragraph("- " + item.descripcion_item, style))
    doc.build(elements)
    pdf.seek(0)

    # Enviar mail
    email = EmailMessage(
        'Lista: ' + lista.nombre_lista,
        mensaje_lista,
        settings.EMAIL_HOST_USER,
        [request.user.email],
        ['bcc@example.com'],
        reply_to=['another@example.com'],
        headers={'Message-ID': 'foo'},
    )
    email.attach('lista.pdf', pdf.read(), 'application/pdf')
    email.send()
#copia el txt que mando el usuario por pdf
    if not os.path.exists(f'listas/static/listas_predefinidas/{lista.nombre_lista}.txt'):
        with open(f'listas/static/listas_predefinidas/{lista.nombre_lista}.txt', 'w') as f:
            for item in items:
                f.write(item.descripcion_item + '\n')
    else:
        pass

    messages.success(request, 'Lista enviada exitosamente')
    return redirect('listas')

@login_required
def listas_predefinidas(request):
    path = 'listas/static/listas_predefinidas/'
    listas_predefinidas = os.listdir(path)
    listas = []
    for archivo in listas_predefinidas:
        nombre, _ = os.path.splitext(archivo)
        listas.append(nombre)
    context = {'listas': listas}
    return render(request, 'listas_predefinidas.html', context)

@login_required
def importar_lista_predefinida(request, nombre_archivo):
    # Obtener el nombre del archivo sin la extensión .txt
    nombre_lista = nombre_archivo.strip('.txt')
    def detect_encoding(filepath):
        with open(filepath, 'rb') as file:
            result = chardet.detect(file.read())
            return result['encoding']
    
    encoding = detect_encoding(f'listas/static/listas_predefinidas/{nombre_archivo}.txt')
    # Abrir el archivo y leer su contenido
    with open(f'listas/static/listas_predefinidas/{nombre_archivo}.txt', 'r', encoding=encoding) as file:
        items = file.readlines()

    # Crear una instancia de Lista con el nombre del archivo
    lista = Lista(nombre_lista=nombre_lista)
    lista.user = request.user
    lista.save()
    for item in items:
        item = Item(descripcion_item=item, item=lista)
        item.save()
    # Redirigir al usuario a la página de listas
    messages.success(request,'Lista importada correctamente')
    return redirect('listas')

@login_required
def fecha_recordatorio(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        fecha_recordatorio = request.POST.get('fecha_recordatorio')
        item.fecha_recordatorio = fecha_recordatorio
        item.save()
        messages.success(request, 'Fecha establecida correctamente')
        return redirect('listas')
    return render(request, 'fecha_recordatorio.html', {'item': item})

@login_required
def hora_recordatorio(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        hora_recordatorio = request.POST.get('hora_recordatorio')
        item.hora_recordatorio = hora_recordatorio
        item.save()
        messages.success(request, 'Hora establecida correctamente')
        return redirect('listas')
    return render(request, 'hora_recordatorio.html', {'item': item})

#Modo oscuro/claro
@login_required
def set_mode(request):
    if request.method == 'POST':
        mode = request.POST.get('mode')
        request.session['dark_mode'] = mode
    return HttpResponse()