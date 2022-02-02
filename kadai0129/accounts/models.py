from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""
    loginnum = models.IntegerField(verbose_name='ログイン回数', default=0)
    class Meta:
        verbose_name_plural = 'CustomUser'
