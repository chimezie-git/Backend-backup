from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dj_rest_auth.models import TokenModel

class LoginViewTestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "phone_number": "1234567890",
        }

        self.user = get_user_model().objects.create_user(**self.user_data)
        self.user.phone_verified = True  # Set the phone as verified
        self.user.save()

        self.login_url = reverse('rest_login')

    def test_login_with_valid_credentials(self):
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("key", response.data)
        self.assertIn("verified", response.data)
        self.assertEqual(response.data["verified"], True)
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["phone_number"], self.user_data["phone_number"])

    def test_login_with_invalid_credentials(self):
        data = {
            "username": self.user_data["username"],
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_login_without_username(self):
        data = {
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertIn('Must include "username" and "password".', response.data["non_field_errors"])


    def test_login_without_password(self):
        data = {
            "username": self.user_data["username"],
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
