# coding: UTF-8
from django.core.cache import cache

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect


def check_auth(func):
    def new_func(request, *args, **argw):
        if not cache.get(request.session.session_key):

            return render_to_response('login.html', {'message': u"请重新登陆!"})

        return func(request, *args, **argw)

    return new_func