from django.db import models
from django.contrib.auth.models import User

class Person(User):
    alice_user_id = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    direction = models.CharField(max_length=255)
    stop = models.CharField(max_length=255)

