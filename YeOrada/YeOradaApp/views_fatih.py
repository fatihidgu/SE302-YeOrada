from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from YeOradaApp.forms import RegisteredUserChangeForm, CommentAnswerForm, CommentForm
from YeOradaApp.models import Customer, RegisteredUser, Comment, CommentAnswer, CommentLike, Client, ClientCuisine, \
    ClientApplicationForm
from django.core.validators import validate_email


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
        wdaysfrom = request.POST.get('wdaysfrom')
        wdaysto = request.POST.get('wdaysto')
        whoursfrom = request.POST.get('whoursfrom')
        whoursto = request.POST.get('whoursto')

        if len(imageCheck.split()) != 0:
            image = request.FILES['client_avatar']

        userObject = RegisteredUser.objects.filter(email=request.user.email).first()
        emailCheck = RegisteredUser.objects.filter(email=email)
        usernameCheck = RegisteredUser.objects.filter(username=username)
        if usernameCheck.first() and username != request.user.username:
            error_message1 = "*Username is already used"
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
            clientObject.workingHours = whoursfrom + '-' + whoursto
            clientObject.workingDays = wdaysfrom + '-' + wdaysto
            clientObject.info = info

            clientObject.workingDaysFrom = wdaysfrom
            clientObject.workingDaysTo = wdaysto
            clientObject.workingHoursFrom = whoursfrom
            clientObject.workingHoursTo = whoursto

            for item in clientcuisines:
                cuisin = request.POST.get(item)
                if len(ClientCuisine.objects.filter(customerEmail=clientObject,
                                                    cuisine=cuisin)) == 0 and cuisin != None:
                    # ekle
                    clientcuisine = ClientCuisine(customerEmail=clientObject, cuisine=cuisin)
                    clientcuisine.save()
                elif len(
                        ClientCuisine.objects.filter(customerEmail=clientObject, cuisine=item)) != 0 and cuisin == None:
                    # delete
                    clientdelete = ClientCuisine.objects.filter(cuisine=item).delete()

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
            error_message2 = "*You entered a wrong email"

    user = request.user
    client = Client.objects.filter(userEmail=user.email).first()

    return render(request, 'yeoradamain/setting_client.html',
                  {'user': user, 'client': client, 'error_message1': error_message1,
                   'passwordChangeForm': passwordChangeForm, 'error_message2': error_message2,
                   'clientcuisines': clientcuisines, 'clientObject': clientObject})


def newclient(request):
    # restemail
    # restname
    client_error_messages = list()
    succesfull_message = ""
    # ClientApplicationForm
    # Client
    #
    if 'sendformname' in request.POST:
        rname = request.POST.get('rname')
        rcity = request.POST.get('rcity')
        rstate = request.POST.get('rstate')
        oname = request.POST.get('oname')
        osname = request.POST.get('osname')
        oemail = request.POST.get('oemail')
        ophone = request.POST.get('ophone')
        rphone = request.POST.get('rphone')
        remail = request.POST.get('remail')
        wdaysfrom = request.POST.get('wdaysfrom')
        wdaysto = request.POST.get('wdaysto')
        whoursfrom = request.POST.get('whoursfrom')
        whoursto = request.POST.get('whoursto')
        address = request.POST.get('address')
        verify = request.POST.get('verify')
        rcategory=request.POST.get('category')

        if RegisteredUser.objects.filter(email=remail).first() or ClientApplicationForm.objects.filter(
                restaurant_email=remail).first():
            # email hatası
            client_error_messages.append("This email has already taken before. Please use another one.")

        if Client.objects.filter(name=rname).first() or ClientApplicationForm.objects.filter(
                restaurant_name=rname).first():
            # restaurant name hatası
            client_error_messages.append("This restaurant name has already taken before. Please use another one.")

        if rname == "" or oname == "" or osname == "" or oemail == "" or ophone == "" or rphone == "" or remail == "" or address == "":
            client_error_messages.append("You must fill out all the fields in the form.")

        if address.__len__() > 85:
            client_error_messages.append("Entered restaurant address is too long.")

        if client_error_messages.__len__() == 0:
            # kayıt işlemi
            ClientApplicationForm.objects.create(restaurant_name=rname, city=rcity, state=rstate,
                                                 owner_name=oname, owner_surname=osname,
                                                 owner_email=oemail,
                                                 owner_phone=ophone, restaurant_phone=rphone,
                                                 restaurant_email=remail, workday_from=wdaysfrom,
                                                 workday_to=wdaysto, workhour_from=whoursfrom,
                                                 workhour_to=whoursto, restaurant_address=address,
                                                 will_be_verified=verify, category=rcategory).save()
            succesfull_message = "We sent your form successfully!"
    return render(request, 'yeoradamain/add_restaurant.html', {'client_error_messages': client_error_messages, 'succesfull_message': succesfull_message, })
