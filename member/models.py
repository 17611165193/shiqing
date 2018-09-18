# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Member(models.Model):
    name = models.CharField(verbose_name=u'姓名', max_length=50, null=True)
    password = models.CharField(verbose_name=u'用户密码', max_length=50, null=True)
    mailbox = models.EmailField(verbose_name=u'邮箱', max_length=20, null=True)
    phone = models.IntegerField(verbose_name=u'手机号码', max_length=20, null=True)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            obj = cls.objects.get(*args, **kwargs)
        except:
            obj = None
        return obj