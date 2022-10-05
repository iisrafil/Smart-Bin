from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, redirect, get_object_or_404
from api.models import Device, Data, AppUser
from landing.forms import DeviceAddForm, DeviceUpdateForm, UserUpdateForm
from landing.models import SiteInfo


@login_required
def home(request):
    site = SiteInfo.objects.all().first()
    user = AppUser.objects.all().count()
    bin = Device.objects.all().count()
    fullbin = Device.objects.filter(percentage__gte=90).count()
    emptybin = Device.objects.filter(percentage__lte=10).count()
    context = {
        "title": "Dashboard",
        "site": site,
        "user": user,
        "bin": bin,
        "fullbin": fullbin,
        "emptybin": emptybin,
    }

    return render(request, 'dashboard/index.html', context)


def auth_login(request):
    site = SiteInfo.objects.all().first()
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Wrong username or password! Try again.')
            return redirect('login')


    else:
        form = AuthenticationForm()

    context = {
        'site': site,
        'form': form,
    }
    return render(request, 'dashboard/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def device_list(request):
    site = SiteInfo.objects.all().first()
    device_lists = Device.objects.all()
    paginator = Paginator(device_lists, 10)

    page = request.GET.get('page', 1)

    try:
        devices = paginator.page(page)
    except PageNotAnInteger:
        devices = paginator.page(1)
    except EmptyPage:
        devices = paginator.page(paginator.num_pages)

    context = {
        'title':"Device list",
        'site': site,
        'devices': devices,
    }
    return render(request, 'dashboard/device_list.html', context)


@login_required
def add_device(request):
    site = SiteInfo.objects.all().first()
    if request.method == 'POST':
        form = DeviceAddForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('device_list')

    form = DeviceAddForm()
    context = {
        'title': "Add Device",
        'site': site,
        'form': form,
    }
    return render(request, 'dashboard/forms.html', context)



@login_required
def view_device(request, id):
    site = SiteInfo.objects.all().first()

    device = Device.objects.get(pk=id)

    context = {
        'title': device.id,
        'site': site,
        'device': device,
    }
    return render(request, 'dashboard/device.html', context)


@login_required
def update_device(request, id):
    site = SiteInfo.objects.all().first()
    device = Device.objects.get(pk=id)
    if request.method == 'POST':
        form = DeviceUpdateForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
        return redirect('device_list')

    form = DeviceUpdateForm(instance=device)
    context = {
        'title': "Update Device",
        'site': site,
        'form': form,
    }
    return render(request, 'dashboard/forms.html', context)


@login_required
def delete_device(request, id):
    device = Device.objects.get(pk=id)
    device.delete()
    return redirect('device_list')


@login_required
def user_list(request):
    site = SiteInfo.objects.all().first()
    user_lists = AppUser.objects.all()
    paginator = Paginator(user_lists, 10)

    page = request.GET.get('page', 1)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    context = {
        'title': "Users list",
        'site': site,
        'list': list,
    }
    return render(request, 'dashboard/users_list.html', context)


@login_required
def update_user(request, id):
    site = SiteInfo.objects.all().first()
    obj = AppUser.objects.get(pk=id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('user_list')

    form = UserUpdateForm(instance=obj)
    context = {
        'title': obj.id,
        'site': site,
        'form': form,
    }
    return render(request, 'dashboard/forms.html', context)
