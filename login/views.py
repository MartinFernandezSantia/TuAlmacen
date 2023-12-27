from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User 

# Create your views here.

# def login(request):
#     if request.method == "POST":
#         return
    
#     return render(request, "login/login.html")

# Decorator to check if user is anonymous
def is_anonymous(func):
    def check(*args, **kwargs):
        if not args[0].user.is_anonymous:
            messages.error(args[0],"Debe cerrar sesión para poder acceder")
            return HttpResponseRedirect("/") 
        
        return func(*args, **kwargs)
    return check

@is_anonymous
def login(request):
    if request.method == "POST":
        email = request.POST["loginEmail"]
        password = request.POST["loginPassword"]
        print(email, password)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"¡Hola! ¡Qué bueno verte por aquí de nuevo {user.get_username()}!")
            return HttpResponseRedirect('/')

        messages.error(request, "El usuario o contraseña ingresados son incorrectos")
        return HttpResponseRedirect(request.path_info)
    params = {}
    params["nombre_sitio"] = "Iniciar sesión"
    return render(request, "login/login.html")


def register(request):
    return render(request, "login/register.html")