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
    state = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='customer_pics')


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
    image1 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image2 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image3 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image4 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image5 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image6 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image7 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image8 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image9 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    logo = models.ImageField(default='defaultLogo.jpg', upload_to='client_logo_pics')
    menu1 = models.ImageField(default='defaultMenu.jpg', upload_to='client_menu_pics')
    menu2 = models.ImageField(default='defaultMenu.jpg', upload_to='client_menu_pics')
    menu3 = models.ImageField(default='defaultMenu.jpg', upload_to='client_menu_pics')
    menu4 = models.ImageField(default='defaultMenu.jpg', upload_to='client_menu_pics')
    menu5 = models.ImageField(default='defaultMenu.jpg', upload_to='client_menu_pics')


class Admin(models.Model):
    userEmail = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, primary_key=True)


class Comment(models.Model):
    customerEmail = models.ForeignKey(Customer, on_delete=models.CASCADE)
    clientEmail = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    rate = models.IntegerField()
    likeNumber = models.IntegerField(default=0, null=True, blank=True)
    commentNumber = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(default='defaultComment.jpg', upload_to='comment_pics')
    image2 = models.ImageField(default='defaultComment.jpg', upload_to='comment_pics')
    image3 = models.ImageField(default='defaultComment.jpg', upload_to='comment_pics')
    is_Approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)


class CommentAnswer(models.Model):
    customerEmail = models.ForeignKey(Customer, on_delete=models.CASCADE)
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
    answer = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class CommentLike(models.Model):
    customerEmail = models.ForeignKey(Customer, on_delete=models.CASCADE)
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
    isLiked = models.BooleanField(blank=True, null=True)


class ClientCuisine(models.Model):
    KEBAP = 'Kebap'
    GRILL = 'Grill'
    TURKISH = 'Turkish'
    PIDE = 'Pide'
    DONER = 'Döner'
    FASTFOOD = 'Fast Food'
    HOMEMADE = 'Homemade'
    SEAFOOD = 'Seafood'
    LUNCH = 'Lunch'
    BREAKFAST = 'Breakfast'
    DINNER = 'Dinner'
    PIZZA = 'Pizza'
    CAFEANDRESTAURANT = 'Cafe & Restaurant'
    CHINESE = 'Chinese'
    KOREAN = 'Korean'
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
        (LUNCH, 'Lunch'),
        (BREAKFAST, 'Breakfast'),
        (DINNER, 'Dinner'),
        (PIZZA, 'Pizza'),
        (CHINESE, 'Chinese'),
        (KOREAN, 'Korean'),
    ]
    customerEmail = models.ForeignKey(Client, on_delete=models.CASCADE)
    cuisine = models.CharField(max_length=200, choices=CUISINES)


class ClientApplicationForm(models.Model):
    restaurant_name = models.CharField(max_length=250, unique=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    owner_surname = models.CharField(max_length=200)
    owner_email = models.EmailField(_('email address'))
    owner_phone = models.CharField(max_length=200)
    restaurant_phone = models.CharField(max_length=200)
    restaurant_email = models.EmailField(_('email address'), unique=True)
    workday_from = models.CharField(max_length=200)
    workday_to = models.CharField(max_length=200)
    workhour_from = models.CharField(max_length=200)
    workhour_to = models.CharField(max_length=200)
    restaurant_address = models.CharField(max_length=300)
    will_be_verified = models.BooleanField(default=False)


class ForgotPasswordCode(models.Model):
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    date_saved = models.DateTimeField(default=timezone.now)