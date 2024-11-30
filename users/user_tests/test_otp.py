from django.test import TestCase
from unittest.mock import patch
from app_utils import otp as OTP
from django.utils.timezone import now, timedelta
from django.conf import settings


class OTPGenerationTestCase(TestCase):
    def test_generate_otp_code(self):
        otp = OTP.generate_otp_code()
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())


class OTPExpirationTestCase(TestCase):
    def test_is_expired(self):
        otp_time = now() - timedelta(minutes=20)
        self.assertFalse(OTP.is_expired(otp_time))

        otp_time = now() - timedelta(minutes=40)
        self.assertTrue(OTP.is_expired(otp_time))

class OTPSendingTestCase(TestCase):
    @patch('app_utils.otp.send_mail')
    def test_send_email_code(self, mock_send_mail):
        mock_send_mail.return_value = 1
        result = OTP.sendEmailCode('TestUser', '123456', 'test@example.com')
        self.assertTrue(result)
        mock_send_mail.assert_called_once_with(
            "Verify your account for Nitrobills",
            """
            Hello TestUser,

            Your Nitrobills verification code is 123456. Dont share this with anyone.

            Thanks,

            Your Nitrobills team
            """,
            settings.EMAIL_HOST_USER,
            ['test@example.com']
        )

    @patch('app_utils.otp.requests.post')
    def test_send_sms_code(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Message sent successfully"}

        response = OTP.sendSMSCode('2349092202826', '123456')
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["msg"], "Message sent successfully")



