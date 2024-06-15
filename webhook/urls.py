from django.urls import path
from webhook import views

urlpatterns = [
    path("temii/", views.TemiiWebhook.as_view(), name="temi_webhook"),
]