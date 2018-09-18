# coding: UTF-8
import random
import urllib

from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password

from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient

from .models import Member


def member_login(request):
    phone = request.POST.get('phone', '')
    password = request.POST.get('password', '')
    if not phone or not password:
        return False, u"请输入用户名或密码"
    # 去掉明文判断
    member = Member.get(phone=phone)
    if not member:
        return False, u"用户名或密码错误"
    phone_status = check_password(password, member.password)
    if phone_status:
        cache.set(request.session.session_key, phone, 60 * 60 * 24)
        #request.session[request.session.session_key] = phone
        return True, u'登陆成功'

    return False, u"账号或密码错误"


def send_verify_code(request, phone):
    # todo 判断接口的请求评论 防止有人频繁调用接口短信轰炸
    number = random.randint(1000, 9999)
    client = YunpianClient(apikey='2e1da426087927fcefc313d08536584b')
    tpl_value = urllib.parse.urlencode({'#code#': str(number)})
    param = {YC.MOBILE: phone, YC.TPL_ID: 2442232, YC.TPL_VALUE: tpl_value}
    r = client.sms().tpl_single_send(param)
    if r.code() == 0:
        cache.set('%s%s' % (request.session.session_key, "SESSION_KEY_NUMBER"), number, 3600 * 24)
        cache.set(request.session.session_key, phone, 3600 * 24)
        return r.code()
    return r.code()


def phone_register_data(request):
    phone = request.POST.get('phone')
    if not phone:
        return False, u"请输入手机号码"
    if not Member.objects.filter(phone=phone):
        code = send_verify_code(request, phone)
        if code == 0:
            return True, u"短信验证码发送成功"
    return False, u"该手机号码已注册!!!"


def register_code_data(request):
    register_code = request.POST.get('register_code')
    number_code = cache.get('%s%s' % (request.session.session_key, "SESSION_KEY_NUMBER"))
    if register_code and number_code:
        if int(register_code) == int(number_code):
            return True, u""
    return False, u"验证码不正确"


def set_member_data(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    phone = cache.get(request.session.session_key)
    if not phone:
        return False, u"获取验证码后重试"
    if not name:
        return False, u"姓名为必填项"
    if not email:
        return False, u"邮箱为必填项"
    # todo 不能用明文密码比对 或 保存
    if password == confirm_password:
        Member.objects.create(name=name, mailbox=email, phone=phone, password=make_password(password, None, 'pbkdf2_sha256'))
        return True, u"注册成功"

    return False, u"密码不一致"