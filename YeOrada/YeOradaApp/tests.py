from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from YeOradaApp.models import*
import unittest
import os
from django.test import TestCase


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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_like_comment(self):
        User = get_user_model()

    def test_client_profile(self):
        User = get_user_model()

    def test_settings(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')

    def test_my_profile(self):
        User = get_user_model()

    def test_details(self):
        response = self.client.get('/customer/details/')
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.client.get('/customer/index/')
        self.assertEqual(response.status_code, 200)

