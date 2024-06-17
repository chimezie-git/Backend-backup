from django.urls import path
from transaction import views

urlpatterns = [
    path("transactions/", views.ListTransactions.as_view()),
    path("beneficiaries/", views.ListBeneficiaries.as_view()),
    path("beneficiaries/create/", views.CreateBeneficiaryApiView.as_view()),
    path("beneficiaries/delete/<int:id>", views.DeleteBeneficiaryApiView.as_view()),
]