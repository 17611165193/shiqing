# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache

from member.serializers import *
from common.decorator import check_auth
from .logics import member_login, phone_register_data, register_code_data, set_member_data, send_verify_code
from .models import Member
from problem.models import QuestionInfo

def date(data):
    date_list = {}
    for item in data:
        day_date = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
        item_date = datetime.datetime.strptime(item.created_at.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
        day = day_date.day - item_date.day
        minute = round((day_date-item_date).total_seconds() / 60)
        hour = round((day_date - item_date).total_seconds() / 60 / 60)
        if day_date.day != item_date.day:
            date_list[item.id] = '%s天前' % (day)
        elif minute < 60 and minute > 0:
            date_list[item.id] = '%s分钟前' % (minute)
        elif hour < 24 and hour > 0:
            date_list[item.id] = '%s小时前' % (hour)
        else:
            date_list[item.id] = '刚刚'
    return date_list


@csrf_exempt
@check_auth
def index(request):
    question = QuestionInfo.objects.filter()
    date_list = date(question)

    return render_to_response('index.html', {'data': QuestionInfo.objects.filter(),
                                             'list': date_list})


class MemberLoginView(APIView):
    def get(self, request, format=None):

        return render(request, 'login.html')

    def post(self, request, format=None):
        serializer = MemberLoginSerializer(data=request.data)
        if serializer.is_valid():
           return render(request, 'index.html')

        #return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render_to_response('login.html', {'message': u"账号或密码不对"})

class RegisterView(APIView):
    def get(self, request):

        return render(request, 'fast_register.html')

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        status, message = member_login(request)
        if status:
            question = QuestionInfo.objects.filter()
            date_list = date(question)
            return render_to_response('index.html', {'data': QuestionInfo.objects.filter(),
                                                     'list': date_list})
        else:
            return render_to_response('login.html', {'message': message})

    return render(request, 'login.html')


@csrf_exempt
def phone_register(request):
    if request.method == 'POST':
        status, message = phone_register_data(request)
        if status:
            return render_to_response('confirm_code.html', {'message': message})
        else:
            return render_to_response('fast_register.html', {'message': message})
    return render(request, 'fast_register.html')


@csrf_exempt
def register_code(request):
   status, message = register_code_data(request)
   if status:
         return render_to_response('register.html', {'message': message})
   return render_to_response('confirm_code.html', {'message': message})


@csrf_exempt
def set_member(request):
   if request.method == 'POST':
      status, message = set_member_data(request)
      print(message)
      if status:
          return render_to_response('login.html', {'message': message})
   return render(request, 'register.html')


@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
       phone = request.POST.get('phone')
       member = Member.objects.filter(phone=phone)
       if not member:
           return render_to_response('appeal_member.html', {'message': u"账号有误"})
       else:
           return render_to_response('forget_password.html', {'member': member})
    return render(request, 'appeal_member.html')


@csrf_exempt
def verification(request):
    phone = request.GET.get('phone')
    code = send_verify_code(request, phone)
    if code == 0:
        return render(request, 'get_verify_code.html')

    return render_to_response('forget_password.html', {'message': u"验证码发送失败"})


@csrf_exempt
def pwd_verify_code(request):
    verify_code = request.POST.get('verify_code')
    number_code = cache.get('%s%s' % (request.session.session_key, "SESSION_KEY_NUMBER"))
    if verify_code and number_code:
        if int(verify_code) == int(number_code):
            return render(request, 'update_pwd.html')
    return render_to_response('get_verify_code.html', {'message': u'验证码不正确'})


@csrf_exempt
def update_pwd(request):
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    phone = cache.get(request.session.session_key)
    if password and confirm_password and phone:
        if str(password) == str(confirm_password):
            Member.objects.filter(phone=phone).update(password=make_password(password, None, 'pbkdf2_sha256'))
            return render_to_response('login.html', {'message': u'密码修改成功'})
    return render_to_response('update_pwd.html', {'message': u'密码输入不一致'})


@csrf_exempt
def login_quick(request):

    return render_to_response('login_quick.html', {'message': u""})


@csrf_exempt
def login_out(request):
    cache.delete(request.session.session_key)
    return render(request, 'login.html')