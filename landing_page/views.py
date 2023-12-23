from django.shortcuts import render
from django.contrib import messages

def load_homepage(request):
    
    # messages.info(request, "Three credits remain in your account.")

    return render(request, "landing_page/index.html")