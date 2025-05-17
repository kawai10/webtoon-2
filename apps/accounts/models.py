from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models

from common.abstracts.abstract_model import TimeStampModel


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_date__isnull=True)


class User(AbstractBaseUser, TimeStampModel):
    class Meta:
        db_table = 'user'

    email = models.EmailField(unique=True, verbose_name='이메일')
    gender = models.CharField(blank=True, max_length=255, verbose_name='성별')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    phone = models.CharField(blank=True, max_length=255, verbose_name='전화번호')
    sns_id = models.CharField(blank=True, max_length=255, verbose_name='SNS ID')
    login_type = models.CharField(null=True, default='email', max_length=255, blank=True, verbose_name='로그인 타입')
    exit_reason = models.CharField(blank=True, max_length=255, verbose_name='탈퇴 사유')
    agree_term = models.BooleanField(default=True, verbose_name='약관 동의')
    agree_privacy = models.BooleanField(default=True, verbose_name='개인정보 처리방침 동의')
    agree_date = models.DateTimeField(auto_now_add=True, verbose_name='동의 날짜')
    promotion_receive = models.DateTimeField(default=False, verbose_name='프로모션 수신')
    is_adult = models.BooleanField(default=False, verbose_name='성인인증 여부')
    first_ip = models.GenericIPAddressField(protocol='both', blank=True, null=True, verbose_name='첫 로그인 IP')
    first_platform = models.CharField(max_length=255, blank=True, null=True, verbose_name='첫 로그인 플랫폼')

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()