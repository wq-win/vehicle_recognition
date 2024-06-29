from django.db import models

from User.models import User


class Road(models.Model):
    # 道路名字
    r_name = models.CharField(max_length=255, unique=True)
    # 道路限制
    r_restriction = models.CharField(max_length=511)
    # 逻辑删除 默认不删除
    r_is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'gp_road'


class Plate(models.Model):
    # 车牌号码
    p_plate = models.CharField(max_length=32)
    # 外键关联道路
    p_roads = models.ForeignKey(Road, on_delete=models.CASCADE)
    # 外键关联用户,1:M,一个车牌只属于一个用户
    p_username = models.ForeignKey(User, on_delete=models.CASCADE)
    # 记录车牌当前时间，后续用于判断是否违规
    p_time = models.DateTimeField(auto_now=True)
    # 是否违规 默认不违规
    p_against = models.BooleanField(default=False)
    # 逻辑删除 默认不删除
    p_is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'gp_plate'

