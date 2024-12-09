from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Transaction, Beneficiaries, BankInfo, Autopayment, Notifications, Review
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone


class TransactionModelTests(TestCase):
    """
    Test cases for the Transaction model.
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
        )

    def test_transaction_creation(self):
        """
        Test creating a transaction.
        """
        transaction = Transaction.objects.create(
            user=self.user,
            reference="REF123",
            status="P",
            is_credit=True,
            transaction_type="CR",
            provider="PayPal",
            amount=Decimal("100.50"),
            reciever_number="1234567890",
        )
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.reference, "REF123")
        self.assertTrue(transaction.is_credit)
        self.assertEqual(transaction.transaction_type, "CR")
        self.assertEqual(transaction.provider, "PayPal")
        self.assertEqual(transaction.amount, Decimal("100.50"))
        self.assertEqual(transaction.reciever_number, "1234567890")

    def test_beneficiaries_creation(self):
        """
        Test creating a beneficiary.
        """
        transaction = Transaction.objects.create(
            user=self.user,
            reference="REF456",
            status="S",
            is_credit=False,
            transaction_type="DR",
            provider="BankTransfer",
            amount=Decimal("200.00"),
            reciever_number="0987654321",
        )
        beneficiary = Beneficiaries.objects.create(
            user=self.user,
            name="John Doe",
            transaction_type="DR",
            provider="BankTransfer",
            user_code="USR123",
            color_id=1,
            avatar_id=2,
            last_payment=transaction,
        )
        self.assertEqual(beneficiary.user, self.user)
        self.assertEqual(beneficiary.name, "John Doe")
        self.assertEqual(beneficiary.transaction_type, "DR")
        self.assertEqual(beneficiary.provider, "BankTransfer")
        self.assertEqual(beneficiary.last_payment, transaction)

    def test_bank_info_credit_method(self):
        """
        Test the credit method of the BankInfo model.
        """
        bank_info = BankInfo.objects.create(
            user=self.user,
            email="testuser@example.com",
            amount=Decimal("1000.00"),
            customer_id=1,
            customer_code="CUST123",
            account_number="123456789",
            account_name="Test User",
            bank_name="Test Bank",
        )
        bank_info.credit(Decimal("500.00"))
        self.assertEqual(bank_info.amount, Decimal("1500.00"))

    def test_autopayment_creation(self):
        """
        Test creating an autopayment.
        """
        transaction = Transaction.objects.create(
            user=self.user,
            reference="REF789",
            status="C",
            is_credit=True,
            transaction_type="CR",
            provider="Stripe",
            amount=Decimal("300.00"),
            reciever_number="1122334455",
        )
        autopayment = Autopayment.objects.create(
            user=self.user,
            last_payment=transaction,
            name="Netflix",
            amount=Decimal("15.99"),
            uuid="autopay-123",
            transaction_type="SUB",
            service_provider="Netflix",
            number="1122334455",
            amount_plan="Monthly",
            period="MO",
            custom_days=30,
            end_date=timezone.now() + timedelta(days=30),
        )
        self.assertEqual(autopayment.name, "Netflix")
        self.assertEqual(autopayment.amount, Decimal("15.99"))
        self.assertEqual(autopayment.service_provider, "Netflix")
        self.assertEqual(autopayment.period, "MO")

    def test_notifications_creation(self):
        """
        Test creating a notification.
        """
        notification = Notifications.objects.create(
            user=self.user,
            type="AL",
            message="This is an alert notification.",
        )
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.type, "AL")
        self.assertEqual(notification.message, "This is an alert notification.")

    def test_review_creation(self):
        """
        Test creating a review.
        """
        review = Review.objects.create(
            user=self.user,
            message="Great service!",
            star=5,
        )
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.message, "Great service!")
        self.assertEqual(review.star, 5)
