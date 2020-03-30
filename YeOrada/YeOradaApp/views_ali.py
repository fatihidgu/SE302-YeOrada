from django.shortcuts import redirect, render

from YeOradaApp.forms import CommentForm
from YeOradaApp.models import Comment, Customer, Client


def clientprofile(request):
    commentForm = CommentForm()
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

    return render(request, 'yeoradamain/restaurant_detail.html', {'commentForm': commentForm, 'commentList':commentList, })