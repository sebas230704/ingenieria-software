from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class Worker(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.CharField(_("Phone"), max_length=20) 
    work = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    hours = models.CharField(max_length=100)
    profilePicture = models.ImageField(upload_to="images")
    has_resume = models.BooleanField(default=False)
    
class JobNotification(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    hiring_user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

# Create your models here.
