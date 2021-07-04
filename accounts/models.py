from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    birthday = models.DateField(null=True,blank=True)
    