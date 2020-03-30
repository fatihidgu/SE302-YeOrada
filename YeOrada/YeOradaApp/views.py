from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


# Create your views here.
from YeOradaApp.forms import RegisteredUserCreationForm


def index(request):
    return render(request, 'yeoradamain/index.html', {})


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            error_message = "* Wrong Password or Username."
    else:
        error_message = ""
        form = AuthenticationForm()
    return render(request, 'yeoradamain/signin.html', {'form': form, 'error_message': error_message, })


def signup(request):
    error_message1 = ""
    error_message2 = ""
    if request.method == "POST":
        form = RegisteredUserCreationForm(request.POST)
        if form.is_valid():
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')

            if pass1 == pass2:
                cb = request.POST.get('cb')
                if not cb:
                    error_message1 = "* You must accept the Terms of Service and the Content Policy."
                else:
                    form.save()
                    return redirect('home')
            else:
                error_message2 = "* Passwords doesn't match."
    else:
        form = RegisteredUserCreationForm()
    return render(request, 'yeoradamain/signup.html', {'form': form, 'error_message1': error_message1, 'error_message2': error_message2, })


def clientprofile(request):

    return render(request, 'yeoradamain/restaurant_detail.html', {})


def settings(request):
    return render(request, 'yeoradamain/setting.html', {})



