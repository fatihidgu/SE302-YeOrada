from urllib.parse import urlencode

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse

from YeOradaApp.forms import RegisteredUserCreationForm, CommentForm
from YeOradaApp.models import Comment, Customer, Client

from .views_ahmet import *
from .views_ali import *
from .views_fatih import *
from .views_yaren import *


def index(request):
    control = request.GET.get('control')
    customer = None
    if control is None:
        control = False

    if request.user.is_authenticated:
        customer = Customer.objects.filter(userEmail=request.user).first()
        if request.user.isCustomer and customer.city is not None:
            clients = Client.objects.filter(userEmail__is_active=True, city=customer.city).order_by('-rateCount')[:12]
        else:
            clients = Client.objects.filter(userEmail__is_active=True, city="İstanbul").order_by('-rateCount')[:12]

    else:
        clients = Client.objects.filter(userEmail__is_active=True, city="İstanbul").order_by('-rateCount')[:12]

    return render(request, 'yeoradamain/index.html', {'clients':clients, 'customer': customer, 'control': control, })


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            registeredUser = RegisteredUser.objects.filter(email=form.data['username']).first()

            if registeredUser is not None and not registeredUser.is_active:
                registeredUser.is_active = True
                registeredUser.save()
                if authenticate(request, email=form.data['username'], password=form.data['password']):
                    print("valid")
                    login(request, registeredUser, backend='django.contrib.auth.backends.ModelBackend')
                    base_url = reverse('home')
                    query_string = urlencode({'control': 'True'})
                    url = '{}?{}'.format(base_url, query_string)
                    return redirect(url)
                else:
                    error_message = "* Wrong Email or Password."
                    registeredUser.is_active = False
                    registeredUser.save()
            else:
                error_message = "* Wrong Email or Password."
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
                    user = RegisteredUser.objects.filter(email=form.cleaned_data['email']).first()
                    user.isCustomer = True
                    user.save()
                    customer = Customer(userEmail=user)
                    customer.save()
                    return redirect('signin')
            else:
                error_message2 = "* Passwords doesn't match."
    else:
        form = RegisteredUserCreationForm()
    return render(request, 'yeoradamain/signup.html', {'form': form, 'error_message1': error_message1, 'error_message2': error_message2, })