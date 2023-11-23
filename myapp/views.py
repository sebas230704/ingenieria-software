from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from .forms import *
from .models import *
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import WorkerOfferForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    workers = Worker.objects.all()
    return render(request, 'home.html', {'workers': workers})


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home') #cambiar home a la pagina que tiene el base diferente
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Password do not match'
        })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form' : AuthenticationForm
    })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form' : AuthenticationForm,
                'error' : 'Username or password is incorrect'
            })
            
        else:
            login(request, user)
            return redirect('home')

@login_required
def offer_worker(request):
    if request.method == 'GET':
        return render(request, 'beWorker.html', {
            'form' : WorkerOfferForm
        })
    else:
        try:
            form = WorkerOfferForm(request.POST)
            new_worker = form.save(commit=False)
            new_worker.user = request.user
            new_worker.email = request.user.email
            new_worker.save()
            return redirect('home')
        except ValueError:
            return render(request, 'beWorker.html', {
                'form' : WorkerOfferForm,
                'error' : "Verificar los datos"
            })
        
        
        