from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from YeOradaApp.forms import RegisteredUserChangeForm
from YeOradaApp.models import Customer, RegisteredUser


def settings(request):
    error_message1 = ""
    if 'saveChanges' in request.POST:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        city = request.POST.get('city')
        country = request.POST.get('country')
        username = request.POST.get('username')
        userObject = RegisteredUser.objects.filter(email=request.user.email).first()
        customerObject = Customer.objects.filter(userEmail=request.user).first()

        #user = RegisteredUser(email=email, name=name, surname=surname, username=username)
        #customer = Customer(city=city, country=country, userEmail=userObject.first())

        emailCheck = RegisteredUser.objects.filter(email=email)
        usernameCheck = RegisteredUser.objects.filter(username=username)
        if (emailCheck.first() and email != request.user.email) or (usernameCheck.first() and username != request.user.username):
            error_message1 = "* Email or username are already used"
            user = request.user
            customer = Customer.objects.filter(userEmail=user.email).first()
        else:
            userObject.name = name;
            userObject.surname = surname;
            userObject.username = username;

            customerObject.city = city;
            customerObject.country = country;

            userObject.save()
            customerObject.save()
            return redirect('settings')

    elif 'changePassword' in request.POST:
        passwordChangeForm = PasswordChangeForm(request.user, request.POST)
        if passwordChangeForm.is_valid():
            passwordChangeForm.save()

    user = request.user
    passwordChangeForm = PasswordChangeForm(request.user)
    customer = Customer.objects.filter(userEmail=user.email).first()

    return render(request, 'yeoradamain/setting.html',
                  {'user': user, 'customer': customer, 'error_message1': error_message1, 'passwordChangeForm': passwordChangeForm, })
