from rest_framework import serializers

class WifiQrSerializer(serializers.Serializer):
    wifi_name = serializers.CharField(max_length=200)
    wifi_password = serializers.CharField(max_length=200)
    encryption_type =  serializers.CharField(max_length=200)
