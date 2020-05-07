from decimal import Decimal
from django import test
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth import get_user_model, login
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from YeOradaApp.models import *
from django.contrib.auth.models import User

import unittest
import os


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNotNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNotNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class UserViewTest(TestCase):

    def test_view_url_exists_at_desired_location_home(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yeoradamain/index.html')

    def test_view_url_exists_at_desired_location_clientsearch(self):
        response = self.client.get('/clientsearch')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_clientsearch(self):
        response = self.client.get(reverse('clientsearch'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_clientsearch(self):
        response = self.client.get(reverse('clientsearch'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yeoradamain/partners.html')


class SettingsTest(TestCase):

    def test_password_change(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        passwordChangeForm = PasswordChangeForm(user, data={'old_password': "foo", 'new_password1': "Foo_123456", 'new_password2': "Foo_123456"})
        if passwordChangeForm.is_valid():
            passwordChangeForm.save()
        u = User.objects.get(email='normal@user.com')
        self.assertEqual(u.check_password('Foo_123456'), True)

    def test_save_changes(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', surname="surname", name='name', username='username')
        customer=Customer.objects.create(userEmail=user, city='city', state='state')
        name = 'name1'
        surname = 'surname1'
        city = 'city1'
        country = 'country1'
        username = 'username1'
        userObject = RegisteredUser.objects.filter(email=user.email).first()
        customerObject = Customer.objects.filter(userEmail=user).first()
        userObject.name = name;
        userObject.surname = surname;
        userObject.username = username;

        customerObject.city = city;
        customerObject.country = country;

        userObject.save()
        customerObject.save()

        self.assertEqual(userObject.surname, surname)
        self.assertEqual(userObject.name, name)
        self.assertEqual(userObject.username, username)
        self.assertEqual(customerObject.city, city)
        self.assertEqual(customerObject.country, country)


class LikeTest(TestCase):

    def test_likeComment_zero(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', surname="surname", name='name',
                                        username='username')
        customer = Customer.objects.create(userEmail=user, city='city', state='state')
        user1 = User.objects.create_user(email='normal1@user.com', password='foo', surname="surname", name='name',
                                         username='username1')
        client = Client.objects.create(userEmail=user1)
        comment1= Comment(customerEmail=customer, clientEmail=client, date='2011-11-11', text="Çok güzel yorum", rate=Decimal(4.0), likeNumber=0, commentNumber=0,)
        comment1.save()
        commentId = comment1.id
        commentId2 = Comment.objects.filter(id=commentId).first()
        customerEmail = Customer.objects.filter(userEmail=user).first()
        commentLike = CommentLike.objects.filter(customerEmail=customerEmail, commentId=commentId2)
        if commentLike.count() == 0:
            createCommentLike = CommentLike(customerEmail=customerEmail, commentId=commentId2, isLiked=True)
            createCommentLike.save()
        self.assertEqual(createCommentLike.isLiked, True)

    def test_likeComment_decrease(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', surname="surname", name='name',
                                        username='username')
        customer = Customer.objects.create(userEmail=user, city='city', state='state')
        user1 = User.objects.create_user(email='normal1@user.com', password='foo', surname="surname", name='name',
                                         username='username1')
        client = Client.objects.create(userEmail=user1)
        comment1 = Comment(customerEmail=customer, clientEmail=client, date='2011-11-11', text="Çok güzel yorum", rate=Decimal(4.0), likeNumber=1, commentNumber=0)
        comment1.save()
        commentId = Comment.objects.filter(customerEmail=customer, clientEmail=client, date='2011-11-11', text="Çok güzel yorum").first()
        print(commentId)

        commentId2 = Comment.objects.filter(id=commentId.id).first()

        customerEmail = Customer.objects.filter(userEmail=user).first()
        print(customerEmail)

        commentLikeObject = CommentLike(customerEmail=customerEmail, commentId=commentId, isLiked=True)
        commentLikeObject.save()

        commentLike = CommentLike.objects.filter(customerEmail=customerEmail, commentId=commentId)
        print(commentLike)

        if commentLike.first().isLiked and commentLike.count() == 1:
            commentLike.update(isLiked=False)
            if commentId2.likeNumber >= 0:
                commentId2.likeNumber -= 1
            commentId2.save()
        self.assertLess(commentId2.likeNumber, comment1.likeNumber)

    def test_likeComment_increase(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', surname="surname", name='name',
                                        username='username')
        customer = Customer.objects.create(userEmail=user, city='city', state='state')
        user1 = User.objects.create_user(email='normal1@user.com', password='foo', surname="surname", name='name',
                                        username='username1')
        client = Client.objects.create(userEmail=user1)
        comment1 = Comment(customerEmail=customer, clientEmail=client, date='2011-11-11', text="Çok güzel yorum", rate=Decimal(4.0), likeNumber=1, commentNumber=0)
        comment1.save()
        commentId = comment1.id
        commentId2 = Comment.objects.filter(id=commentId).first()
        customerEmail = Customer.objects.filter(userEmail=user).first()
        commentLike = CommentLike.objects.filter(customerEmail=customerEmail, commentId=commentId2)
        if commentLike.count() == 0:
            createCommentLike = CommentLike(customerEmail=customerEmail, commentId=commentId2, isLiked=True)
            createCommentLike.save()
        else:
            commentLike.update(isLiked=True)
            commentId2.likeNumber += 1
            commentId2.save()
        self.assertEqual(commentLike.get().isLiked, True)
        self.assertEqual(commentId2.likeNumber, comment1.likeNumber)


class HomePage(TestCase):

    def test_search_restaurant(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', surname="surname", name='name',
                                        username='username')
        client = Client.objects.create(userEmail=user, name="User Restaurant", city="İstanbul", state="Kadıköy")
        c = test.Client()
        c.login(username='normal@user.com', password='foo')

        response = c.post('/clientsearch',
                              {'restaurant': 'User Restaurant', 'city_input': 'İstanbul', 'state_input': 'Kadıköy', 'searchRestaurant': 'True', }, encoding='utf-8')
        self.assertEqual(response.status_code, 200)


class PostReview(TestCase):

    def test_post_review(self):
        User = get_user_model()
        c = test.Client()
        user = User.objects.create_user(email='normal@user.com', password='foo', surname="surname", name='name',
                                        username='username')
        clientObject = Client.objects.create(userEmail=user, name="User Restaurant-1", city="İstanbul", state="Kadıköy")

        c.login(username='normal@user.com', password='foo')

        with open('test.png', 'rb') as fp:
            response = c.post('/clientprofile/username', {'text': 'Test Comment 1', 'fileOneChecking': fp, 'fileTwoChecking': fp, 'fileThrChecking': fp, 'rate': '4', 'publishReview': 'True', }, encoding='utf-8')
            self.assertEqual(response.status_code, 200)


class DeactiveAccount(TestCase):

    def test_deactive_account(self):
        User = get_user_model()
        c = test.Client()
        user = User.objects.create_user(email='normal@user.com', password='foo', surname="surname", name='name',
                                        username='username', isCustomer=True)
        c.login(username='normal@user.com', password='foo')
        url = reverse('home')
        homeres = c.get(url)
        print(homeres)
        response = c.post('/clientsettings',
                          {'Email': 'normal@user.com',
                           'yourEmail': 'True', }, encoding='utf-8', follow=True)
        self.assertEqual(response.status_code, 200)


class PostAnswer(TestCase):

    def test_post_answer(self):
        User = get_user_model()
        c = test.Client()
        user = User.objects.create_user(email='normal@user.com', password='foo', surname="surname", name='name',
                                        username='username', isCustomer=True)
        customerObject = Customer.objects.create(userEmail=user)

        user_client = User.objects.create_user(email='normal@client.com', password='foo', surname="surname", name='name',
                                        username='username_client', isClient=True)

        clientObject = Client.objects.create(userEmail=user_client, name="User Restaurant-1", city="İstanbul", state="Kadıköy")

        c.login(username='normal@user.com', password='foo')

        comment = Comment(customerEmail=customerObject, clientEmail=clientObject, text='Test Comment', rate=Decimal(4.0))
        comment.save()
        commentObject = Comment.objects.filter(customerEmail=customerObject, clientEmail=clientObject).first()

        response = c.post('/clientprofile/username_client',
                          {'post': 'Test Answer', 'commentId': commentObject.id,
                           'postComment': 'True', }, encoding='utf-8', follow=True)
        self.assertEqual(response.status_code, 200)


class AdminSettings(TestCase):

    def test_admin_settings_save(self):
        User = get_user_model()
        c = test.Client()
        user = User.objects.create_user(email='normal@user.com', password='foo', surname="surname", name='name',
                                        username='username', isAdmin=True)
        c.login(username='normal@user.com', password='foo')
        response = c.post('/adminsettings',
                          {'name': 'name', 'surname': 'surname', 'email': 'normal@user.com', 'username': 'username',
                           'saveChanges2': 'True', }, encoding='utf-8', follow=True)
        self.assertEqual(response.status_code, 200)











