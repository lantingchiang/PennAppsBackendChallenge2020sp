from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass
    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['username', 'email', 'password', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Club(models.Model):
    club_name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    likers = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.club_name


class Comment(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    posted_by = models.CharField(max_length=100, default='anonymous')
    comment = models.TextField()
    date = models.DateTimeField()


class Category(models.Model):
    clubs = models.ManyToManyField(Club)
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


