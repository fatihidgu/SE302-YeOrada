from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from YeOradaApp.forms import RegisteredUserChangeForm, CommentAnswerForm, CommentForm
from YeOradaApp.models import Customer, RegisteredUser, Comment, CommentAnswer, CommentLike


def settings(request):
    error_message1 = ""
    error_message2 = ""
    passwordChangeForm = PasswordChangeForm(request.user)
    if 'saveChanges' in request.POST:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        city = request.POST.get('city')
        country = request.POST.get('country')
        username = request.POST.get('username')
        imageCheck = request.POST.get('customer_avatar_check')

        if len(imageCheck.split()) != 0:
            image = request.FILES['customer_avatar']

        userObject = RegisteredUser.objects.filter(email=request.user.email).first()
        customerObject = Customer.objects.filter(userEmail=request.user).first()

        # user = RegisteredUser(email=email, name=name, surname=surname, username=username)
        # customer = Customer(city=city, country=country, userEmail=userObject.first())

        emailCheck = RegisteredUser.objects.filter(email=email)
        usernameCheck = RegisteredUser.objects.filter(username=username)
        if (emailCheck.first() and email != request.user.email) or (
                usernameCheck.first() and username != request.user.username):
            error_message1 = "* Email or username are already used"
            user = request.user
            customer = Customer.objects.filter(userEmail=user.email).first()
        else:
            userObject.name = name;
            userObject.surname = surname;
            userObject.username = username;

            customerObject.city = city;
            customerObject.country = country;

            if len(imageCheck.split()) != 0:
                customerObject.image = image

            userObject.save()
            customerObject.save()
            return redirect('settings')

    elif 'changePassword' in request.POST:
        passwordChangeForm = PasswordChangeForm(request.user, request.POST)
        if passwordChangeForm.is_valid():
            passwordChangeForm.save()
            return redirect('home')

    elif 'yourEmail' in request.POST:
        if request.POST.get('Email') == request.user.email:
            ruser = RegisteredUser.objects.filter(email=request.user.email)
            ruser.update(is_active=False)
            return redirect('home')
        else:
            error_message2 = "You entered wrong mail"

    user = request.user

    customer = Customer.objects.filter(userEmail=user.email).first()

    return render(request, 'yeoradamain/setting.html',
                  {'user': user, 'customer': customer, 'error_message1': error_message1,
                   'passwordChangeForm': passwordChangeForm, 'error_message2': error_message2})


def myprofile(request):
    comments = Comment.objects.filter(customerEmail=request.user.email)
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
    commentList = Comment.objects.filter(customerEmail=request.user.email).order_by('-date')
    answersList = CommentAnswer.objects.all()

    customer = Customer.objects.filter(userEmail=request.user).first()
    customerLikes = CommentLike.objects.filter(customerEmail=customer)

    return render(request, 'yeoradamain/user_profile_view.html',
                  {'user': user, 'customer': customer, 'comments': comments, 'commentForm': commentForm,
                   'commentList': commentList,
                   'commentAnswerForm': commentAnswerForm, 'answersList': answersList,
                   'customerLikes': customerLikes, })
