from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import qrcode 
from django.conf import settings
import os
from PIL import Image
from django.templatetags.static import static
import string
import random
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):

    def get(self, request):
        return Response({"info": "Welcome to Dowell-wifi-qrcode-app"},status=status.HTTP_200_OK)

class GenerateWifiQr(APIView):
    """
    Generates Quick Response Code for a Wifi Network
    """

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = {
            'wifi_name': 'Name / SSID of the WIFI Network',
            'wifi_password': 'Password of the wifi ',
            'encryption_type': 'Either WPA (for WPA and WPA2) or WEP or nopass if no encryption type is available'
        }
            

        return Response({'payload description': an_apiview})
    
    def post(self, request):
        try: 
            wifi_name = request.data['wifi_name']
            wifi_password = request.data['wifi_password']
            encryption_type =  request.data['encryption_type'].upper()

            if encryption_type == "" or encryption_type.lower() == "none" or encryption_type.lower() =="nopass":
                encryption_type == "nopass"

            data = f"WIFI:T:{encryption_type};S:{wifi_name};P:{wifi_password};;"

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(data)
            qr.make()

            qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

            #adding logo to the qr code
            # image_path = os.path.join(settings.STATIC_ROOT, "logo.jpg")
            # image_path = static("logo.jpg")
            logo_name = "logo.jpg"
            image_path = f"{settings.BASE_DIR}/static/{logo_name}"
            image = Image.open(image_path)
            image_width, image_height = image.size

            max_size = min(qr_img.size) // 5

            if image_width > image_height:
                new_width = max_size
                new_height = int((image_height / image_width) * max_size)
            else:
                new_width = int((image_width / image_height) * max_size)
                new_height = max_size

            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

            center_x = (qr_img.size[0] - resized_image.size[0]) // 2
            center_y = (qr_img.size[1] - resized_image.size[1]) // 2

            #creating the qr code
            qr_img.paste(resized_image, (center_x, center_y))

            image_name = f"{''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(12))}.png"
            qr_path = os.path.join(settings.BASE_DIR, 'media/wifi_qr_codes/', image_name)        
            qr_img.save(qr_path)
            # qr_image_url = f"{settings.BASE_DIR}/media/wifi_qr_codes/{image_name}"
            # print(qr_image_url)

            return Response({"success": True, 'QR_Code_URL': qr_path},status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e), "success": False}, status=HTTP_400_BAD_REQUEST)
        
