from django.db import models
from asb.models import CustomUser
from k8s.models import Lab
# Create your models here.


class Config(models.Model):
    name = models.TextField()
    field_name = models.FileField(upload_to=None, max_length=254)
    REQUIRED_FIELDS = ['user','lab','start_date']

    def __str__(self):
        return self.id

class Job(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    config = models.ForeignKey(Config, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ['user','lab','start_date']

    def __str__(self):
        return self.id