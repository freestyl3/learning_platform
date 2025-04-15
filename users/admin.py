from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserCreationForm, MyUserChangeForm
from .models import MyUser

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ['first_name', 'last_name', 'username', 'password', 'is_teacher']

admin.site.register(MyUser, MyUserAdmin)