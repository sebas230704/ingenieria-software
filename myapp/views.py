from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from .forms import *
from .models import *
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
                # Crear el usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                
                # Guardar el perfil asociado al usuario
                worker = Worker.objects.create(idUser=user)
                
                # Iniciar sesión
                login(request, user)
                
                return redirect('home')
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

def be_worker(request):
    if request.method == 'GET':
        return render(request, 'beWorker.html', {
            'form' : WorkerForm
        })
    else:
        try:
            form = WorkerForm(request.POST, request.FILES)  # Aquí está la corrección
            new_worker = form.save(commit=False)
            new_worker.idUser = request.user
            new_worker.save()
            return redirect('worker_list')
        except ValueError:
            return render(request, 'beWorker.html', {
            'form' : WorkerForm,
            'error' : "Please validate your information"
        })

def worker_list(request):
    workers = Worker.objects.all()
    return render(request, 'worker_list.html', {'workers' : workers})

def hire_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    if request.method == 'POST':
        message = request.POST.get('message', '')
        JobNotification.objects.create(worker=worker, hiring_user=request.user, message=message)
        return redirect('worker_list')
    else:
        return render(request, 'hire_worker.html', {'worker': worker})
    
def mis_contratos(request):
    contratos = JobNotification.objects.filter(worker__idUser=request.user)
    return render(request, 'misContratos.html', {'contratos': contratos})