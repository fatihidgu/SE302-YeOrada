from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import RegisteredUser, Comment, CommentAnswer


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
        fields = ('email', 'username', 'name', 'surname', 'isCustomer', 'isClient', 'isAdmin',)
        widgets = {
            'password': forms.PasswordInput(),
        }


class CommentForm(forms.Form):

    class Meta:
        model = Comment
        fields = ('text', 'rate',)


class CommentAnswerForm(forms.Form):

    class Meta:
        model = CommentAnswer
        fields = ('answer',)


class ImageUploadForm(forms.Form):

    class Meta:
        model = Comment
        fields = ('image','image2','image3',)