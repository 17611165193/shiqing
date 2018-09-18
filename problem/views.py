# -*- coding: utf-8 -*-
import datetime

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.cache import cache

from member.views import date
from member.models import Member
from .models import QuestionInfo, CommentInfo, CollectionInfo, FollowMember, PrivateLetter, QuestionIntegral, DynamicMessage, AnswerInfo, Browse, Fabulous
from common.decorator import check_auth

@csrf_exempt
@check_auth
def set_problem(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        phone = cache.get(request.session.session_key)
        member = Member.get(phone=phone)
        if not question_text:
            return render_to_response('set_problem.html', {'message': u"请填写提问内容"})
        if not phone:
            return render_to_response('set_problem.html', {'message': u"身份过期,请重新登陆"})
        question = QuestionInfo.objects.create(member=member, problem_text=question_text)
        Fabulous.objects.create(question=question, fabulous=0)
        QuestionIntegral.objects.create(question=question, coin=0)
        date_list = date(QuestionInfo.objects.filter())
        return render_to_response('index.html', {'data': QuestionInfo.objects.filter(member=member),
                                                 'list': date_list})
    return render(request, 'set_problem.html')


@csrf_exempt
@check_auth
def recommend_list(request):
    date = datetime.datetime.now()

    return render_to_response('recommend.html', {'data': QuestionIntegral.objects.filter(created_at__day=date.day).order_by('-coin')[:1]})


@csrf_exempt
@check_auth
def comment(request):
    id = request.POST.get('answer_id')
    time = datetime.datetime.now()
    phone = cache.get(request.session.session_key)
    comment_text = request.POST.get('comment_text')
    if not comment_text:
        render_to_response('recommend.html', {'question': QuestionInfo.objects.filter()})
    if id and comment_text:
        answer = AnswerInfo.get(id=id)
        member = Member.get(phone = phone)
        CommentInfo.objects.create(answer=answer, member=member, comment_text=comment_text)
        DynamicMessage.objects.create(member=answer.member, send_member=member.id, message_text="用户: %s(%s)评论了你的%s" % (member.name, answer.question.member.phone, answer.question.problem_text))
        integral = QuestionIntegral.get(question=answer.question, created_at__day=time.day)
        question = QuestionInfo.objects.filter(id=answer.question.id)
        date_list = date(question)
        if not integral:
            QuestionIntegral.objects.create(question=QuestionInfo.get(id=answer.question.id), coin=0)
        else:
            QuestionIntegral.objects.filter(question=answer.question.id).update(coin=(integral.coin + 1))
        return render_to_response('comment.html', {'question': question,
                                                   'answer': AnswerInfo.objects.filter(question=answer.question.id),
                                                   'list': date_list,
                                                   'message': u"评论成功"})

    return render_to_response('index.html', {'data': QuestionInfo.objects.filter(), 'message': u"评论失败"})


@csrf_exempt
@check_auth
def comment_list(request):
    id = request.GET.get('id')

    return render_to_response('comment.html', {'comment': CommentInfo.objects.filter(answer=id)})


@csrf_exempt
@check_auth
def hot_list(request):
    date = datetime.datetime.now()
    return render_to_response('recommend.html', {'data': QuestionIntegral.objects.filter(created_at__month=date.month).order_by('-coin')[:1]})


@csrf_exempt
@check_auth
def collection(request):
    question_id = request.GET.get('id', None)
    phone = cache.get(request.session.session_key)
    member = Member.get(phone=phone)
    question = QuestionInfo.get(id=question_id)
    date_list = date(QuestionInfo.objects.filter())
    if question.member == member:
        return render_to_response('index.html', {'message': u'不可收藏自己的提问', 'data': QuestionInfo.objects.filter(),
                                                 'list': date_list})
    if not CollectionInfo.objects.filter(question=question, member=member):
        CollectionInfo.objects.create(question=question, member=member)
    else:
        return render_to_response('index.html', {'message': u'不可重复添加收藏', 'data': QuestionInfo.objects.filter(),
                                                 'list': date_list})
    if not phone or not member or not question:
        return render_to_response('index.html', {'message': u'添加收藏失败', 'data': QuestionInfo.objects.filter(),
                                                 'list': date_list})
    DynamicMessage.objects.create(member=question.member, send_member=member.id, message_text="用户: %s(%s)收藏了你的%s" % (member.name, member.phone, question.problem_text))

    return render_to_response('index.html', {'message': u'收藏添加成功', 'data': QuestionInfo.objects.filter(),
                                             'list': date_list})


@csrf_exempt
@check_auth
def collection_list(request):
    phone = cache.get(request.session.session_key)
    member = Member.get(phone=phone)
    return render_to_response('collection.html', {'collection': CollectionInfo.objects.filter(member=member.id)})


@csrf_exempt
@check_auth
def follow_member(request):
    follow_id = request.GET.get('id')
    question_id = request.GET.get('question_id')
    phone = cache.get(request.session.session_key)
    date_list = date(QuestionInfo.objects.filter())
    if not phone:
        return render_to_response('index.html', {'data': QuestionInfo.objects.filter(), 'list': date_list, 'message': u"身份验证过期,请重新登陆"})
    member = Member.get(phone=phone)
    if int(follow_id) == int(member.id):
        return render_to_response('index.html', {'data': QuestionInfo.objects.filter(), 'list': date_list, 'message': u"不能关注自己"})
    member = Member.get(phone=phone)
    question = QuestionInfo.get(id=question_id)
    if FollowMember.objects.filter(member=member.id, follow_member=question.member):
        return render_to_response('index.html', {'data': QuestionInfo.objects.filter(), 'list': date_list, 'message': u"不可重复关注"})
    FollowMember.objects.create(member=member.id, follow_member=question.member)
    DynamicMessage.objects.create(member=question.member, send_member=member.id, message_text="用户: %s(%s)关注了你" % (member.name, member.phone))

    return render_to_response('index.html', {'question': QuestionInfo.objects.filter(), 'message': u"关注成功"})


@csrf_exempt
@check_auth
def my_follow(request):
    phone = cache.get(request.session.session_key)
    if not phone:
        return render_to_response('index.html', {'question': QuestionInfo.objects.filter(),
                                                 'message': u"身份验证过期,请重新登陆"})
    member = Member.get(phone=phone)
    if member:
        return render_to_response('my_follow.html', {'follow': FollowMember.objects.filter(member=member.id)})
    return render_to_response('index.html', {'question': QuestionInfo.objects.filter()})


@csrf_exempt
@check_auth
def private_letter(request):
    member_id = request.GET.get('id')
    phone = cache.get(request.session.session_key)
    member = Member.get(phone=phone)
    if int(member_id) == int(member.id):
        return  render_to_response('index.html', {'question': QuestionInfo.objects.filter(), 'message': u"不能给自己发送私信"})
    return render_to_response('private_letter.html', {'id': member_id, 'member': Member.get(id=member_id)})


@csrf_exempt
@check_auth
def set_private_letter(request):
    member_id = request.POST.get('member_id')
    letter_text = request.POST.get('letter_text')
    phone = cache.get(request.session.session_key)
    member = Member.get(phone=phone)
    letter_member = Member.get(id=member_id)
    PrivateLetter.objects.create(send_letter=member, member=letter_member.id, letter_text=letter_text)
    return render_to_response('index.html', {'question': QuestionInfo.objects.filter(), 'message': u"私信发送成功"})


@csrf_exempt
@check_auth
def message(request):
    phone = cache.get(request.session.session_key)
    member = Member.get(phone=phone)
    return render_to_response('message.html', {'letter': PrivateLetter.objects.filter(member=member.id)})


@csrf_exempt
@check_auth
def recent_browse(request):
    date = datetime.datetime.now()
    phone = cache.get(request.session.session_key)
    member = Member.get(phone=phone)
    return render_to_response('recent_browse.html', {'data': Browse.objects.filter(member=member, browse_number__gte=3, created_at__day=date.day)})


@csrf_exempt
@check_auth
def fabulous(request):
    question_id = request.GET.get('question_id')
    integral = QuestionIntegral.get(question=question_id)
    fabulous_data = Fabulous.get(question=QuestionInfo.get(id=question_id))
    if not integral:
        QuestionIntegral.objects.create(question=QuestionInfo.get(id=question_id), coin=1)
    else:
        QuestionIntegral.objects.filter(question=question_id).update(coin=(integral.coin+1))
    if not fabulous_data:
        Fabulous.objects.create(question=QuestionInfo.get(id=question_id), fabulous=1)
    else:
        Fabulous.objects.filter(question=question_id).update(fabulous=(fabulous_data.fabulous+1))
    return render_to_response('comment.html', {'question': QuestionInfo.objects.filter(id=question_id), 'answer': AnswerInfo.objects.filter(question=question_id),
                                               'fabulous': Fabulous.get(question=question_id), 'message': u"点赞成功"})


@csrf_exempt
@check_auth
def follow_list(request):
    phone = cache.get(request.session.session_key)
    member = Member.get(phone=phone)
    data = []
    follow = FollowMember.objects.filter(member=member.id)
    for item in follow:
        data.append(item.follow_member)
    question = QuestionInfo.objects.filter(member__in=data)
    date_list = date(question)
    return render_to_response('index.html', {'data': question, 'list': date_list})


@csrf_exempt
@check_auth
def set_answer(request):
    time = datetime.datetime.now()
    question_id = request.POST.get('question_id')
    phone = cache.get(request.session.session_key)
    answer_text = request.POST.get('answer_text')
    if not answer_text:
        return render_to_response('index.html', {'data': QuestionInfo.objects.filter(), 'message': u"回答内容不可为空"})
    member = Member.get(phone=phone)
    if member and answer_text:
        question = QuestionInfo.get(id=question_id)
        AnswerInfo.objects.create(question=question, member=member, answer_text=answer_text)
        DynamicMessage.objects.create(member=question.member, send_member=member.id,
                                      message_text="用户: %s(%s)收藏了你的%s" % (
                                      member.name, member.phone, question.problem_text))
        integral = QuestionIntegral.get(question=question, created_at__day=time.day)
        if not integral:
            QuestionIntegral.objects.create(question=QuestionInfo.get(id=question.id), coin=0)
        else:
            QuestionIntegral.objects.filter(question=question.id).update(coin=(integral.coin + 1))
        return render_to_response('comment.html', {'question': QuestionInfo.objects.filter(id=question_id),
                                                   'answer': AnswerInfo.objects.filter(question=question_id),
                                                   'fabulous': Fabulous.get(question=question)})
    return render_to_response('index.html', {'data': QuestionInfo.objects.filter(), 'message': u"回答失败"})


@csrf_exempt
@check_auth
def dynamic_message(request):
    phone = cache.get(request.session.session_key)
    member = Member.get(phone=phone)
    return render_to_response('dynamic_message.html', {'data': DynamicMessage.objects.filter(member=member)})


@csrf_exempt
@check_auth
def details(request):
    time = datetime.datetime.now()
    id = request.GET.get('id')
    question = QuestionInfo.get(id=id)
    phone = cache.get(request.session.session_key)
    member = Member.get(phone=phone)
    browse = Browse.get(member=member, question=question, created_at__day=time.day)
    if not browse:
        Browse.objects.create(question=question, member=member, browse_number=0)
    else:
        Browse.objects.filter(question=question.id).update(browse_number=(browse.browse_number + 1))

    return render_to_response('comment.html', {'question': QuestionInfo.objects.filter(id=id),
                                               'answer': AnswerInfo.objects.filter(question=question),
                                               'fabulous': Fabulous.get(question=question)})


@csrf_exempt
@check_auth
def search(request):
    search_text = request.POST.get('search_text')
    question = QuestionInfo.objects.filter(problem_text__icontains=str(search_text))
    date_list = date(question)
    return render_to_response('index.html', {'data': question,
                                             'list': date_list})


@csrf_exempt
@check_auth
def delete_collection(request):
    id = request.GET.get('id')
    phone = cache.get(request.session.session_key)
    member = Member.get(phone=phone)
    CollectionInfo.objects.filter(id=id).delete()
    return render_to_response('collection.html', {'collection': CollectionInfo.objects.filter(member=member.id),
                                                  'message': u"删除成功!"})
