from django.db import models
from member.models import Member



class QuestionInfo(models.Model):
    member = models.ForeignKey(Member, verbose_name=u"提问用户", on_delete=models.CASCADE)
    problem_text = models.TextField(verbose_name=u"提问内容", max_length=100, null=True)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)


    @classmethod
    def get(cls, *args, **kwargs):
        try:
            obj = cls.objects.get(*args, **kwargs)
        except:
            obj = None
        return obj


class AnswerInfo(models.Model):
    question = models.ForeignKey(QuestionInfo, verbose_name=u"发布的提问", on_delete=models.CASCADE)
    member = models.ForeignKey(Member, verbose_name=u'答案用户', on_delete=models.CASCADE, null=True)
    answer_text = models.TextField(verbose_name=u"答案内容", max_length=100, null=True)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            obj = cls.objects.get(*args, **kwargs)
        except:
            obj = None
        return obj

class CommentInfo(models.Model):
    answer = models.ForeignKey(AnswerInfo, verbose_name=u"答案", on_delete=models.CASCADE)
    member = models.ForeignKey(Member, verbose_name=u'评论用户', on_delete=models.CASCADE)
    comment_text = models.TextField(verbose_name=u"评论内容", max_length=100, null=True)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            obj = cls.objects.get(*args, **kwargs)
        except:
            obj = None
        return obj


class CollectionInfo(models.Model):
    question = models.ForeignKey(QuestionInfo, verbose_name=u"发布的提问", on_delete=models.CASCADE)
    member = models.ForeignKey(Member, verbose_name=u'用户', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)


    @classmethod
    def get(cls, *args, **kwargs):
        try:
            obj = cls.objects.get(*args, **kwargs)
        except:
            obj = None
        return obj


class FollowMember(models.Model):
    member = models.IntegerField(verbose_name=u'用户ID', max_length=20, null=True, blank=True)
    follow_member = models.ForeignKey(Member, verbose_name=u"关注用户", on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)


class PrivateLetter(models.Model):
    member = models.IntegerField(verbose_name=u'用户ID', max_length=20, null=True, blank=True)
    send_letter = models.ForeignKey(Member, verbose_name=u'发送私信用户', on_delete=models.CASCADE, null=True, blank=True)
    letter_text = models.TextField(verbose_name=u"评论内容", max_length=100, null=True)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)


class QuestionIntegral(models.Model):
    question = models.ForeignKey(QuestionInfo, verbose_name=u"发布的提问", on_delete=models.CASCADE)
    coin = models.IntegerField(verbose_name=u"积分", null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)


    @classmethod
    def get(cls, *args, **kwargs):
        try:
            obj = cls.objects.get(*args, **kwargs)
        except:
            obj = None
        return obj


class DynamicMessage(models.Model):
    member = models.ForeignKey(Member, verbose_name=u"接收用户", on_delete=models.CASCADE, null=True, blank=True)
    send_member = models.IntegerField(verbose_name=u'发送用户ID', max_length=20, null=True, blank=True)
    message_text = models.CharField(verbose_name=u"动态消息", max_length=50, null=True)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)


class Browse(models.Model):
    question = models.ForeignKey(QuestionInfo, verbose_name=u"提问", on_delete=models.CASCADE)
    member = models.ForeignKey(Member, verbose_name=u"用户", on_delete=models.CASCADE)
    browse_number = models.IntegerField(verbose_name=u"浏览量", max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            obj = cls.objects.get(*args, **kwargs)
        except:
            obj = None
        return obj


class Fabulous(models.Model):
    question = models.ForeignKey(QuestionInfo, verbose_name=u"发布的提问", on_delete=models.CASCADE)
    fabulous = models.IntegerField(verbose_name=u"赞", null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True, null=True)

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            obj = cls.objects.get(*args, **kwargs)
        except:
            obj = None
        return obj