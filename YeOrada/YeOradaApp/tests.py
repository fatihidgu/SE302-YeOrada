from decimal import Decimal
from django.test import TestCase, Client
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
        customer=Customer.objects.create(userEmail=user, city='city', country='country')
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
        customer = Customer.objects.create(userEmail=user, city='city', country='country')
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
        customer = Customer.objects.create(userEmail=user, city='city', country='country')
        user1 = User.objects.create_user(email='normal1@user.com', password='foo', surname="surname", name='name',
                                         username='username1')
        client = Client.objects.create(userEmail=user1)
        comment1= Comment(customerEmail=customer, clientEmail=client, date='2011-11-11', text="Çok güzel yorum", rate=Decimal(4.0), likeNumber=1, commentNumber=0)
        comment1.save()
        commentId = Comment.objects.filter(text="Çok güzel yorum",date='2011-11-11').first()

        commentId2 = Comment.objects.filter(id=commentId.id).first()

        customerEmail = Customer.objects.filter(userEmail=user).first()

        commentLike = CommentLike.objects.filter(customerEmail=customerEmail, commentId=commentId)

        if commentLike.count() == 1:
            createCommentLike = CommentLike(customerEmail=customerEmail, commentId=commentId2, isLiked=True)
            createCommentLike.save()
        else:
            if commentLike.first().isLiked:
                commentLike.update(isLiked=False)
                if (commentId2.likeNumber >= 0):
                    commentId2.likeNumber -= 1
                commentId2.save()
        self.assertEqual(commentId2.likeNumber, comment1.likeNumber)

    def test_likeComment_increase(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo', surname="surname", name='name',
                                        username='username')
        customer = Customer.objects.create(userEmail=user, city='city', country='country')
        user1 = User.objects.create_user(email='normal1@user.com', password='foo', surname="surname", name='name',
                                        username='username1')
        client=Client.objects.create(userEmail=user1)
        comment1= Comment(customerEmail=customer, clientEmail=client, date='2011-11-11', text="Çok güzel yorum", rate=Decimal(4.0), likeNumber=1, commentNumber=0)
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

