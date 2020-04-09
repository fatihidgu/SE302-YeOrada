from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

# Create your models here.


class RegisteredUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(_('email address'), unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    isCustomer = models.BooleanField(default=False)
    isClient = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Customer(models.Model):
    userEmail = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, primary_key=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, blank=True)


class Client(models.Model):
    RESTAURANT = 'Restaurant'
    CAFE = 'Cafe'
    BAR = 'Bar'
    CATEGORIES = [
        (RESTAURANT, 'Restaurant'),
        (CAFE, 'Cafe'),
        (BAR, 'Bar'),
    ]
    name = models.CharField(max_length=250, null=True, blank=True)
    userEmail = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address1 = models.CharField(max_length=300, null=True, blank=True)
    address2 = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=200)
    workingHours = models.CharField(max_length=200)
    workingDays = models.CharField(max_length=200)
    info = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=200, null=True, blank=True, choices=CATEGORIES)
    rate = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    rateCount = models.IntegerField(null=True, blank=True)


class Admin(models.Model):
    userEmail = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, primary_key=True)


class Comment(models.Model):
    customerEmail = models.ForeignKey(Customer, on_delete=models.CASCADE)
    clientEmail = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    rate = models.IntegerField()


class CommentAnswer(models.Model):
    customerEmail = models.ForeignKey(Customer, on_delete=models.CASCADE)
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
    answer = models.TextField()


class CommentLike(models.Model):
    customerEmail = models.ForeignKey(Customer, on_delete=models.CASCADE)
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE)


class ClientCuisine(models.Model):
    KEBAP = 'Kebap'
    GRILL = 'Grill'
    TURKISH = 'Turkish'
    PIDE = 'Pide'
    DONER = 'Döner'
    FASTFOOD = 'Fast Food'
    HOMEMADE = 'Homemade'
    SEAFOOD = 'Seafood'
    CAFEANDRESTAURANT = 'Cafe & Restaurant'
    CUISINES = [
        (KEBAP, 'Kebap'),
        (GRILL, 'Grill'),
        (TURKISH, 'Turkish'),
        (PIDE, 'Pide'),
        (DONER, 'Döner'),
        (FASTFOOD, 'Fast Food'),
        (HOMEMADE, 'Homemade'),
        (SEAFOOD, 'Seafood'),
        (CAFEANDRESTAURANT, 'Cafe & Restaurant'),
    ]
    customerEmail = models.ForeignKey(Client, on_delete=models.CASCADE)
    cuisine = models.CharField(max_length=200, choices=CUISINES)
