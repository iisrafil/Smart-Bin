from rest_framework import serializers

from api.models import Data, Device, AppUser


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('device', 'height', 'gas', 'temp', 'humidity')
        depth = 0


class SendDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('device', 'time', 'percent', 'gas', 'unwanted_gas', 'temp', 'humidity')
        depth = 0


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'location', 'percentage', 'lastFullTime', 'lastCleanTime',)
        depth = 0


class DeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'location', 'percentage', 'lastFullTime', 'lastCleanTime', 'gas', 'temp', 'humidity')
        depth = 0


class UserReceiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('id',)
        depth = 0


class UserSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True)

    class Meta:
        model = AppUser
        fields = ['id', 'status', 'devices']
        depth = 1


class NotificationSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    status = serializers.BooleanField(default=False)


class Notification(object):

    def __init__(self, id, status):
        self.id = id
        self.status = status
