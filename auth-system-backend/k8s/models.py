from django.db import models
from asb.models import CustomUser

# Create your models here.

class Lab(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ['user','start_date']

    def __str__(self):
        return self.id