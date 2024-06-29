import datetime
import time

from User.models import User
from Vehicle.models import Road


def str_to_road_id(road_str):
    """
    把str:road_name返回对应id
    :param road_str: 道路字符串
    :return: 道路的id
    """
    roads = Road.objects.all()
    for road in roads:
        if road.r_name == road_str:
            return road.id
    else:
        return Road.objects.all().first().id  # 不选择道路默认返回第一个


def str_to_datetime(date_str):
    """
    把str:date转成datetime.datetime格式
    :param date_str: 日期字符串
    :return: datetime.datetime
    """
    date_str = date_str.replace('T', ' ')
    date_str = date_str + ':00'
    fmt = '%Y-%m-%d %H:%M:%S'
    time_tuple = time.strptime(date_str, fmt)
    year, mon, mday, hour, min, sec = time_tuple[:6]
    p_time = datetime.datetime(year, mon, mday, hour, min, sec)
    return p_time


def str_to_user_id(username_str):
    """
    把str:username_str返回对应id
    :param username_str: 用户名字符串
    :return: 用户名id
    """
    users = User.objects.all()
    for user in users:
        if user.u_username == username_str:
            return user.id
    else:
        return User.objects.all().first().id  # 不选择用户默认返回第一个