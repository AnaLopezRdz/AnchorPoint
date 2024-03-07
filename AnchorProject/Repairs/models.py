from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime



# Create your models here.

class UserProfile(models.Model):
    phone = PhoneNumberField(blank=True)
    user_django_profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):

      return f'{self.user_django_profile.first_name} {self.user_django_profile.last_name}\n{str(self.phone)}'

    # json models

    def to_json(self):
        return {
            'phone': str(self.phone),
            'user_django_profile': {
                'first_name': self.user_django_profile.first_name,
                'last_name': self.user_django_profile.last_name
            }
        }

class MechanicProfile(models.Model):
    phone = PhoneNumberField(blank=True)
    mec_django_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=500)
    longitud = models.FloatField(default = 0)
    latitud = models.FloatField(default = 0)

    def __str__(self):

      return f'{self.mec_django_profile.first_name} {self.mec_django_profile.last_name}\n, {self.skills},{str(self.phone)}, {self.latitud}, {self.longitud} '

    # jsonf models
    def to_json(self):
        return {
            'phone': str(self.phone),
            'mec_django_profile': {
                'first_name': self.mec_django_profile.first_name,
                'last_name': self.mec_django_profile.last_name
            },
            'skills': self.skills,
            'longitud': self.longitud,
            'latitud': self.latitud
        }

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

#    json models
    def to_json(self):
        if self.status == 0:
            color = "red"
        elif self.status == 1:
            color = "green"
        elif self.status == 2:
            color = "yellow"

        return {
            'comment': self.comment,
            'photo': self.photo.url,  # you're storing the URL of the uploaded photo
            'user_post': self.user_post.to_json(),
            # if mecanic_post is not None, convert it to JSON, otherwise return None
            'mecanic_post': self.mecanic_post.to_json() if self.mecanic_post else None,
            'status': self.get_status_display(),  # get human-readable status
            'date': self.date.strftime('%Y-%m-%dT%H:%M:%S'),  # format date as string
            'post_latitud': self.post_latitud,
            'post_longitud': self.post_longitud,
            "eventName": self.user_post.user_django_profile.first_name,
            "color": color,
            "calendar": "Boat Repairs",
        }



class Message(models.Model):
   message_sent = models.TextField()
   user_sent_message = models.ForeignKey(User, on_delete=models.CASCADE)
   date = models.DateTimeField(db_default=datetime.now())

class Chat(models.Model):
   messages = models.ManyToManyField(Message)
   chat_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
   chat_mec = models.ForeignKey(MechanicProfile, on_delete=models.CASCADE)
