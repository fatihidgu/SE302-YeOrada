from django import template

from YeOradaApp.models import Comment, Client

register = template.Library()


@register.filter
def filterCuisines(clientcuisines, clientEmail):
    clientObject = Client.objects.filter(userEmail=clientEmail).first()
    cuisineList = list()
    for x in clientcuisines:
        if x.customerEmail == clientObject:
            cuisineList.append(x)
    return cuisineList


@register.filter
def filterComments(customerLikes, commentId):
    commentObject = (Comment.objects.filter(id=commentId)).first()
    customerLikesList = list()
    for i in customerLikes:
        customerLikesList.append(i)
    print(customerLikesList)
    for j in customerLikesList:
        if j.commentId == commentObject:
            print(j)
            listt = list()
            listt.append(j)
            return listt
    return None