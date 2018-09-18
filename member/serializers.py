import datetime

from member.models import Member

from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.validators import *


class MemberLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    pass_word = serializers.CharField(required=True)

    def validate(self, data):
        member = Member.get(phone=data['phone'])
        if not check_password(data['pass_word'], member.password):
            raise serializers.ValidationError({'user_name': '密码错误'})

        return data

    def validate_user_name(self, value):
        if not Member.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号尚未注册')

        return value


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField(max_length=11, min_length=11,
                                  validators=[UniqueValidator(queryset=Member.objects.all())])
    email = serializers.EmailField()
    pass_word = serializers.CharField(max_length=6, min_length=15)
    confirm_password = serializers.CharField(max_length=6, min_length=15)

    def validate(self, data):
        if data['pass_word'] != data['confirm_password']:
            raise serializers.ValidationError({'pass_word': '2次输入密码不一致'})

        return data
