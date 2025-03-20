from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', '普通用户'),
        ('admin', '管理员'),
    ]
    
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='联系电话')
    wechat = models.CharField(max_length=50, blank=True, null=True, verbose_name='微信号')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='用户角色')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == 'admin' 