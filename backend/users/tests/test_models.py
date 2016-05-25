from django.core.exceptions import ValidationError
from django.test import TestCase
from ..factories import UserFactory
from ..models import User


class UserModelTests(TestCase):
    def test_user_creation_is_valid(self):
        user = User(email='test_user@gmail.com', password='Pass12#$%', username='test_user')
        self.assertIsNone(user.full_clean())

    def test_user_creation_without_pass_raises_error(self):
        user = User(email='test_user@gmail.com', username='test_user')
        with self.assertRaises(ValidationError):
            user.full_clean()


class UserManagerTests(TestCase):
    def test_superuser_creation(self):
        self.assertEqual(User.objects.count(), 0)
        User.objects.create_superuser(email='admin@gmail.com', password='Pass12#$%')
        self.assertEqual(User.objects.count(), 1)

    def test_simple_user_creation(self):
        self.assertEqual(User.objects.count(), 0)
        User.objects.create(
            email='test_user@gmail.com',
            username='test_user',
            password='Pass12#$%'
        )
        self.assertEqual(User.objects.count(), 1)

    def test_full_user_creation(self):
        user = User.objects.create('test_full_user@gmail.com', 'test_full_user')
        user.name = 'Test'
        user.last_name = 'User'
        user.birth_date = '2001-01-01'
        user.gender = ''
        user.save()
        saved_user = User.objects.first()
        self.assertEqual(saved_user.name, user.name)
        self.assertEqual(saved_user.last_name, user.last_name)
        self.assertEqual(str(saved_user.birth_date), user.birth_date)
        self.assertEqual(saved_user.gender, user.gender)

    def test_model_str(self):
        user = UserFactory.create()
        self.assertEqual(str(user), user.email)
