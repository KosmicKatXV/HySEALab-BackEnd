from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from rest_framework.authtoken.models import Token
import k8s as k
class CustomUserManager(BaseUserManager):
   def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

   def create_user(self, email, password, **extra_fields):
      extra_fields.setdefault("is_staff", False)
      extra_fields.setdefault("is_superuser", False)
      return self._create_user(email, password, **extra_fields)

   def create_superuser(self, email, password, **extra_fields):
      extra_fields.setdefault("is_staff", True)
      extra_fields.setdefault("is_superuser", True)
      if extra_fields.get("is_staff") is not True:
         raise ValueError("Superuser must have is_staff=True.")
      if extra_fields.get("is_superuser") is not True:
         raise ValueError("Superuser must have is_superuser=True.")
      return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
   email = models.EmailField(max_length=100, unique=True)
   username = None
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['password','first_name','last_name']
   objects = CustomUserManager()
   invited_users = models.ManyToManyField("self",
                                          through='Invitation',
                                          symmetrical=False,
                                          related_name='invited')

   def __str__(self):
      return self.email

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def register_user_k8s(sender, instance=None, created=False, **kwargs):
   if created:
      email = user.__str__()
      id = str(user.id)
      token = Token.objects.create(user=instance)
      #Create token
      k.createSecretToken(instance.id,token.key)
      #Create deployment
      invitation_list = []
      #Create PVC
      k.createPVC(id)
      #Create PV
      k.createPV(id,email)
      #Create Service
      k.createSvc(id)
        
@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_user_k8s(sender, instance, **kwargs):
   k.deleteSecretToken(instance.id)

class Invitation(models.Model):
   from_person = models.ForeignKey(CustomUser, related_name='from_people',on_delete=models.CASCADE)
   to_person = models.ForeignKey(CustomUser, related_name='to_people',on_delete=models.CASCADE)
   class Meta:
        constraints = [
            models.UniqueConstraint(fields=["from_person", "to_person"], name='unique_intro'),
        ]

   def add_relationship(self, person):
      relationship = Invitation.objects.create(
         from_person=self,
         to_person=person)
      return relationship

   def remove_relationship(user, person):
      Invitation.objects.filter(
         from_person=user,
         to_person=person).delete()
      return

   def get_invited(user):
      return Invitation.objects.filter(
        to_person=user)

   def get_invitations(user):
      return Invitation.objects.filter(
         from_person=user)