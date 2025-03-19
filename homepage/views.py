from django.shortcuts import render

# Create your views here.

def homepage(request):
    template = 'homepage/homepage.html'
    return render(request, template)

def auth_page(request):
    template = 'homepage/auth.html'
    return render(request, template)
