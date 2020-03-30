from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


# Create your views here.
from YeOradaApp.forms import RegisteredUserCreationForm, CommentForm
from YeOradaApp.models import Comment, Customer, Client


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
    commentList = Comment.objects.filter(clientEmail="sivasetliekmek@gmail.com")
    if 'publishReview' in request.POST:
        if request.user.is_authenticated:
            if request.user.isCustomer:
                commentForm = CommentForm(request.POST)
                if commentForm.is_valid():
                    text = request.POST.get('text')
                    customerObject = Customer.objects.filter(userEmail=request.user.email).first()
                    clientObject = Client.objects.filter(userEmail="sivasetliekmek@gmail.com").first()
                    comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text=text, rate=1)
                    uploaded_image = request.POST.get('commentPhoto')
                    comment.save()
        else:
            return redirect('signin')
    else:
        commentForm = CommentForm()

    return render(request, 'yeoradamain/restaurant_detail.html', {'commentForm': commentForm, 'commentList':commentList})