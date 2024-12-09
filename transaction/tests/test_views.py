from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.utils.timezone import make_aware
from datetime import datetime
from ..models import Transaction, Beneficiaries, Autopayment, Notifications, Review


User = get_user_model()


class TransactionTests(APITestCase):
    """
    Test cases for Transaction model.
    """
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

        self.transaction = Transaction.objects.create(
            user=self.user,
            reference="TX12345",
            date=make_aware(datetime(2024, 11, 30)),
            status="Success",
            is_credit=True,
            transaction_type="Deposit",
            provider="Bank A",
            reciever_number="123456789",
            amount=1000
        )
        self.transaction_url = reverse('transactions')

    def test_list_transactions_success(self):
        """
        Test list transactions API.
        """
        response = self.client.get(self.transaction_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["reference"], self.transaction.reference)

    def test_list_transactions_no_data(self):
        """
        Test list transactions API with no data.
        """
        Transaction.objects.all().delete()
        response = self.client.get(self.transaction_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 0)


class BeneficiaryTests(APITestCase):
    """
    Test cases for Beneficiaries model.
    """
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

        self.beneficiary = Beneficiaries.objects.create(
            user=self.user,
            name="John Doe",
            provider="Bank A",
            transaction_type="Transfer",
            user_code="USER123",
            color_id=1,
            avatar_id=1
        )
        self.list_beneficiary_url = reverse('beneficiaries')
        self.create_beneficiary_url = reverse('create_beneficiary')
        self.delete_beneficiary_url = reverse('delete_beneficiary', args=[self.beneficiary.id])

    def test_list_beneficiaries_success(self):
        """
        Test list beneficiaries API.
        """
        response = self.client.get(self.list_beneficiary_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], self.beneficiary.name)

    def test_create_beneficiary_success(self):
        """
        Test create beneficiary API.
        """
        payload = {
            "name": "Jane Doe",
            "provider": "Bank B",
            "transaction_type": "Deposit",
            "user_code": "USER456",
            "color_id": 2,
            "avatar_id": 2
        }
        response = self.client.post(self.create_beneficiary_url, payload, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Beneficiaries.objects.count(), 2)

    def test_delete_beneficiary_success(self):
        """
        Test delete beneficiary API.
        """
        response = self.client.delete(self.delete_beneficiary_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Beneficiaries.objects.filter(id=self.beneficiary.id).exists())


class AutopaymentTests(APITestCase):
    """
    Test cases for Autopayment model.
    """
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

        self.autopayment = Autopayment.objects.create(
            user=self.user,
            name="Electric Bill",
            transaction_type="Payment",
            service_provider="Utility Company",
            uuid="UUID123",
            amount=200,
            number="987654321",
            amount_plan="Fixed",
            period="Monthly",
            custom_days=30,
            end_date=make_aware(datetime(2024, 12, 31))
        )
        self.list_autopay_url = reverse('autopay')
        self.create_autopay_url = reverse('create_autopay')
        self.delete_autopay_url = reverse('delete_autopay', args=[self.autopayment.id])

    def test_list_autopayments_success(self):
        """
        Test list autopayments API.
        """
        response = self.client.get(self.list_autopay_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], self.autopayment.name)

    def test_create_autopayment_success(self):
        """
        Test create autopayment API.
        """
        payload = {
            "name": "Internet Bill",
            "transaction_type": "Payment",
            "service_provider": "ISP",
            "uuid": "UUID456",
            "amount": 100,
            "number": "123123123",
            "amount_plan": "Fixed",
            "period": "Monthly",
            "custom_days": 30,
            "end_date": make_aware(datetime(2024, 12, 31))
        }
        response = self.client.post(self.create_autopay_url, payload, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Autopayment.objects.count(), 2)

    def test_delete_autopayment_success(self):
        """
        Test delete autopayment API.
        """
        response = self.client.delete(self.delete_autopay_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Autopayment.objects.filter(id=self.autopayment.id).exists())


class NotificationTests(APITestCase):
    """
    Test cases for Notifications model.
    """
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

        self.notification = Notifications.objects.create(
            user=self.user,
            type="INFO",
            message="Notification message"
        )
        self.notifications_url = reverse('notifications')

    def test_get_notifications_success(self):
        """
        Test get notifications API.
        """
        response = self.client.get(self.notifications_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["message"], self.notification.message)


class ReviewTests(APITestCase):
    """
    Test cases for Review model.
    """
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        self.create_review_url = reverse('save_review')

    def test_create_review_success(self):
        """
        Test create review API.
        """
        payload = {
            "message": "Great service!",
            "star": 5
        }
        response = self.client.post(self.create_review_url, payload, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().message, "Great service!")
