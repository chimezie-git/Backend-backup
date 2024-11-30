from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser, UserData

class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            phone_number='1234567890',
            password='password123'
        )

    def test_custom_user_model_fields(self):
        """Test if the CustomUser fields are correctly saved and retrieved."""
        self.assertEqual(self.user.phone_number, '1234567890')

        self.assertFalse(self.user.email_verified)
        self.assertFalse(self.user.phone_verified)

        self.assertEqual(self.user.otp_code, '')

        self.assertTrue(timezone.now() - self.user.otp_time < timedelta(seconds=1))

        self.assertEqual(self.user.referral_code, "")

    def test_custom_user_model_defaults(self):
        """Test the default values of the CustomUser model fields."""
        user = CustomUser.objects.create_user(
            username='newuser',
            phone_number='9876543210',
            password='newpassword123'
        )

        self.assertFalse(user.email_verified)
        self.assertFalse(user.phone_verified)
        self.assertEqual(user.otp_code, "")
        self.assertEqual(user.referral_code, "")


class UserDataModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            phone_number='1234567890',
            password='password123'
        )
        self.user_data = UserData.objects.create(
            user=self.user,
            amount=100.00,
            pin_code="12345"
        )

    def test_userdata_model_fields(self):
        """Test if the UserData fields are correctly saved and retrieved."""
        self.assertEqual(self.user_data.amount, 100.00)

        self.assertEqual(self.user_data.pin_code, '12345')

        self.assertEqual(self.user_data.referral_count, 0)

        self.assertEqual(self.user_data.user, self.user)

    def test_add_referral(self):
        """Test if the add_referral method increments referral_count."""
        self.assertEqual(self.user_data.referral_count, 0)

        self.user_data.add_referral()

        self.assertEqual(self.user_data.referral_count, 1)

    def test_userdata_one_to_one_relationship(self):
        """Test if the one-to-one relationship between CustomUser and UserData works."""
        user_data = UserData.objects.get(user=self.user)

        self.assertEqual(user_data.user.username, 'testuser')

    def test_referral_count_increase(self):
        """Test if the referral count increases correctly."""
        self.user_data.add_referral()
        self.user_data.add_referral()

        self.assertEqual(self.user_data.referral_count, 2)
