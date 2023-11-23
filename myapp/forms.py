from django import forms
from django.forms import ModelForm
from .models import *

class WorkerOfferForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['email','phone', 'work', 'location', 'resume', 'description', 'hours', 'profilePicture']