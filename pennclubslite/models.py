from django.db import models
from django.contrib.auth.models import AbstractUser


class Club(models.Model):
    club_name = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.club_name

class Category(models.Model):
    clubs = models.ManyToManyField(Club)
    tag = models.CharField(max_length=100)
    def __str__(self):
        return self.tag

class CustomUser(AbstractUser):
    pass
    email = models.EmailField(blank=False, unique=True)
    favorites = models.ManyToManyField(Club)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['username', 'email', 'password']

    def __str__(self):
        return self.username