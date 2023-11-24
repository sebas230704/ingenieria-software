from django import forms
from django.forms import ModelForm
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['email','phone', 'work', 'location', 'description', 'hours', 'profilePicture']
        
