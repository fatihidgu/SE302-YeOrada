from datetime import timedelta

from django.shortcuts import render, redirect
from decimal import *

from YeOradaApp.models import Client, ClientCuisine, Customer
from django.db.models import Q
from django.utils import timezone


def clientsearch(request):
    filter_home = request.POST.get('filter_home')
    cuisine_name = request.POST.get('cuisine_name')

    if filter_home is not None:
        if filter_home == "Cafes & Restaurants":
            clients = Client.objects.filter(Q(category='Restaurant') | Q(category='Cafe'), userEmail__is_active=True)
        elif filter_home == "Bars & Pubs":
            clients = Client.objects.filter(userEmail__is_active=True, category='Bar')
        elif filter_home == "Desserts & Bakes":
            clients = Client.objects.filter(userEmail__is_active=True, category='Restaurant')
        elif filter_home == "Newly Opened":
            one_month_ago = timezone.now() - timedelta(days=30)
            clients = Client.objects.filter(userEmail__is_active=True, userEmail__date_joined__gte=one_month_ago)
        elif filter_home == "Near by":
            if request.user.is_authenticated:
                if request.user.isCustomer:
                    customerObject = Customer.objects.filter(userEmail=request.user).first()
                    if customerObject.city is not None:
                        clients = Client.objects.filter(userEmail__is_active=True, city=customerObject.city, state=customerObject.state)
                    else:
                        clients = Client.objects.filter(userEmail__is_active=True, city="İstanbul")
            else:
                clients = Client.objects.filter(userEmail__is_active=True, city="İstanbul")
        elif filter_home == "filter-cuisine" and cuisine_name is not None:
            cuisine_list = ClientCuisine.objects.filter(cuisine=cuisine_name)
            if cuisine_list.count() != 0:
                clients = list()
                for cuisine in cuisine_list:
                    clients.append(cuisine.customerEmail)
    else:
        clients = Client.objects.filter(userEmail__is_active=True)

    clientcuisines = ClientCuisine.objects.all()
    city = ""
    state = ""

    if 'searchRestaurant' in request.POST:
        name = request.POST.get('restaurant')
        city = request.POST.get('city_input')
        state = request.POST.get('state_input')
        print("State:", state)
        print("City:", city)

        if len(name.split()) == 0:

            if len(city.split()) == 0 and len(state.split()) == 0:
                clients = Client.objects.filter(userEmail__is_active=True)
            else:
                clients = Client.objects.filter(userEmail__is_active=True, city=city, state=state)
        else:

            if len(city.split()) == 0 and len(state.split()) == 0:
                clients = Client.objects.filter(name__icontains=name, userEmail__is_active=True)
            else:
                clients = Client.objects.filter(userEmail__is_active=True, name__icontains=name, city=city, state=state)

        clientcuisines = ClientCuisine.objects.all()

    elif 'search' in request.POST:
        city = request.POST.get('city_input')
        state = request.POST.get('state_input')

        if len(city.split()) == 0 and len(state.split()) == 0:
            clientQuerySet = Client.objects.filter(userEmail__is_active=True)
        else:
            clientQuerySet = Client.objects.filter(userEmail__is_active=True, city=city, state=state)

        clients = list()

        for client in clientQuerySet:
            clients.append(client)

        restaurant = request.POST.get('Restaurant')
        cafe = request.POST.get('Cafe')
        bar = request.POST.get('Bar')

        kebap = request.POST.get('Kebap')
        grill = request.POST.get('Grill')
        turkish = request.POST.get('Turkish')
        pide = request.POST.get('Pide')
        doner = request.POST.get('Döner')
        fastfood = request.POST.get('Fast Food')
        homemade = request.POST.get('Homemade')
        seafood = request.POST.get('Seafood')
        lunch = request.POST.get('Lunch')
        breakfast = request.POST.get('Breakfast')
        dinner = request.POST.get('Dinner')
        pizza = request.POST.get('Pizza')
        CafeRestaurant = request.POST.get('CafeRestaurant')
        chinese = request.POST.get('Chinese')
        korean = request.POST.get('Korean')

        onestar = request.POST.get('one_star')
        twostar = request.POST.get('two_star')
        threestar = request.POST.get('three_star')
        fourstar = request.POST.get('four_star')
        fivestar = request.POST.get('five_star')

        categoryList = list()

        if restaurant == 'on':
            # clientQuery = Client.objects.filter(category__exact='Restaurant')
            # for client in clientQuery:
            #    clients.append(client)
            categoryList.append('Restaurant')
        if cafe == 'on':
            # clientQuery = Client.objects.filter(category__exact='Cafe')
            # for client in clientQuery:
            #    clients.append(client)
            categoryList.append('Cafe')
        if bar == 'on':
            # clientQuery = Client.objects.filter(category__exact='Bar')
            # for client in clientQuery:
            #    clients.append(client)
            categoryList.append('Bar')

        categoryClientList = clients.copy()

        categoryFlag = False
        if categoryList.__len__() > 0:
            for client in categoryClientList:
                categoryFlag = False
                for category in categoryList:
                    if client.category == category:
                        categoryFlag = True
                        break
                if not categoryFlag:
                    clients.remove(client)

        cuisineList = list()

        if kebap == 'on':
            # clients = clients.filter(category__exact='Kebap')
            cuisineList.append('Kebap')
        if grill == 'on':
            # clients = clients.filter(category__exact='Grill')
            cuisineList.append('Grill')
        if turkish == 'on':
            # clients = clients.filter(category__exact='Turkish')
            cuisineList.append('Turkish')
        if pide == 'on':
            # clients = clients.filter(category__exact='Pide')
            cuisineList.append('Pide')
        if doner == 'on':
            # clients = clients.filter(category__exact='Döner')
            cuisineList.append('Döner')
        if fastfood == 'on':
            # clients = clients.filter(category__exact='Fast Food')
            cuisineList.append('Fast Food')
        if homemade == 'on':
            # clients = clients.filter(category__exact='Homemade')
            cuisineList.append('Homemade')
        if seafood == 'on':
            # clients = clients.filter(category__exact='Seafood')
            cuisineList.append('Seafood')
        if lunch == 'on':
            # clients = clients.filter(category__exact='Lunch')
            cuisineList.append('Lunch')
        if breakfast == 'on':
            # clients = clients.filter(category__exact='Breakfast')
            cuisineList.append('Breakfast')
        if dinner == 'on':
            # clients = clients.filter(category__exact='Dinner')
            cuisineList.append('Dinner')
        if pizza == 'on':
            # clients = clients.filter(category__exact='Pizza')
            cuisineList.append('Pizza')
        if CafeRestaurant == 'on':
            # clients = clients.filter(category__exact='Cafe & Restaurant')
            cuisineList.append('Cafe & Restaurant')
        if chinese == 'on':
            # clients = clients.filter(category__exact='Chinese')
            cuisineList.append('Chinese')
        if korean == 'on':
            # clients = clients.filter(category__exact='Korean')
            cuisineList.append('Korean')

        controlFlag = True
        cuisineClientList = clients.copy()
        if cuisineList.__len__() > 0:
            for client in cuisineClientList:
                controlFlag = True
                for cuisine in cuisineList:
                    cuisineCheck = ClientCuisine.objects.filter(customerEmail=client, cuisine__exact=cuisine)

                    if cuisineCheck.count() == 0:
                        controlFlag = False
                        break

                if not controlFlag:
                    clients.remove(client)

        starList = list()

        if onestar == 'on':
            # clientQuery = Client.objects.filter(rate__lt=2, rate__gt=1)
            value = Decimal(1)
            starList.append(value)
        if twostar == 'on':
            # clientQuery = Client.objects.filter(rate__lte=3, rate__gt=2)
            value = Decimal(2)
            starList.append(value)
        if threestar == 'on':
            # clientQuery = Client.objects.filter(rate__lte=4, rate__gt=3)
            value = Decimal(3)
            starList.append(value)
        if fourstar == 'on':
            # clientQuery = Client.objects.filter(rate__lte=5, rate__gt=4)
            value = Decimal(4)
            starList.append(value)
        if fivestar == 'on':
            # clientQuery = Client.objects.filter(rate__exact=5)
            value = Decimal(5)
            starList.append(value)

        starFlag = False;
        starClientList = clients.copy()
        if starList.__len__() > 0:
            for client in starClientList:
                starFlag = False;
                for star in starList:
                    if star.__le__(Decimal(5)) and client.rate.__eq__(Decimal(5)):
                        starFlag = True
                        break
                    elif client.rate.__gt__(star) and client.rate.__le__(star + 1):
                        starFlag = True
                        break

                if not starFlag:
                    clients.remove(client)
    clienty = Client.objects.filter(userEmail__is_active=True).order_by('-rateCount')[:7]

    return render(request, 'yeoradamain/partners.html', {'clients': clients, 'clientcuisines': clientcuisines,'clienty': clienty, 'city': city, 'state': state, })
