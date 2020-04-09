from django.shortcuts import render

from YeOradaApp.models import Client, ClientCuisine


def clientsearch(request):
    clients = Client.objects.all()
    clientcuisines = ClientCuisine.objects.all()

    if 'searchRestaurant' in request.POST:
        name = request.POST.get('restaurant')
        clients = Client.objects.filter(name__icontains=name)
        clientcuisines = ClientCuisine.objects.all()

    return render(request, 'yeoradamain/partners.html', {'clients': clients, 'clientcuisines': clientcuisines, })


