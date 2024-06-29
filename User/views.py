import os
import random
import uuid
from datetime import datetime
from io import BytesIO

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from User.models import User
from User.views_constant import HTTP_OK, HTTP_USER_EXIST
from User.views_utils import get_color, generate_code, send_email_activate
from djangoGraduationProject import settings
from djangoGraduationProject.settings import MEDIA_KEY_PREFIX


def home(request):
    data = {
        "title": "首页",
    }
    return render(request, 'base_main.html', context=data)


def home_super(request):
    data = {
        "title": "管理员首页",
    }
    return render(request, 'main/super_index.html', context=data)


def mine(request):
    user_id = request.session.get('user_id')
    data = {
        "title": "个人中心",
        'is_login': False,
        'user_id': user_id,
    }

    if user_id:
        user = User.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_username
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url

    return render(request, 'main/mine.html', context=data)


def mine_super(request):
    # 分页
    page = int(request.GET.get("page", 1))

    per_page = int(request.GET.get("per_page", 5))

    users = User.objects.all()

    paginator = Paginator(users, per_page)

    page_object = paginator.page(page)

    user_id = request.session.get('user_id')

    data = {
        "title": "管理员中心",
        'is_login': False,
        'users': users,
        "page_object": page_object,
        "page_range": paginator.page_range
    }

    if user_id:
        user = User.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_username
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url

    return render(request, 'main/mine_super.html', context=data)


# 获取验证码
def get_code(request):
    # 初始化画布，初始化画笔

    mode = "RGB"
    size = (200, 100)
    red = get_color()
    green = get_color()
    blue = get_color()
    color_bg = (red, green, blue)
    image = Image.new(mode=mode, size=size, color=color_bg)
    image_draw = ImageDraw(image, mode=mode)
    image_font = ImageFont.truetype(settings.FONT_PATH, 100)
    verify_code = generate_code()
    request.session['verify_code'] = verify_code

    for i in range(4):
        fill = (get_color(), get_color(), get_color())
        image_draw.text(xy=(50 * i, 0), text=verify_code[i], font=image_font, fill=fill)
    for i in range(2000):
        fill = (get_color(), get_color(), get_color())
        xy = (random.randrange(201), random.randrange(100))
        image_draw.point(xy, fill)

    fp = BytesIO()
    image.save(fp, "png")
    return HttpResponse(fp.getvalue(), content_type="image/png")


def register(request):
    if request.method == "GET":
        data = {
            "title": "注册",
        }
        return render(request, 'user/register.html', context=data)
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # password = hash_str(password)，views.utils模块中的hash_str返回sha512加密
        password = make_password(password)
        email = request.POST.get("email")
        icon = request.FILES.get("icon")

        user = User()
        user.u_username = username
        user.u_password = password
        user.u_email = email
        user.u_icon = icon
        user.save()

        u_token = uuid.uuid4().hex

        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_email_activate(username, email, u_token)

        return redirect(reverse("user:login"))


def login(request):
    if request.method == "GET":
        error_message = request.session.get('error_message')
        data = {
            "title": "登录",
        }
        if error_message:
            del request.session['error_message']
            data['error_message'] = error_message
        return render(request, 'user/login.html', context=data)
    elif request.method == "POST":
        # 验证码校验
        receive_code = request.POST.get("verify_code")
        store_code = request.session.get("verify_code")

        if receive_code.lower() != store_code.lower():
            request.session['error_message'] = 'verify code error'
            return redirect(reverse('user:login'))

        # 内聚校验方式，检验用户名、密码是否在库中
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 账号被删除后，必须要管理员找回
        users = User.objects.filter(u_username=username).filter(is_delete=False)

        if users.exists():
            user = users.first()

            if check_password(password, user.u_password):

                if user.is_active:
                    request.session['user_id'] = int(user.id)

                    if user.is_super:
                        return redirect(reverse('user:mine_super'))

                    return redirect(reverse('user:mine'))
                else:
                    # print('用户未激活')
                    request.session['error_message'] = 'user not activate'
                    # TODO 未激活重定向activate_fail.html
                    return redirect(reverse('user:login'))
            else:
                # print("密码错误")
                request.session['error_message'] = 'password error'
                return redirect(reverse('user:login'))
        # print("用户不存在")
        request.session['error_message'] = 'user does not exist'
        return redirect(reverse('user:login'))


def logout(request):
    request.session.flush()

    return redirect(reverse('user:mine'))


# 服务器校验方式，注册时，检查用户名是否重复
def check_user(request):
    username = request.GET.get("username")

    users = User.objects.filter(u_username=username)

    data = {
        "status": HTTP_OK,
        "msg": 'user can use',
    }

    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'user already exist'
    else:
        pass

    return JsonResponse(data=data)


def activate(request):
    u_token = request.GET.get('u_token')  # 激活时，url中传递u_token用GET获取

    user_id = cache.get(u_token)

    if user_id:
        cache.delete(u_token)

        user = User.objects.get(pk=user_id)

        user.is_active = True

        user.save()
        return redirect(reverse('user:login'))

    return render(request, 'user/activate_fail.html')


# 管理员删除用户
def delete(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(pk=user_id)
    user.is_delete = True
    user.is_active = False
    user.save()
    for plate in user.plate_set.all():
        # print(plate.p_plate)
        plate.p_is_delete = True
        plate.save()
    return redirect(reverse('user:mine_super'))


# 管理员恢复用户
def addition(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(pk=user_id)
    user.is_delete = False
    user.save()
    for plate in user.plate_set.all():
        # print(plate.p_plate)
        plate.p_is_delete = False
        plate.save()
    return redirect(reverse('user:mine_super'))


def search(request):
    username = request.GET.get('username')
    if username is None:
        return redirect(reverse('user:mine_super'))

    user = User.objects.filter(u_username=username).first()
    data = {
        "title": '查找用户',
        "msg": 'search success',
    }
    # print(user)
    # print(type(user))
    if user:
        data['user_id'] = user.id
        data['username'] = user.u_username
        data['email'] = user.u_email
        data['activate'] = user.is_active
        data['delete'] = user.is_delete
    else:
        data['msg'] = 'search user is not exist'
    return render(request, 'user/search.html', context=data)


def update(request):
    if request.method == "GET":
        user_id = request.GET.get('user_id')
        data = {
            "title": "修改信息",
            "u_state": True,
        }
        if len(user_id) == 0:
            user_id = request.session.get('user_id')
            data['u_state'] = False
        request.session["update_user_id"] = user_id

        return render(request, 'user/update.html', context=data)
    elif request.method == "POST":
        user_id = request.session.get("update_user_id")

        username = request.POST.get("username")
        password = request.POST.get("password")
        password = make_password(password)
        email = request.POST.get("email")
        icon = request.FILES.get("icon")

        user = User.objects.get(pk=user_id)
        u_icon_name =user.u_icon.name
        u_icon_re = u_icon_name.split('/')[-1]
        f_name = u_icon_name[0:len(u_icon_name)-len(u_icon_re)-1]
        filePath = os.path.join(settings.MEDIA_ROOT, f_name, icon.name)
        # print(filePath)
        with open(filePath, 'wb') as fp:
            for part in icon.chunks():
                fp.write(part)
                fp.flush()
        # user = User.objects.get(pk=user_id)
        # user.u_username = username
        # user.u_password = password
        # user.u_email = email
        # user.u_icon = icon

        if username != '':
            User.objects.filter(pk=user_id).update(u_username=username)
        if password != '':
            User.objects.filter(pk=user_id).update(u_password=password)
        if email != '':
            User.objects.filter(pk=user_id).update(u_email=email)
        if icon is not None:
            user.u_icon.name = user.u_icon.name.replace(u_icon_re, icon.name)
            user.save()

    return redirect(reverse('user:mine_super'))


def activate_super(request):
    uid = request.GET.get('user_id')
    user = User.objects.get(pk=uid)
    user.is_active = True
    user.save()
    return redirect(reverse('user:mine_super'))
