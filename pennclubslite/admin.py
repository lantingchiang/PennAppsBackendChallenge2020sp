from django.contrib import admin
from .models import Club, Category, CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

admin.site.register(Club)
admin.site.register(Category)
admin.site.register(CustomUser, UserAdmin)
