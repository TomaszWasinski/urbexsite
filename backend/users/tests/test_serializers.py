from django.test import TestCase
from ..factories import UserFactory
from ..serializers import UserCreationSerializer


class UserCreationSerializerTests(TestCase):
    def setUp(self):
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

    def test_user_creation_success(self):
        serializer = UserCreationSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid(self):
        self.data['email'] = 'invalidemail'
        serializer = UserCreationSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_validator(self):
        self.data['password'] = 'pass'  # password is too short
        self.data['confirm_password'] = 'pass'
        serializer = UserCreationSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
