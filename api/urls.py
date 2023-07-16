from django.urls import path
from api.views import *

urlpatterns = [
    path('server-status', serverStatus.as_view()),
    path('generate_qr', GenerateWifiQr.as_view()),
    path('download/<str:filename>', DownloadQRCode),
    path('public', Public.as_view()),
]
