from django.urls import path
from api.views import *

urlpatterns = [
    path('server-status', serverStatus.as_view()),
]
