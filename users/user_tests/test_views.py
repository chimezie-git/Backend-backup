from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from rest_framework.authtoken.models import Token


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'phone_number': '1234567890'
        }

        self.user = get_user_model().objects.create_user(**self.user_data)

        Token.objects.filter(user=self.user).delete()
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()

    @patch('dj_rest_auth.registration.views.api_settings.TOKEN_SERIALIZER')
    def test_register_user(self, mock_token_serializer):
        mock_token_serializer.return_value.data = {'key': self.token.key}

        url = reverse('account_signup')
        data = {
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password1": "password@123",
            "password2": "password@123",
            "phone_number": "0987654321"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('key' in response.data)
