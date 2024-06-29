import os

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from User.models import User
from Vehicle.models import Plate, Road
from Vehicle.views_constant import PLATE_EXIST, PLATE_NOT_EXIST
from VehicleRecognition.surface import Surface, close_window
from Vehicle.views_utils import str_to_datetime, str_to_road_id, str_to_user_id
from djangoGraduationProject import settings
import tkinter as tk


def index(request):
    # TODO 1.分页器 2. footer判断是否是管理员 3.展示表格内容
    # 分页
    page = int(request.GET.get("page", 1))

    per_page = int(request.GET.get("per_page", 5))

    plates = Plate.objects.all()

    paginator = Paginator(plates, per_page)

    page_object = paginator.page(page)

    user_id = request.session.get('user_id')

    data = {
        "title": "车辆识别主页",
        'is_super': False,
        'plates': plates,
        "page_object": page_object,
        "page_range": paginator.page_range,
    }

    if user_id:  # type(user_id) is int
        user = User.objects.get(pk=user_id)
        data['user'] = user
    else:
        return render(request, 'base_vehicle.html')

    return render(request, 'main/vehicle_index.html', data)


def search(request):
    data = {
        "title": '查找用户',
        "msg": 'search success',
        'is_super': False,
    }
    page = int(request.GET.get("page", 1))

    per_page = int(request.GET.get("per_page", 5))

    username = request.GET.get('username')
    if len(username) == 0:
        return redirect(reverse('vehicle:index'))

    user_id = request.session.get('user_id')
    if User.objects.get(pk=user_id).is_super:
        data['is_super'] = True

    user = User.objects.filter(u_username=username).first()
    if user is None:
        data['msg'] = 'search user is not exist'
        return render(request, 'vehicle/search.html', data)
    elif user.is_delete:
        data['msg'] = 'search user is delete'
        return render(request, 'vehicle/search.html', data)

    plates = user.plate_set.all()

    paginator = Paginator(plates, per_page)

    page_object = paginator.page(page)

    data['plates'] = plates
    data['page_object'] = page_object
    data['page_range'] = paginator.page_range

    return render(request, 'vehicle/search.html', context=data)


def delete(request):
    plate_id = request.GET.get('plate_id')
    plate = Plate.objects.get(pk=plate_id)
    plate.p_is_delete = True
    plate.save()
    return redirect(reverse('vehicle:index'))


def update(request):
    if request.method == "GET":
        plate_id = request.GET.get('plate_id')
        request.session["update_plate_id"] = plate_id
        plate = Plate.objects.get(pk=plate_id)
        roads = Road.objects.all()
        data = {
            "title": "修改车牌信息",
            "plate": plate,
            "roads": roads,
        }
        return render(request, 'vehicle/update.html', context=data)
    elif request.method == "POST":
        plate_id = request.session.get("update_plate_id")

        road_str = request.POST.get("road")
        # 把str:road_name返回对应id
        p_road_id = str_to_road_id(road_str)
        date_str = request.POST.get("date")
        # 自定义函数str_to_datetime，str返回datetime.datetime
        p_time = str_to_datetime(date_str)
        against = request.POST.get("against")
        if against == 'T':
            p_against = True
        elif against == 'F':
            p_against = False
        Plate.objects.filter(pk=plate_id).update(p_roads_id=p_road_id)
        Plate.objects.filter(pk=plate_id).update(p_time=p_time)
        Plate.objects.filter(pk=plate_id).update(p_against=p_against)

    return redirect(reverse('vehicle:index'))


def add(request):
    if request.method == "GET":
        users = User.objects.all()
        roads = Road.objects.all()
        data = {
            "title": "添加车牌信息",
            "method": "GET",
            "users": users,
            "roads": roads,
        }
        return render(request, 'vehicle/add.html', context=data)
    elif request.method == "POST":
        pic = request.FILES.get('pic')

        filePath = os.path.join(settings.MEDIA_ROOT, 'vehicle', pic.name)  # TODO 图片保存路径在Vehicle下面？
        print(filePath)
        with open(filePath, 'wb') as fp:
            for part in pic.chunks():
                fp.write(part)
                fp.flush()

        p_name = request.POST.get('p_name')
        username_str = request.POST.get('username')
        # 把str:username_str返回对应id
        p_username_id = str_to_user_id(username_str)
        road_str = request.POST.get("road")
        # 把str:road_name返回对应id
        p_road_id = str_to_road_id(road_str)
        date_str = request.POST.get('date')
        # 自定义函数str_to_datetime，str返回datetime.datetime
        p_time = str_to_datetime(date_str)
        against = request.POST.get('against')
        if against == 'T':
            p_against = True
        elif against == 'F':
            p_against = False

        plate = Plate()
        plate.p_plate = p_name
        plate.p_username_id = p_username_id
        plate.p_roads_id = p_road_id
        plate.p_time = p_time
        plate.p_against = p_against
        plate.save()

        return redirect(reverse('vehicle:index'))


def add_road(request):
    if request.method == 'GET':
        data = {
            "title": '添加道路',
        }
        return render(request, 'road/add.html', context=data)
    elif request.method == 'POST':
        r_name = request.POST.get('road_name')
        restriction = request.POST.get('restriction')
        road = Road()
        road.r_name = r_name
        road.r_restriction = restriction
        road.r_is_delete = False
        road.save()
    return redirect(reverse('vehicle:index'))


def update_road(request):
    page = int(request.GET.get("page", 1))

    per_page = int(request.GET.get("per_page", 5))

    roads = Road.objects.all()

    paginator = Paginator(roads, per_page)

    page_object = paginator.page(page)

    data = {
        "title": "更新道路",
        'roads': roads,
        "page_object": page_object,
        "page_range": paginator.page_range,
    }

    return render(request, 'road/update.html', data)


def save_road(request):
    if request.method == 'GET':
        rid = request.GET.get('road_id')
        request.session["save_road_id"] = rid
        r_name = Road.objects.get(pk=rid).r_name
        data = {
            "title": "保存道路",
            "r_name": r_name,
        }
        return render(request, 'road/save.html', data)
    elif request.method == 'POST':
        rid = request.session.get('save_road_id')
        r_name = request.POST.get('road_name')
        r_restriction = request.POST.get('restriction')
        road = Road.objects.get(pk=rid)
        road.r_name = r_name
        road.r_restriction = r_restriction
        road.save()
    return redirect(reverse('vehicle:update_road'))


def delete_road(request):
    r_id = request.GET.get('road_id')
    road = Road.objects.get(pk=r_id)
    road.r_is_delete = True
    road.save()
    return redirect(reverse('vehicle:update_road'))


def predict(request):
    win = tk.Tk()
    surface = Surface(win)
    win.protocol('WM_DELETE_WINDOW', close_window)
    win.mainloop()
    return HttpResponse('h')


def check_plate(request):
    p_plate = request.GET.get('plate')
    plate = Plate.objects.filter(p_plate=p_plate).first()
    data = {
        "status": PLATE_EXIST,
        "msg": 'plate existed',
    }
    if isinstance(plate, type(None)):
        u = []
        data['status'] = PLATE_NOT_EXIST
        data['msg'] = 'plate not exist'
        users = User.objects.all()
        for user in users:
            u.append(user.u_username)
        data['username'] = u
        return JsonResponse(data)
    username = plate.p_username.u_username
    uid = plate.p_username_id
    data['username'] = username
    data['uid'] = uid
    return JsonResponse(data)