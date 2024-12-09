from django.urls import path
from transaction import views

urlpatterns = [
    # transactions
    path("transactions/", views.ListTransactions.as_view(), name='transactions'),
    # beneficiaries
    path("beneficiaries/", views.ListBeneficiaries.as_view(), name='beneficiaries'),
    path("beneficiaries/create/", views.CreateBeneficiaryApiView.as_view(), name='create_beneficiary'),
    path("beneficiaries/delete/<int:id>/", views.DeleteBeneficiaryApiView.as_view(), name='delete_beneficiary'),
    # autopayment
    path("autopay/", views.ListAutopayApiView.as_view(), name='autopay'),
    path("autopay/create/", views.CreateAutopayApiView.as_view(), name='create_autopay'),
    path("autopay/update/<int:id>/", views.UpdateAutopayApiView.as_view(), name='update_autopay'),
    path("review/", views.SaveReviewApiView.as_view(), name='save_review'),
    path("autopay/delete/<int:id>/", views.DeleteAutopayApiView.as_view(), name='delete_autopay'),
    # notifications
    path("notifications/", views.GetNotificationsApiView.as_view(), name='notifications'),
]
