from django.shortcuts import render

# Create your views here.

def login(request):
    if request.method == "POST":
        return
    
    return render(request, "login/login.html")