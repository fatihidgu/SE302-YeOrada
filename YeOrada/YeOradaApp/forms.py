from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import RegisteredUser


class RegisteredUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = RegisteredUser
        fields = ('email', 'username', 'name', 'surname', 'isCustomer', 'isClient', 'isAdmin',)
        widgets = {
            'password': forms.PasswordInput(),
        }


class RegisteredUserChangeForm(UserChangeForm):

    class Meta:
        model = RegisteredUser
        fields = ('email', 'username', 'name', 'surname', 'password', 'isCustomer', 'isClient', 'isAdmin',)
        widgets = {
            'password': forms.PasswordInput(),
        }

