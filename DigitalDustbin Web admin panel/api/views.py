from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# Create your views here.
from rest_framework.decorators import api_view

from api.models import Device, Data, AppUser
from api.serializers import DataSerializer, SendDataSerializer, UserReceiveSerializer, UserSerializer, \
    DeviceInfoSerializer, NotificationSerializer, Notification


@api_view(['GET', 'POST'])
def data_list(request):
    if request.method == 'GET':
        d_id = request.GET.get('id', '')
        device = Device.objects.get(id=d_id)
        data = Data.objects.filter(device=device).last()
        serializer = SendDataSerializer(data, many=False)
        return JsonResponse({'data': serializer.data})

    if request.method == 'POST':
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            device = Device.objects.get(id=request.data["device"])
            previousPercent = Data.objects.filter(device=device).last().percent

            data = serializer.save()
            data.device = device

            bin_height = device.dustbinHeight
            bin_height_now = data.height
            percent = int(100 - ((bin_height_now / bin_height) * 100))
            if data.gas > 400:
                data.unwanted_gas = True
            else:
                data.unwanted_gas = False

            device.percentage = percent
            device.gas = data.gas
            device.temp = data.temp
            device.humidity = data.humidity
            device.save()

            data.percent = percent
            data.save()

            if previousPercent < 90 and percent >= 90:
                device.lastFullTime = datetime.now()
                device.save()

            if previousPercent > 10 and percent <= 10:
                device.lastCleanTime = datetime.now()
                device.save()

            return JsonResponse({'save': "200"})


@api_view(['GET'])
def device_info(request):
    if request.method == 'GET':
        d_id = request.GET.get('id', '')
        device = Device.objects.get(id=d_id)
        serialized = DeviceInfoSerializer(device, many=False)
        return JsonResponse({'data': serialized.data})


@api_view(['GET', 'POST'])
def user_handle(request):
    if request.method == 'POST':
        serializer = UserReceiveSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            serializer = UserSerializer(user)
            return JsonResponse({'data': serializer.data})

        else:
            user = AppUser.objects.get(id=request.data["id"])
            serializer = UserSerializer(user)
            return JsonResponse({'data': serializer.data})
    elif request.method == 'GET':
        u_id = request.GET.get('id', '')
        user = AppUser.objects.get(id=u_id)
        serializer = UserSerializer(user)
        return JsonResponse({'data': serializer.data})


@api_view(['GET'])
def notification(request):
    u_id = request.GET.get('id', '')
    user = AppUser.objects.get(id=u_id)
    try:
        device = Device.objects.filter(user=user).filter(percentage__gte=90).first()

    except Device.DoesNotExist:
        notificationapi = Notification(id='', status=False)
        serialized = NotificationSerializer(notificationapi)
        return JsonResponse({'data': serialized.data})
    try:
        notificationapi = Notification(id=device.id, status=True)
    except AttributeError:
        notificationapi = Notification(id='', status=False)
        serialized = NotificationSerializer(notificationapi)
        return JsonResponse({'data': serialized.data})

    serialized = NotificationSerializer(notificationapi)
    return JsonResponse({'data': serialized.data})
