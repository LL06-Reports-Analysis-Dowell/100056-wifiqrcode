import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import qrcode 
from django.conf import settings
import os


@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):

    def get(self, request):
        return Response({"info": "Welcome to Dowell-wifi-qrcode-app"},status=status.HTTP_200_OK)

class GenerateWifiQr(APIView):
    """
    Generates Quick Response Code for a Wifi Network
    """

    def post(self, request):
        wifi_name = request.data['wifi_name']
        wifi_password = request.data['wifi_password']
        encryption_type =  request.data['encryption_type'].upper()

        if encryption_type == "" or encryption_type.lower() == "none" or encryption_type.lower() =="nopass":
            encryption_type == "nopass"

        data = f"WIFI:T:{encryption_type};S:{wifi_name};P:{wifi_password};;"

        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")
        # image_name = wifi_name + ".png"
        # qr_path = os.path.join(settings.BASE_DIR, 'data/', image_name)
        qr_image.save("wifi.png")

        return Response({"info": "QrCode Generated Successfully"},status=status.HTTP_200_OK)
        
