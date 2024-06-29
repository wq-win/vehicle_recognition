from django.db import models


class User(models.Model):
    u_username = models.CharField(max_length=12, unique=True)
    u_password = models.CharField(max_length=255)
    # u_email = models.CharField(max_length=64)
    u_email = models.EmailField(max_length=75)
    u_icon = models.ImageField(upload_to='icons/%Y%m%d')
    # 默认未激活
    is_active = models.BooleanField(default=False)
    # 默认不删除(存在)
    is_delete = models.BooleanField(default=False)
    # 默认是普通用户
    is_super = models.BooleanField(default=False)

    class Meta:
        db_table = 'gp_user'