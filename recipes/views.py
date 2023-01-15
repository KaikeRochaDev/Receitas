from django.shortcuts import render

# Create your views here.
def home(request):
    return HttpResponse('Home')

def sobre(request):
    return HttpResponse('Sobre')

def contato(request):
    return HttpResponse('Contato')