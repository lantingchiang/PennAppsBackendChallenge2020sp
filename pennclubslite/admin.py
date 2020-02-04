from django.contrib import admin
from .models import Club, Category, CustomUser, Comment

admin.site.register(Club)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Comment)
