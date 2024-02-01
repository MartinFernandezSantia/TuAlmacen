from django.shortcuts import render
from django.contrib import messages

def load_homepage(request):

    return render(request, "landing_page/index.html")