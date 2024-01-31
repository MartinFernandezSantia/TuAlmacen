from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
import re
from .models import InfoUser
from django.http import JsonResponse

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

        registerName = request.POST.get("registerName")
        registerSurname = request.POST.get("registerSurname")
        registerEmail = request.POST.get("registerEmail")
        registerPassword = request.POST.get("registerPassword")
        registerPassword2 = request.POST.get("registerPassword2")
        registerPhone = request.POST.get("registerPhone")


        name_pattern = r"^[a-zA-Z0-9@.+_-]{1,150}$" # Regex to comply with Django username requirements
        password_pattern = "^(?=.*[A-Z])(?=.*\d).{8,}$" # Needs one upper, one number and at least 8 characters
        email_pattern = r"^\S+@\S+\.\S+$" # Needs to match email pattern

        if not re.match(name_pattern, registerName):
            messages.error(request, f'Lo sentimos, pero los nombres de usuario no pueden contener más de 150 caracteres o caracteres especiales fuera de @ - _ . +.')
            return JsonResponse({"redirect_url": request.path_info})
        elif User.objects.filter(email=registerEmail).exists() or not re.match(email_pattern, registerEmail):
            messages.error(request, f'"{registerEmail}" ya esta en uso o no coincide con el formato de un mail.')
            return JsonResponse({"redirect_url": request.path_info})
        elif not re.match(password_pattern, registerPassword):
            messages.error(request, "La contraseña ingresada es muy debil o no cumple los requisitos.")
            return JsonResponse({"redirect_url": request.path_info})
        elif registerPassword != registerPassword2:
            messages.error(request, "Las contraseñas no coinciden.")
            return JsonResponse({"redirect_url": request.path_info})
        
        new_user = User.objects.create_user(
            username=registerName, 
            last_name=registerSurname, 
            email=registerEmail, 
            password=registerPassword)

        info_user = InfoUser(user=new_user, phone_number=registerPhone)
        info_user.save()

        messages.success(request,"Tu cuenta ha sido exitosamente creada!!")
        return JsonResponse({"redirect_url": "/login"})


    return render(request, "login/register.html")

@login_required
def logout_request(request):
    logout(request)

    messages.success(request,"¡Hasta la próxima! Esperamos verte pronto.")
    return HttpResponseRedirect('/')