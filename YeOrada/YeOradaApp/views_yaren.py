from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from YeOradaApp.forms import RegisteredUserChangeForm, CommentAnswerForm, CommentForm
from YeOradaApp.models import Customer, RegisteredUser, Comment, CommentAnswer, CommentLike, Admin, ClientApplicationForm, Client

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def settings(request):
    error_message1 = ""
    error_message2 = ""
    passwordChangeForm = PasswordChangeForm(request.user)
    if 'saveChanges' in request.POST:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        city = request.POST.get('city')
        state = request.POST.get('state')
        username = request.POST.get('username')
        imageCheck = request.POST.get('customer_avatar_check')

        if len(imageCheck.split()) != 0:
            image = request.FILES['customer_avatar']

        userObject = RegisteredUser.objects.filter(email=request.user.email).first()
        customerObject = Customer.objects.filter(userEmail=request.user).first()

        # user = RegisteredUser(email=email, name=name, surname=surname, username=username)
        # customer = Customer(city=city, country=country, userEmail=userObject.first())

        usernameCheck = RegisteredUser.objects.filter(username=username)
        if usernameCheck.first() and username != request.user.username:
            error_message1 = "*Username is already used"
            user = request.user
            customer = Customer.objects.filter(userEmail=user.email).first()
        else:
            userObject.name = name;
            userObject.surname = surname;
            userObject.username = username;

            if city == "":
                customerObject.city = None
            else:
                customerObject.city = city;

            if state == "":
                customerObject.state = None
            else:
                customerObject.state = state;

            if len(imageCheck.split()) != 0:
                customerObject.image = image

            userObject.save()
            customerObject.save()
            return redirect('settings')

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
            error_message2 = "You entered a wrong email"

    user = request.user

    customer = Customer.objects.filter(userEmail=user.email).first()

    return render(request, 'yeoradamain/setting.html',
                  {'user': user, 'customer': customer, 'error_message1': error_message1,
                   'passwordChangeForm': passwordChangeForm, 'error_message2': error_message2})


def myprofile(request):
    user = request.user
    if 'postComment' in request.POST:
        if request.user.is_authenticated:
            if request.user.isCustomer:
                commentAnswerForm = CommentAnswerForm(request.POST)
                if commentAnswerForm.is_valid():
                    answer = request.POST.get('post')
                    commentId = request.POST.get('commentId')
                    commentObject = Comment.objects.filter(id=commentId).first()
                    customerObject = Customer.objects.filter(userEmail=request.user.email).first()
                    commentAnswer = CommentAnswer(customerEmail=customerObject, commentId=commentObject, answer=answer)
                    commentAnswer.save()
                    return redirect('myprofile')
        else:
            return redirect('signin')

    commentForm = CommentForm()
    commentAnswerForm = CommentAnswerForm()
    commentList = Comment.objects.filter(customerEmail=request.user.email, is_Approved=True).order_by('-date')
    answersList = CommentAnswer.objects.all()

    customer = Customer.objects.filter(userEmail=request.user).first()
    customerLikes = CommentLike.objects.filter(customerEmail=customer)

    return render(request, 'yeoradamain/user_profile_view.html',
                  {'user': user, 'customer': customer, 'commentForm': commentForm,
                   'commentList': commentList,
                   'commentAnswerForm': commentAnswerForm, 'answersList': answersList,
                   'customerLikes': customerLikes, })


def adminsettings(request):
    error_message1 = ""
    error_message2 = ""

    passwordChangeForm = PasswordChangeForm(request.user)
    if 'saveChanges2' in request.POST:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        userObject = RegisteredUser.objects.filter(email=request.user.email).first()
        emailCheck = RegisteredUser.objects.filter(email=email)
        usernameCheck = RegisteredUser.objects.filter(username=username)
        if (emailCheck.first() and email != request.user.email) or (
                usernameCheck.first() and username != request.user.username):
            error_message1 = "*Username is already used"

        else:
            userObject.name = name;
            userObject.surname = surname;
            userObject.username = username;

            userObject.save()

            return redirect('adminsettings')

    elif 'changePassword' in request.POST:
        passwordChangeForm = PasswordChangeForm(request.user, request.POST)
        if passwordChangeForm.is_valid():
            passwordChangeForm.save()
            return redirect('signin')

    user = request.user

    return render(request, 'yeoradamain/admin_settings.html',
                  {'user': user, 'error_message1': error_message1,
                   'passwordChangeForm': passwordChangeForm, 'error_message2': error_message2})


def adminprofile(request):
    user = request.user
    applicationformlist = ClientApplicationForm.objects.all().order_by('-date')
    if 'accept' in request.POST:
        if request.user.is_authenticated:
                 adminObject = Admin.objects.filter(userEmail=user).first()
                 commentId = request.POST.get('commentId')
                 commentSet = Comment.objects.filter(id=commentId)
                 commentObject = commentSet.first()

                 admin_name = adminObject.userEmail.name
                 admin_surname = adminObject.userEmail.surname
                 customer_name = commentObject.customerEmail.userEmail.name
                 customer_surname = commentObject.customerEmail.userEmail.surname
                 review = commentObject.text
                 date = commentObject.date
                 restaurant = commentObject.clientEmail.name
                 rate = commentObject.rate

                 clientObject = Client.objects.filter(userEmail__email=commentObject.clientEmail.userEmail.email).first()
                 newRate = (((clientObject.rate * clientObject.rateCount) + int(rate)) / (
                         clientObject.rateCount + 1))
                 clientObject.rate = newRate
                 clientObject.rateCount = clientObject.rateCount + 1;

                 subject = 'Yeorada | Your review has just accepted!'
                 html_message = render_to_string('yeoradamain/acceptReview.html',
                                                 {'customer_name': customer_name, 'customer_surname': customer_surname,
                                                  'review': review, 'restaurant': restaurant, 'date': date, 'admin_name': admin_name,
                                                  'admin_surname': admin_surname, })
                 plain_message = strip_tags(html_message)
                 from_email = 'YeOrada <noreply.yeorada@gmail.com>'
                 to = commentObject.customerEmail.userEmail.email

                 mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

                 commentSet.update(is_Approved=True, approved_by=adminObject)
                 clientObject.save()
                 return redirect('adminprofile')
    elif 'decline' in request.POST:
        if request.user.is_authenticated:
             adminObject = Admin.objects.filter(userEmail=user).first()
             admin_name = adminObject.userEmail.name
             admin_surname = adminObject.userEmail.surname

             reason = request.POST.get('reason')
             if len(reason.split()) == 0:
                 reason = "No reason is provided by the customer representative."
             commentId = request.POST.get('commentId')
             commentSet = Comment.objects.filter(id=commentId)

             commentObject = commentSet.first()
             customer_name = commentObject.customerEmail.userEmail.name
             customer_surname = commentObject.customerEmail.userEmail.surname
             review = commentObject.text
             date = commentObject.date
             restaurant = commentObject.clientEmail.name

             subject = 'Yeorada | Your review has just declined'
             html_message = render_to_string('yeoradamain/declineReview.html', {'customer_name': customer_name, 'customer_surname': customer_surname,
                                                                                'review': review, 'restaurant': restaurant, 'date': date,
                                                                                'reason': reason, 'admin_name': admin_name, 'admin_surname': admin_surname, })
             plain_message = strip_tags(html_message)
             from_email = 'YeOrada <noreply.yeorada@gmail.com>'
             to = commentObject.customerEmail.userEmail.email

             mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

             commentSet.delete()
             return redirect('adminprofile')
    elif 'acceptClient' in request.POST:
        User = get_user_model()
        formset=ClientApplicationForm.objects.filter(id=request.POST.get('client-form-id'))
        formobj=formset.first()
        pwd = User.objects.make_random_password(length=12, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        usrname=formobj.restaurant_name.lower().replace(" ", "")
        registered_user = User.objects.create_user(email=formobj.restaurant_email, password=pwd, username=usrname,
                                                   name=formobj.owner_name, surname=formobj.owner_surname,
                                                   isClient=True)
        registered_user.save()
        client_user = Client.objects.create(userEmail=registered_user, name=formobj.restaurant_name,
                                            phone=formobj.restaurant_phone,
                                            city=formobj.city, state=formobj.state, address1=formobj.restaurant_address,
                                            workingHours=formobj.workhour_from + '-' + formobj.workhour_to,
                                            workingDays=formobj.workday_from + '-' + formobj.workday_to,
                                            category=formobj.category, is_verified=formobj.will_be_verified, workingHoursFrom=formobj.workhour_from,
                                            workingHoursTo=formobj.workhour_to, workingDaysFrom=formobj.workday_from, workingDaysTo=formobj.workday_to, )
        client_user.save()

        subject = 'YeOrada | Your restaurant application is accepted!'
        html_message = render_to_string('yeoradamain/clientApplicationAccepted.html',
                                        {'email': formobj.restaurant_email, 'password': pwd,
                                         'owner_name': formobj.owner_name, 'admin_name': request.user.name, 'admin_surname': request.user.surname, })
        plain_message = strip_tags(html_message)
        from_email = 'YeOrada <noreply.yeorada@gmail.com>'
        to = formobj.owner_email

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        formset.delete()
        return redirect('adminprofile')
    elif 'declineClient' in request.POST:
        reason = request.POST.get('reasonClient')
        formset = ClientApplicationForm.objects.filter(id=request.POST.get('client-form-id'))
        formobj = formset.first()

        subject = 'YeOrada | Your restaurant application is declined'
        html_message = render_to_string('yeoradamain/clientApplicationDeclined.html',
                                        {'reason': reason, 'restaurant_name': formobj.restaurant_name, 'owner_surname': formobj.owner_surname,
                                         'owner_name': formobj.owner_name, 'admin_name': request.user.name,
                                         'admin_surname': request.user.surname, })
        plain_message = strip_tags(html_message)
        from_email = 'YeOrada <noreply.yeorada@gmail.com>'
        to = formobj.owner_email

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        formset.delete()
        return redirect('adminprofile')
    commentList = Comment.objects.filter(is_Approved=False).order_by('-date')
    customer = Customer.objects.filter(userEmail=request.user).first()

    return render(request, 'yeoradamain/admin_profile.html',
                  {'user': user, 'customer': customer,
                   'commentList': commentList,'applicationformlist':applicationformlist })


def faq(request):

    return render(request, 'yeoradamain/faq.html',)