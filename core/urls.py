from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# import dj_rest_auth.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),
    path("api/auth/", include("users.urls")),
    # path("api/auth/", include("dj_rest_auth.urls")),
    path("api/webhook/", include("webhook.urls")),
    path("api/bills/", include("bills.urls")),
    path("api/data/", include("transaction.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(), name="redoc"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(), name="redoc"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(), name="swagger"),
]
