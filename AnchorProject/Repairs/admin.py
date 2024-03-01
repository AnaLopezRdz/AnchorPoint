from django.contrib import admin
from .models import *

# Register your models here.
models = (
    UserProfile, MechanicProfile, Post, Message, Chat
)
for model in models:
    admin.site.register(model)
