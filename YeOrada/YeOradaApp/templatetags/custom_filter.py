from django import template

register = template.Library()


@register.filter
def filterCuisines(clientcuisines, clientEmail):
    clientcuisines.filter(customerEmail=clientEmail)
    return clientcuisines
