from django.test import TestCase
from django.contrib.admin.sites import site
from ..models import Transaction, Beneficiaries, BankInfo, Autopayment, Notifications, Review
from ..admin import (
    TransactionAdmin,
    BeneficiaryAdmin,
    BankInfoAdmin,
    AutopaymentAdmin,
    NotificationAdmin,
    ReviewAdmin,
)


class AdminPageTests(TestCase):
    """
    Test cases for the Django admin configuration.
    """

    def test_transaction_admin_registration(self):
        """
        Test that the Transaction model is registered in the admin site.
        """
        self.assertIn(Transaction, site._registry)
        self.assertIsInstance(site._registry[Transaction], TransactionAdmin)

    def test_beneficiary_admin_registration(self):
        """
        Test that the Beneficiaries model is registered in the admin site.
        """
        self.assertIn(Beneficiaries, site._registry)
        self.assertIsInstance(site._registry[Beneficiaries], BeneficiaryAdmin)

    def test_bank_info_admin_registration(self):
        """
        Test that the BankInfo model is registered in the admin site.
        """
        self.assertIn(BankInfo, site._registry)
        self.assertIsInstance(site._registry[BankInfo], BankInfoAdmin)

    def test_autopayment_admin_registration(self):
        """
        Test that the Autopayment model is registered in the admin site.
        """
        self.assertIn(Autopayment, site._registry)
        self.assertIsInstance(site._registry[Autopayment], AutopaymentAdmin)

    def test_notification_admin_registration(self):
        """
        Test that the Notifications model is registered in the admin site.
        """
        self.assertIn(Notifications, site._registry)
        self.assertIsInstance(site._registry[Notifications], NotificationAdmin)

    def test_review_admin_registration(self):
        """
        Test that the Review model is registered in the admin site.
        """
        self.assertIn(Review, site._registry)
        self.assertIsInstance(site._registry[Review], ReviewAdmin)

    def test_transaction_admin_configuration(self):
        """
        Test the configuration of the TransactionAdmin.
        """
        admin_obj = site._registry[Transaction]
        self.assertEqual(admin_obj.list_display, ('user', 'provider',
                                                    'amount', 'status',
                                                    'date', 'reciever_number')
                                                    )
        self.assertEqual(admin_obj.search_fields, ('user', 'provider',
                                                    'reciever_number', '')
                                                    )
        self.assertEqual(admin_obj.list_filter, ('status', 'provider'))
        self.assertEqual(admin_obj.date_hierarchy, 'date')
        self.assertEqual(admin_obj.ordering, ('-date',))

    def test_beneficiary_admin_configuration(self):
        """
        Test the configuration of the BeneficiaryAdmin.
        """
        admin_obj = site._registry[Beneficiaries]
        self.assertEqual(admin_obj.list_display, ('user', 'provider',
                                                    'name', 'user_code')
                                                    )
        self.assertEqual(admin_obj.search_fields, ('user', 'provider', 'name'))
        self.assertEqual(admin_obj.list_filter, ('provider',))

    def test_bank_info_admin_configuration(self):
        """
        Test the configuration of the BankInfoAdmin.
        """
        admin_obj = site._registry[BankInfo]
        self.assertEqual(admin_obj.list_display, ('user', 'amount',
                                                    'account_status', 'bank_name')
                                                    )
        self.assertEqual(admin_obj.search_fields, ('user', 'bank_name'))
        self.assertEqual(admin_obj.list_filter, ('bank_name',))

    def test_autopayment_admin_configuration(self):
        """
        Test the configuration of the AutopaymentAdmin.
        """
        admin_obj = site._registry[Autopayment]
        self.assertEqual(admin_obj.list_display, ('user', 'name',
                                                    'service_provider', 'number',
                                                    'amount_plan', 'end_date')
                                                    )
        self.assertEqual(admin_obj.search_fields, ('user', 'name', 'service_provider'))
        self.assertEqual(admin_obj.list_filter, ('service_provider', 'period'))

    def test_notification_admin_configuration(self):
        """
        Test the configuration of the NotificationAdmin.
        """
        admin_obj = site._registry[Notifications]
        self.assertEqual(admin_obj.list_display, ('user', 'message', 'type'))
        self.assertEqual(admin_obj.search_fields, ('user', 'type'))
        self.assertEqual(admin_obj.list_filter, ('type',))

    def test_review_admin_configuration(self):
        """
        Test the configuration of the ReviewAdmin.
        """
        admin_obj = site._registry[Review]
        self.assertEqual(admin_obj.list_display, ('user', 'message', 'star'))
        self.assertEqual(admin_obj.search_fields, ('user', 'star'))
        self.assertEqual(admin_obj.list_filter, ('star',))
