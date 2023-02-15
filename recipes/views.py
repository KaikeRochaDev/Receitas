from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html', {'name': 'KaikeRochaDev'})

def sobre(request):
    return HttpResponse('Sobre')


def contato(request):
    return HttpResponse('Contato')