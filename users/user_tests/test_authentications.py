from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.authentication import EmailAuthBackend
from users.authentication import PhoneAuthBackend
from datetime import timedelta
from django.utils import timezone
from users.models import CustomUser


class EmailAuthBackendTestCase(TestCase):
    """Test cases for the EmailAuthBackend class"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword"
        )

    def test_authenticate_with_correct_credentials(self):
        """Test authenticate method with correct credentials"""
        backend = EmailAuthBackend()
        user = backend.authenticate(None, username="test@example.com", password="securepassword")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")

    def test_authenticate_with_incorrect_password(self):
        """Test authenticate method with incorrect password"""
        backend = EmailAuthBackend()
        user = backend.authenticate(None, username="test@example.com", password="wrongpassword")
        self.assertIsNone(user)

    def test_authenticate_with_nonexistent_email(self):
        """Test authenticate method with nonexistent email"""
        backend = EmailAuthBackend()
        user = backend.authenticate(None, username="nonexistent@example.com", password="securepassword")
        self.assertIsNone(user)

    def test_get_user(self):
        """Test get_user method"""
        backend = EmailAuthBackend()
        user = backend.get_user(self.user.id)
        self.assertEqual(user, self.user)


class PhoneAuthBackendTestCase(TestCase):
    """Test cases for the PhoneAuthBackend class"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            phone_number="1234567890",
            otp_code="123456"
        )
        self.user.otp_time = timezone.now()
        self.user.save()

    def test_authenticate_with_correct_credentials(self):
        """Test authenticate method with correct credentials"""
        backend = PhoneAuthBackend()
        user = backend.authenticate(None, username="1234567890", password="123456")
        self.assertIsNotNone(user)
        self.assertEqual(user.phone_number, "1234567890")

    def test_authenticate_with_incorrect_otp(self):
        """Test authenticate method with incorrect otp"""
        backend = PhoneAuthBackend()
        user = backend.authenticate(None, username="1234567890", password="654321")
        self.assertIsNone(user)

    # TODO: def test_authenticate_with_expired_otp(self):
    #     """Test authenticate method with expired OTP"""


    def test_authenticate_with_nonexistent_phone_number(self):
        """Test authenticate method with nonexistent phone number"""
        backend = PhoneAuthBackend()
        user = backend.authenticate(None, username="9876543210", password="123456")
        self.assertIsNone(user)

    def test_get_user(self):
        """Test get_user method"""
        backend = PhoneAuthBackend()
        user = backend.get_user(self.user.id)
        self.assertEqual(user, self.user)
