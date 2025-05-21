from django.db import models
from asb.models import CustomUser

# Create your models here.

class Lab(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    replicaset = models.TextField()
    instanceid = models.TextField()
    in_use = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ['user','start_date']


#implementar carpetas compartidas
    def __str__(self):
        return str(self.user.id)