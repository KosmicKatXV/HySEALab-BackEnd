from django.db import models
from asb.models import CustomUser

# Create your models here.

class Lab(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    in_use = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ['user','start_date']


#implementar carpetas compartidas
    def __str__(self):
        return self.id