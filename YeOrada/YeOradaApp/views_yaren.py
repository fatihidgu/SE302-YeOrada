from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render

from YeOradaApp.forms import RegisteredUserChangeForm
from YeOradaApp.models import Customer, RegisteredUser


def settings(request):
    error_message1 = ""
    user = request.user
    passwordChangeForm = PasswordChangeForm(request.user)
    customer = Customer.objects.filter(userEmail=user.email).first()
    if 'saveChanges' in request.POST:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        city = request.POST.get('city')
        country = request.POST.get('country')
        username = request.POST.get('username')
        userObject = RegisteredUser.objects.filter(email=request.user.email)
        user = RegisteredUser(email=email, name=name, surname=surname, username=username)
        customer = Customer(city=city, country=country, userEmail=userObject.first())

        emailCheck = RegisteredUser.objects.filter(email=email)
        usernameCheck = RegisteredUser.objects.filter(username=username)
        if emailCheck.first() or usernameCheck.first():
            error_message1 = "* Email or username are already used"
            user = request.user
            customer = Customer.objects.filter(userEmail=user.email).first()
        else:
            user.save()
            customer.save()

    elif 'changePassword' in request.POST:
        passwordChangeForm = PasswordChangeForm(request.user, request.POST)
        if passwordChangeForm.is_valid():
            passwordChangeForm.save()

    else:
       user = request.user
       customer = Customer.objects.filter(userEmail=user.email).first()

    return render(request, 'yeoradamain/setting.html',
                  {'user': user, 'customer': customer, 'error_message1': error_message1, 'passwordChangeForm': passwordChangeForm, })
