from django.db import models
from django.utils.translation import gettext as _


class Worker(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(_("Phone"), max_length=20) 
    work = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    hours = models.CharField(max_length=100)
    profilePicture = models.ImageField(upload_to='images/', default="default.png")
    has_resume = models.BooleanField(default=False)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    

# Create your models here.
