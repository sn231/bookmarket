from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='联系电话')
    wechat = models.CharField(max_length=50, blank=True, null=True, verbose_name='微信号')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username 