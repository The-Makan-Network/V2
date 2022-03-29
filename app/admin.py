from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'phoneno', 'password1')
