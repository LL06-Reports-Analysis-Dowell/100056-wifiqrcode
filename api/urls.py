from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('server-status', serverStatus.as_view()),
    path('generate_qr', GenerateWifiQr.as_view()),
    path('download/<str:filename>', DownloadQRCode),
    path("register/", UserRegister.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('public', Public.as_view()),
]
