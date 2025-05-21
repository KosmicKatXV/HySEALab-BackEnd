from django.db import models
from asb.models import CustomUser

# Create your models here.

class Lab(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    in_use = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ['user','start_date']

    def __str__(self):
        return str(self.user.id)
class Volume(models.Model):
    owners = models.ManyToManyField(CustomUser,related_name='owners')
    viewers = models.ManyToManyField(CustomUser,related_name='viewers')
    replicaset = models.TextField()
    instanceid = models.TextField()
    in_use = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ['user','start_date']

    def __str__(self):
        return str(self.id)
