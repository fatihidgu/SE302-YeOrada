from django.shortcuts import render

from YeOradaApp.models import Client


def clientsearch(request):
    clients = Client.objects.all()

    if 'searchRestaurant' in request.POST:
        name = request.POST.get('restaurant')
        clients = Client.objects.filter(name__icontains=name)

    return render(request, 'yeoradamain/partners.html', {'clients': clients, })


