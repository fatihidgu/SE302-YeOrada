from django.http import JsonResponse
from django.shortcuts import redirect, render

from YeOradaApp.forms import CommentForm, CommentAnswerForm, ImageUploadForm
from YeOradaApp.models import Comment, Customer, Client, CommentAnswer, CommentLike, RegisteredUser, ClientCuisine


def clientprofile(request, username):
    if 'publishReview' in request.POST:
        if request.user.is_authenticated:
            if request.user.isCustomer:
                commentForm = CommentForm(request.POST)
                if commentForm.is_valid():
                    text = request.POST.get('text')
                    imgOne = None
                    imgTwo = None
                    imgThr = None

                    customerObject = Customer.objects.filter(userEmail=request.user.email).first()
                    clientObject = Client.objects.filter(userEmail__username=username).first()
                    rate = request.POST.get('rate')

                    newRate = (((clientObject.rate * clientObject.rateCount) + int(rate)) / (
                            clientObject.rateCount + 1))
                    clientObject.rate = newRate
                    clientObject.rateCount = clientObject.rateCount + 1;
                    clientObject.save()

                    print(request.POST.get('fileOneChecking'), ", ", request.POST.get('fileTwoChecking'), " ve ",
                          request.POST.get('fileThrChecking'))
                    if request.POST.get('fileOneChecking') == '1' and request.POST.get(
                            'fileTwoChecking') == '1' and request.POST.get('fileThrChecking') == '1':
                        imgOne = request.FILES['commentPhotoOne']
                        imgTwo = request.FILES['commentPhotoTwo']
                        imgThr = request.FILES['commentPhotoThr']
                        comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text=text, rate=rate,
                                          image=imgOne, image2=imgTwo, image3=imgThr)
                    elif request.POST.get('fileOneChecking') == '1' and request.POST.get(
                            'fileTwoChecking') == '1' and request.POST.get('fileThrChecking') == '0':
                        imgOne = request.FILES['commentPhotoOne']
                        imgTwo = request.FILES['commentPhotoTwo']
                        comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text=text, rate=rate,
                                          image=imgOne, image2=imgTwo)
                    elif request.POST.get('fileOneChecking') == '1' and request.POST.get(
                            'fileTwoChecking') == '0' and request.POST.get('fileThrChecking') == '1':
                        imgOne = request.FILES['commentPhotoOne']
                        imgThr = request.FILES['commentPhotoThr']
                        comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text=text, rate=rate,
                                          image=imgOne, image3=imgThr)
                    elif request.POST.get('fileOneChecking') == '1' and request.POST.get(
                            'fileTwoChecking') == '0' and request.POST.get('fileThrChecking') == '0':
                        imgOne = request.FILES['commentPhotoOne']
                        comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text=text, rate=rate,
                                          image=imgOne)
                    elif request.POST.get('fileOneChecking') == '0' and request.POST.get(
                            'fileTwoChecking') == '1' and request.POST.get('fileThrChecking') == '1':
                        imgTwo = request.FILES['commentPhotoTwo']
                        imgThr = request.FILES['commentPhotoThr']
                        comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text=text, rate=rate,
                                          image2=imgTwo, image3=imgThr)
                    elif request.POST.get('fileOneChecking') == '0' and request.POST.get(
                            'fileTwoChecking') == '1' and request.POST.get('fileThrChecking') == '0':
                        imgTwo = request.FILES['commentPhotoTwo']
                        comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text=text, rate=rate,
                                          image2=imgTwo)
                    elif request.POST.get('fileOneChecking') == '0' and request.POST.get(
                            'fileTwoChecking') == '0' and request.POST.get('fileThrChecking') == '1':
                        imgOne = request.FILES['commentPhotoOne']

                        comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text=text, rate=rate,
                                          image=imgOne)
                    else:
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
                    commentObject.commentNumber += 1
                    commentObject.save()
                    commentAnswer = CommentAnswer(customerEmail=customerObject, commentId=commentObject, answer=answer)
                    commentAnswer.save()
                    return redirect('clientprofile', username)
        else:
            return redirect('signin')

    elif 'Save' in request.POST:
        if request.user.is_authenticated:
            if request.user.isClient:
                clientObject = Client.objects.filter(userEmail__username=username).first()

                if request.POST.get('fileOneChecking') == 'exist':
                    clientObject.image1 = request.FILES['clientPhotoOne']
                elif request.POST.get('fileOneChecking') == 'notExist':
                    clientObject.image1 = 'defaultClient.jpg'

                if request.POST.get('fileTwoChecking') == 'exist':
                    clientObject.image2 = request.FILES['clientPhotoTwo']
                elif request.POST.get('fileTwoChecking') == 'notExist':
                    clientObject.image2 = 'defaultClient.jpg'

                if request.POST.get('fileThrChecking') == 'exist':
                    clientObject.image3 = request.FILES['clientPhotoThr']
                elif request.POST.get('fileThrChecking') == 'notExist':
                    clientObject.image3 = 'defaultClient.jpg'

                if request.POST.get('fileFourChecking') == 'exist':
                    clientObject.image4 = request.FILES['clientPhotoFour']
                elif request.POST.get('fileFourChecking') == 'notExist':
                    clientObject.image4 = 'defaultClient.jpg'

                if request.POST.get('fileFiveChecking') == 'exist':
                    clientObject.image5 = request.FILES['clientPhotoFive']
                elif request.POST.get('fileFiveChecking') == 'notExist':
                    clientObject.image5 = 'defaultClient.jpg'

                if request.POST.get('fileSixChecking') == 'exist':
                    clientObject.image6 = request.FILES['clientPhotoSix']
                elif request.POST.get('fileSixChecking') == 'notExist':
                    clientObject.image6 = 'defaultClient.jpg'

                if request.POST.get('fileSevenChecking') == 'exist':
                    clientObject.image7 = request.FILES['clientPhotoSeven']
                elif request.POST.get('fileSevenChecking') == 'notExist':
                    clientObject.image7 = 'defaultClient.jpg'

                if request.POST.get('fileEightChecking') == 'exist':
                    clientObject.image8 = request.FILES['clientPhotoEight']
                elif request.POST.get('fileEightChecking') == 'notExist':
                    clientObject.image8 = 'defaultClient.jpg'

                if request.POST.get('fileNineChecking') == 'exist':
                    clientObject.image9 = request.FILES['clientPhotoNine']
                elif request.POST.get('fileNineChecking') == 'notExist':
                    clientObject.image9 = 'defaultClient.jpg'

                clientObject.save()

                return redirect('clientprofile', username)

    elif 'SaveMenu' in request.POST:
        if request.user.is_authenticated:
            if request.user.isClient:
                clientObject = Client.objects.filter(userEmail__username=username).first()

                if request.POST.get('fileMenuOneChecking') == 'exist':

                    clientObject.menu1 = request.FILES['clientMenuPhotoOne']
                elif request.POST.get('fileMenuOneChecking') == 'notExist':
                    clientObject.menu1 = 'defaultMenu.jpg'

                if request.POST.get('fileMenuTwoChecking') == 'exist':
                    clientObject.menu2 = request.FILES['clientMenuPhotoTwo']
                elif request.POST.get('fileMenuTwoChecking') == 'notExist':
                    clientObject.menu2 = 'defaultMenu.jpg'

                if request.POST.get('fileMenuThrChecking') == 'exist':
                    clientObject.menu3 = request.FILES['clientMenuPhotoThr']
                elif request.POST.get('fileMenuThrChecking') == 'notExist':
                    clientObject.menu3 = 'defaultMenu.jpg'

                if request.POST.get('fileMenuFourChecking') == 'exist':
                    clientObject.menu4 = request.FILES['clientMenuPhotoFour']
                elif request.POST.get('fileMenuFourChecking') == 'notExist':
                    clientObject.menu4 = 'defaultMenu.jpg'

                if request.POST.get('fileMenuFiveChecking') == 'exist':
                    clientObject.menu5 = request.FILES['clientMenuPhotoFive']
                elif request.POST.get('fileMenuFiveChecking') == 'notExist':
                    clientObject.menu5 = 'defaultMenu.jpg'

                clientObject.save()

                return redirect('clientprofile', username)

    commentForm = CommentForm()
    commentAnswerForm = CommentAnswerForm()
    clientObject = Client.objects.filter(userEmail__username=username).first()
    commentList = Comment.objects.filter(clientEmail=clientObject.userEmail.email).order_by('-date')
    answersList = CommentAnswer.objects.all()

    customerr = Customer.objects.filter(userEmail=request.user).first()
    customerLikes = CommentLike.objects.filter(customerEmail=customerr)

    registeredUser = RegisteredUser.objects.filter(username=username).first()
    clientcuisines = ClientCuisine.objects.all()

    CountOfPhoto = 0
    CountofComment = Comment.objects.filter(clientEmail=clientObject.userEmail.email)
    for com in CountofComment:
        if com.image != "defaultComment.jpg" and com.image2 == "defaultComment.jpg" and com.image3 == "defaultComment.jpg":
            CountOfPhoto += 1
        elif com.image != "defaultComment.jpg" and com.image2 != "defaultComment.jpg" and com.image3 == "defaultComment.jpg":
            CountOfPhoto += 2
        elif com.image != "defaultComment.jpg" and com.image2 != "defaultComment.jpg" and com.image3 != "defaultComment.jpg":
            CountOfPhoto += 3
    print(CountOfPhoto)

    clienty = Client.objects.filter(userEmail__is_active=True).order_by('-rateCount')[:10]

    client_menu_count = 0;

    if clientObject.menu1.url != "/media/defaultMenu.jpg":
        client_menu_count = client_menu_count + 1
    if clientObject.menu2.url != "/media/defaultMenu.jpg":
        client_menu_count = client_menu_count + 1
    if clientObject.menu3.url != "/media/defaultMenu.jpg":
        client_menu_count = client_menu_count + 1
    if clientObject.menu4.url != "/media/defaultMenu.jpg":
        client_menu_count = client_menu_count + 1
    if clientObject.menu5.url != "/media/defaultMenu.jpg":
        client_menu_count = client_menu_count + 1

    return render(request, 'yeoradamain/restaurant_detail.html',
                  {'commentForm': commentForm, 'commentList': commentList,
                   'commentAnswerForm': commentAnswerForm, 'answersList': answersList,
                   'customerLikes': customerLikes, 'registeredUser': registeredUser, 'clientObject': clientObject,
                   'clientcuisines': clientcuisines, 'customerr': customerr, 'clienty': clienty,
                   'CountOfPhoto': CountOfPhoto, 'client_menu_count': client_menu_count, })


def likeComment(request):
    if request.user.is_authenticated:
        if request.user.isCustomer:
            commentId = request.GET.get('commentId', None)
            # print("comment id is ",commentId)
            commentId2 = Comment.objects.filter(id=commentId).first()
            customerEmail = Customer.objects.filter(userEmail=request.user).first()
            commentLike = CommentLike.objects.filter(customerEmail=customerEmail, commentId=commentId2)
            if commentLike.count() == 0:
                createCommentLike = CommentLike(customerEmail=customerEmail, commentId=commentId2, isLiked=True)
                commentId2.likeNumber += 1
                createCommentLike.save()
                commentId2.save()
            else:
                if commentLike.first().isLiked:
                    commentLike.update(isLiked=False)
                    if (commentId2.likeNumber > 0):
                        commentId2.likeNumber -= 1
                    commentId2.save()
                else:
                    commentLike.update(isLiked=True)
                    commentId2.likeNumber += 1
                    commentId2.save()

    return JsonResponse({}, status=400)
