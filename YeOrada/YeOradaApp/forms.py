from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import RegisteredUser, Comment


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


class CommentForm(forms.Form):

    class Meta:
        model = Comment
        fields = ('text', 'rate',)