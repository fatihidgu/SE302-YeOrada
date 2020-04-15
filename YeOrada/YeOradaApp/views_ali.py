from django.http import JsonResponse
from django.shortcuts import redirect, render

from YeOradaApp.forms import CommentForm, CommentAnswerForm
from YeOradaApp.models import Comment, Customer, Client, CommentAnswer, CommentLike, RegisteredUser


def clientprofile(request, username):
    if 'publishReview' in request.POST:
        if request.user.is_authenticated:
            if request.user.isCustomer:
                commentForm = CommentForm(request.POST)
                if commentForm.is_valid():
                    text = request.POST.get('text')
                    customerObject = Customer.objects.filter(userEmail=request.user.email).first()
                    clientObject= Client.objects.filter(userEmail__username=username).first()
                    rate = request.POST.get('rate')
                    comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text=text, rate=rate)
                    # uploaded_image = request.POST.get('commentPhoto')
                    comment.save()
                    return redirect('clientprofile', username)
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
                    return redirect('clientprofile', username)
        else:
            return redirect('signin')

    commentForm = CommentForm()
    commentAnswerForm = CommentAnswerForm()
    clientObject = Client.objects.filter(userEmail__username=username).first()
    commentList = Comment.objects.filter(clientEmail=clientObject.userEmail.email)
    answersList = dict()
    numberOfComment = list()
    for comments in commentList:
        commentAnswers = CommentAnswer.objects.filter(commentId=comments.id)
        numberOfComment.append(commentAnswers.count())
        answersList.update({comments.id: commentAnswers})

    customerr = Customer.objects.filter(userEmail=request.user).first()
    customerLikes = CommentLike.objects.filter(customerEmail=customerr)

    registeredUser =  RegisteredUser.objects.filter(username=username).first()
    return render(request, 'yeoradamain/restaurant_detail.html',
                  {'commentForm': commentForm, 'commentList': commentList,
                   'commentAnswerForm': commentAnswerForm, 'answersList': answersList,
                   'numberOfComment': numberOfComment, 'customerLikes': customerLikes,'registeredUser':registeredUser,'clientObject':clientObject, })


def likeComment(request):
    if request.user.is_authenticated:
        if request.user.isCustomer:
            commentId = request.GET.get('commentId', None)
            #print("comment id is ",commentId)
            commentId2 = Comment.objects.filter(id=commentId).first()
            customerEmail = Customer.objects.filter(userEmail=request.user).first()
            commentLike = CommentLike.objects.filter(customerEmail=customerEmail, commentId=commentId2)
            if commentLike.count() == 0:
                createCommentLike = CommentLike(customerEmail=customerEmail, commentId=commentId2, isLiked=True)
                createCommentLike.save()
            else:
                if commentLike.first().isLiked:
                    commentLike.update(isLiked=False)
                else:
                    commentLike.update(isLiked=True)

    return JsonResponse({}, status = 400)
