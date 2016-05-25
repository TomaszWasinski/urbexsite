import json

from configuration.celery import app
from django.core.urlresolvers import reverse
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase
from ..factories import UserFactory
from ..models import User


class UserCreationTests(APITestCase):
    def setUp(self):
        app.conf.CELERY_ALWAYS_EAGER = True

        self.user = UserFactory.build()
        self.data = {
            'email': self.user.email,
            'username': self.user.username,
            'password': 'Pass12#$%',
            'confirm_password': 'Pass12#$%',
            'name': self.user.name,
            'last_name': self.user.last_name,
            'birth_date': self.user.birth_date,
            'gender': self.user.gender,
        }

    def test_success_user_creation(self):
        response = self.client.post(reverse('user-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_failed_user_creation(self):
        self.data['email'] = 'invalidemail'
        response = self.client.post(reverse('user-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_send_email(self):
        response = self.client.post(reverse('user-list'), self.data, format='json')
        self.assertEqual(mail.outbox[0].subject, 'Account confirmation!')

    def test_mail_activation(self):
        self.user = UserFactory.create()
        response = self.client.get(reverse('activation', args=[self.user.activation_key]), follow=True,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_mail_activation_with_wrong_key(self):
        self.user = UserFactory.create()
        self.user.activation_key = '123wrongkey456'
        response = self.client.get(reverse('activation', args=[self.user.activation_key]), follow=True,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.data)


class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.data = {
            'email': self.user.email,
            'password': 'pass',
        }
        self.assertTrue(self.client.login(email=self.user.email, password='pass'))

        self.url = reverse('token-auth')
        self.response = self.client.post(self.url, self.data, format='json')
        self.token = self.response.data['token']

    def test_success_auth_user(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_failed_auth_user(self):
        self.data['password'] = 'invalidpassword'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_valid_token(self):
        response = self.client.post(reverse('token-verify'), {'token': self.token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_invalid_token(self):
        self.token = 'invalidtoken'
        response = self.client.post(reverse('token-verify'), {'token': self.token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)


class UserViewPermissionTests(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.data = {
            'email': self.user.email,
            'password': 'pass',
        }
        self.url = reverse('token-auth')
        self.assertTrue(self.client.login(email=self.user.email, password='pass'))

    def test_authenticated_user_details(self):
        response = self.client.get(reverse('user-detail', args=[self.user.pk]), follow=True,
                                   content_type='application/json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['username'], self.user.username)

    def test_not_authenticated_user_details(self):
        self.another_user = UserFactory.create()
        response = self.client.get(reverse('user-detail', args=[self.user.pk]), follow=True,
                                   content_type='application/json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(result['username'], self.another_user.username)


class UserViewSetTests(APITestCase):
    def setUp(self):
        self.user_one = UserFactory.create()
        self.user_two = UserFactory.create()
        self.user_three = UserFactory.create()

    def test_users_list(self):
        response = self.client.get(reverse('user-list'), follow=True, content_type='application/json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), User.objects.all().count())

    def test_invalid_user(self):
        response = self.client.get(reverse('user-detail', args=['5']), follow=True,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # user not found
