from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime


# Create your models here.

class UserProfile(models.Model):
    phone = PhoneNumberField(blank=True)
    user_django_profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):

      return f'{self.user_django.first_name} , {self.user_django.last_name}\n{str(self.phone)}'

class MechanicProfile(models.Model):
    phone = PhoneNumberField(blank=True)
    mec_django_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=500)
    longitud = models.FloatField(default = 0)
    latitud = models.FloatField(default = 0)

    def __str__(self):

      return f'{self.django_mec_user.first_name} , {self.django_mec_user.last_name}\n, {self.skills},{str(self.phone)}, {self.latitud}, {self.longitud} '

class Post(models.Model):
   status_choices = (
      (0, 'not assigned'),
      (1, 'accepted'),
      (2, 'finished')
   )
   comment = models.TextField(max_length = 500)
   photo = models.ImageField(upload_to ='uploads/')
   user_post = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
   mecanic_post = models.ForeignKey(MechanicProfile, on_delete=models.CASCADE, null = True,  default = None)
   status = models.IntegerField(choices= status_choices, default = 0)
   date = models.DateTimeField(db_default=datetime.now())
   post_latitud = models.FloatField(default = 0)
   post_longitud = models.FloatField(default = 0)

class Message(models.Model):
   message_sent = models.TextField()
   user_sent_message = models.ForeignKey(User, on_delete=models.CASCADE)
   date = models.DateTimeField(db_default=datetime.now())

class Chat(models.Model):
   messages = models.ManyToManyField(Message)
   chat_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
   chat_mec = models.ForeignKey(MechanicProfile, on_delete=models.CASCADE)
