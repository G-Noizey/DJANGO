import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserLoginForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    """
    Vista para el registro de usuarios.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Autentica al usuario después de registrarlo
            return redirect('home')  # Redirige a la página principal
    else:
        form = CustomUserCreationForm()  # Carga un formulario vacío si no es POST
    return render(request, 'register.html', {'form': form})  # Asegúrate de usar la ruta correcta


def login_view(request):
    """
    Vista para el inicio de sesión de usuarios.
    """
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Obtiene al usuario autenticado
            login(request, user)  # Inicia sesión
            return redirect('home')  # Redirige a la página principal
    else:
        form = CustomUserLoginForm()  # Carga un formulario vacío si no es POST
    return render(request, 'login.html', {'form': form})  # Asegúrate de usar la ruta correcta


def logout_view(request):
    logout(request)
    
    message = message(
        "info", 
        "Se ha cerrado sesión exitosamente", 
        200, 
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8MIbugIhZBykSmQcR0QPcfnPUBOZQ6bm35w&s"
    )
    
    return render(request, "login.html", {
        "message": json.dumps(message.to_dict())
    })



@login_required
def home_view(request):
    """
    Vista para la página principal (protegida para usuarios autenticados).
    """
    return render(request, 'home.html')  # Asegúrate de usar la ruta correcta
