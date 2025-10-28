from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from rest_framework.authtoken.models import Token
import k8s.k8s as k
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
   SPACE_QUOTA = models.TextField(default='512Mi')

   def __str__(self):
      return self.email

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def register_user_k8s(sender, instance=None, created=False, **kwargs):
   if created:
      email = instance.email
      id = str(instance.id)
      token = str(Token.objects.create(user=instance))
      #Create token
      k.createSecretToken(instance.id,token)
      #Create deployment
      invitation_list = []
      k.createLab(id,token,email,invitation_list)
      #Create PVC
      k.createPVC(id,instance.SPACE_QUOTA)
      #Create PV
      k.createPV(id,email)
      #Create Service
      k.createSvc(id)
   else:
      id = str(instance.id)
      #Delete PVC
      k.deletePVC(id)
      #Create new PVC
      k.createPVC(id,instance.SPACE_QUOTA)

        
@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_user_k8s(sender, instance, **kwargs):
   id = str(instance.id)
   #Delete token
   k.deleteSecretToken(id)
   #Delete deployment
   k.deleteLab(id)
   #Delete PVC
   k.deletePVC(id)
   #Delete PV
   k.deletePV(id)
   #Delete Service
   k.deleteSvc(id)


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

   def remove_relationship(host, guest):
      Invitation.objects.filter(
         from_person=host,
         to_person=guest).delete()
      return

   def get_invited(user):
      return Invitation.objects.filter(
        to_person=user)

   def get_invitations(user):
      return Invitation.objects.filter(
         from_person=user)