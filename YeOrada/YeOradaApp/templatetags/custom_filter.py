from django import template

from YeOradaApp.models import Comment, Client

register = template.Library()


@register.filter
def filterCuisines(clientcuisines, clientEmail):
    clientObject = Client.objects.filter(userEmail=clientEmail).first()
    cuisineList = clientcuisines.filter(customerEmail=clientObject)
    return cuisineList


@register.filter
def filterComments(customerLikes, commentId):
    commentObject = (Comment.objects.filter(id=commentId)).first()

    currentCustomerLikes = customerLikes.filter(commentId=commentObject)

    if currentCustomerLikes.count() == 1:
        return currentCustomerLikes
    else:
        return None


@register.filter
def filterAnswers(answersList, commentId):
    commentObject = (Comment.objects.filter(id=commentId)).first()

    customerAnswers = answersList.filter(commentId=commentObject)

    return customerAnswers