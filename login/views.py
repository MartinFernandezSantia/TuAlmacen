from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
import re

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

@is_anonymous
def register(request):
    if request.method == "POST":
        # all_post_values = request.POST

        # # You can loop through the values
        # for key, value in all_post_values.items():
        #     print(f"Field '{key}' has value '{value}'")
        name = request.POST.get("registerName")
        surname = request.POST.get("registerSurname")
        email = request.POST.get("registerEmail")
        password1 = request.POST.get("registerPassword")
        password2 = request.POST.get("registerPassword2")

        password_pattern = "^(?=.*[A-Z])(?=.*\d).{8,}$" # Needs one upper, one number and at least 8 characters
        email_pattern = r"^\S+@\S+\.\S+$" # Needs to match email pattern

        if User.objects.filter(email=email).exists() or not re.match(email_pattern, email):
            messages.error(request, f'"{email}" ya esta en uso o no coincide con el formato de un mail.')
            return HttpResponseRedirect("/")
        elif not re.match(password_pattern, password1):
            messages.error(request, "La contraseña ingresada es muy debil o no cumple los requisitos")
            return HttpResponseRedirect(request.path_info)
        elif password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return HttpResponseRedirect(request.path_info)

        User.objects.create_user(first_name=name, email=email, password=password1)

        messages.success(request,"Tu cuenta ha sido exitosamente creada!!")
        return HttpResponseRedirect('/login')

    return render(request, "login/register.html")

@login_required
def logout_request(request):
    logout(request)

    messages.success(request,"¡Hasta la próxima! Esperamos verte pronto.")
    return HttpResponseRedirect('/')