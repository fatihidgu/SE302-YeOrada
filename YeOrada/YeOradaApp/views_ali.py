from django.shortcuts import redirect, render

from YeOradaApp.forms import CommentForm, CommentAnswerForm
from YeOradaApp.models import Comment, Customer, Client, CommentAnswer


def clientprofile(request):
    commentForm = CommentForm()
    commentAnswerForm = CommentAnswerForm()
    commentList = Comment.objects.filter(clientEmail="sivasetliekmek@gmail.com")
    answersList = dict()
    numberOfComment = list()
    for comments in commentList:
        commentAnswers = CommentAnswer.objects.filter(commentId=comments.id)
        numberOfComment.append(commentAnswers.count())
        answersList.update({comments.id:commentAnswers})

    if 'publishReview' in request.POST:
        if request.user.is_authenticated:
            if request.user.isCustomer:
                commentForm = CommentForm(request.POST)
                if commentForm.is_valid():
                    text = request.POST.get('text')
                    customerObject = Customer.objects.filter(userEmail=request.user.email).first()
                    clientObject = Client.objects.filter(userEmail="sivasetliekmek@gmail.com").first()
                    comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text=text, rate=1)
                    #uploaded_image = request.POST.get('commentPhoto')
                    comment.save()
        else:
            return redirect('signin')

    elif 'postComment' in request.POST:
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
        else:
            return redirect('signin')

    return render(request, 'yeoradamain/restaurant_detail.html', {'commentForm':commentForm, 'commentList':commentList,
                                                                  'commentAnswerForm':commentAnswerForm, 'answersList':answersList, 'numberOfComment':numberOfComment,})