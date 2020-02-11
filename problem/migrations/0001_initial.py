# Generated by Django 2.1 on 2018-09-07 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(max_length=100, null=True, verbose_name='答案内容')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='member.Member', verbose_name='答案用户')),
            ],
        ),
        migrations.CreateModel(
            name='Browse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browse_number', models.IntegerField(blank=True, max_length=20, null=True, verbose_name='浏览量')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='CollectionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='CommentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=100, null=True, verbose_name='评论内容')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.AnswerInfo', verbose_name='答案')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member', verbose_name='评论用户')),
            ],
        ),
        migrations.CreateModel(
            name='DynamicMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_member', models.IntegerField(blank=True, max_length=20, null=True, verbose_name='发送用户ID')),
                ('message_text', models.CharField(max_length=50, null=True, verbose_name='动态消息')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='member.Member', verbose_name='接收用户')),
            ],
        ),
        migrations.CreateModel(
            name='FollowMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.IntegerField(blank=True, max_length=20, null=True, verbose_name='用户ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('follow_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member', verbose_name='关注用户')),
            ],
        ),
        migrations.CreateModel(
            name='PrivateLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.IntegerField(blank=True, max_length=20, null=True, verbose_name='用户ID')),
                ('letter_text', models.TextField(max_length=100, null=True, verbose_name='评论内容')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('send_letter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='member.Member', verbose_name='发送私信用户')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_text', models.TextField(max_length=100, null=True, verbose_name='提问内容')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member', verbose_name='提问用户')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionIntegral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.IntegerField(blank=True, null=True, verbose_name='积分')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.QuestionInfo', verbose_name='发布的提问')),
            ],
        ),
        migrations.AddField(
            model_name='collectioninfo',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.QuestionInfo', verbose_name='发布的提问'),
        ),
        migrations.AddField(
            model_name='browse',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.QuestionInfo', verbose_name='提问'),
        ),
        migrations.AddField(
            model_name='answerinfo',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.QuestionInfo', verbose_name='发布的提问'),
        ),
    ]