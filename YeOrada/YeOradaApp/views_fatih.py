from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from YeOradaApp.forms import RegisteredUserChangeForm, CommentAnswerForm, CommentForm
from YeOradaApp.models import Customer, RegisteredUser, Comment, CommentAnswer, CommentLike, Client, ClientCuisine


def clientsettings(request):
    error_message1 = ""
    error_message2 = ""
    clientcuisines = [
       'Kebap',
       'Grill',
       'Turkish',
       'Pide',
       'Döner',
       'Fast Food',
        'Homemade',
        'Seafood',
       'Cafe & Restaurant',
        'Lunch',
        'Breakfast',
       'Dinner',
        'Pizza',
        'Chinese',
        'Korean', ]


    clientObject = Client.objects.filter(userEmail__username=request.user.username).first()
    passwordChangeForm = PasswordChangeForm(request.user)
    if 'saveChanges' in request.POST:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        state = request.POST.get('state')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        workinghours = request.POST.get('workinghours')
        workingdays = request.POST.get('workingdays')
        info = request.POST.get('info')
        imageCheck = request.POST.get('client_avatar_check')


        if len(imageCheck.split()) != 0:
            image = request.FILES['client_avatar']

        userObject = RegisteredUser.objects.filter(email=request.user.email).first()
        emailCheck = RegisteredUser.objects.filter(email=email)
        usernameCheck = RegisteredUser.objects.filter(username=username)
        if usernameCheck.first() and username != request.user.username:
            error_message1 = "*Username are already used"
            user = request.user
            client = Customer.objects.filter(userEmail=user.email).first()
        else:


            userObject.name = name;
            userObject.surname = surname;
            userObject.username = username;

            clientObject.phone = phone
            clientObject.city = city
            clientObject.address1 = address1
            clientObject.address2 = address2
            clientObject.state = state
            clientObject.workingHours = workinghours
            clientObject.workingDays = workingdays
            clientObject.info = info

            cuisineList = ClientCuisine.objects.filter(customerEmail=clientObject).get("cuisine")
            print("my first ",cuisineList)
            for item in clientcuisines:
                cuisin = request.POST.get(item)
                if cuisin == cuisineList:
                    print("Burada", cuisin)
            #clientcuisine=ClientCuisine(customerEmail=clientObject,cuisine='Seafood')
            #clientcuisine.save()


            if len(imageCheck.split()) != 0:
                clientObject.logo = image

            userObject.save()
            clientObject.save()
            return redirect('clientsettings')

    elif 'changePassword' in request.POST:
        passwordChangeForm = PasswordChangeForm(request.user, request.POST)
        if passwordChangeForm.is_valid():
            passwordChangeForm.save()
            return redirect('signin')

    elif 'yourEmail' in request.POST:
        if request.POST.get('Email') == request.user.email:
            ruser = RegisteredUser.objects.filter(email=request.user.email)
            ruser.update(is_active=False)
            return redirect('home')
        else:
            error_message2 = "You entered wrong mail"

    user = request.user
    client = Client.objects.filter(userEmail=user.email).first()

    return render(request, 'yeoradamain/setting_client.html',
                  {'user': user, 'client': client, 'error_message1': error_message1,
                   'passwordChangeForm': passwordChangeForm, 'error_message2': error_message2, 'clientcuisines': clientcuisines, 'clientObject': clientObject })
