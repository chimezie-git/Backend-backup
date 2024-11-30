from django.urls import path
from transaction import views

urlpatterns = [
    # transactions
    path("transactions/", views.ListTransactions.as_view()),
    # beneficiaries
    path("beneficiaries/", views.ListBeneficiaries.as_view()),
    path("beneficiaries/create/", views.CreateBeneficiaryApiView.as_view()),
    path("beneficiaries/delete/<int:id>/",
         views.DeleteBeneficiaryApiView.as_view()),
    # autopayment
    path("autopay/", views.ListAutopayApiView.as_view()),
    path("autopay/create/", views.CreateAutopayApiView.as_view()),
    path("autopay/update/<int:id>/", views.UpdateAutopayApiView.as_view()),
    path("review/", views.SaveReviewApiView.as_view()),
    path("autopay/delete/<int:id>/",
         views.DeleteAutopayApiView.as_view()),
    # notifications
    path("notifications/", views.GetNotificationsApiView.as_view()),
]
