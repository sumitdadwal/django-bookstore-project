from distutils.command.upload import upload
from statistics import mode, quantiles
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image=models.ImageField(upload_to='admins')
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name