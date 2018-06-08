# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('addr', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('semester', models.PositiveSmallIntegerField(verbose_name='学期')),
                ('class_type', models.SmallIntegerField(verbose_name=((0, '面授(脱产)'), (1, '面授(周末)'), (2, '网络班')))),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('end_date', models.DateField(verbose_name='结业日期', blank=True, null=True)),
                ('branch', models.ForeignKey(to='app01.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('price', models.PositiveSmallIntegerField()),
                ('period', models.PositiveSmallIntegerField(verbose_name='周期(月)')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('day_num', models.SmallIntegerField(verbose_name='第几节(天)')),
                ('has_work', models.BooleanField(default=True)),
                ('work_title', models.CharField(max_length=128, blank=True, null=True)),
                ('work_content', models.TextField(blank=True, null=True)),
                ('outline', models.TextField(verbose_name='本节大纲')),
                ('date', models.DateField(auto_now_add=True)),
                ('from_class', models.ForeignKey(verbose_name='班级', to='app01.ClassList')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, blank=True, null=True)),
                ('qq', models.CharField(max_length=64, unique=True)),
                ('qq_name', models.CharField(max_length=64, blank=True, null=True)),
                ('phone', models.CharField(max_length=64, unique=True, blank=True, null=True)),
                ('source', models.SmallIntegerField(choices=[(0, '转介绍'), (1, 'QQ群'), (2, '微信群'), (3, '百度推广'), (4, '51CTO'), (5, '知乎')])),
                ('referral_from', models.CharField(verbose_name='转介绍人QQ', max_length=64, blank=True, null=True)),
                ('content', models.TextField(verbose_name='咨询详情')),
                ('memo', models.TextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('consult_course', models.ForeignKey(verbose_name='咨询课程', to='app01.Course')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerFollowUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField(verbose_name='跟踪内容')),
                ('intention', models.SmallIntegerField(verbose_name=((0, '一星'), (1, '二星'), (3, '三星'), (4, '四星'), (5, '五星')))),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('contract_agreed', models.BooleanField(verbose_name='学员已同意合同条款', default=False)),
                ('contract_approved', models.BooleanField(verbose_name='合同已审核', default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('amount', models.PositiveSmallIntegerField(verbose_name='数额', default=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('attendace', models.SmallIntegerField(default=0, choices=[(0, '已签到'), (1, '迟到'), (2, '请假'), (0, '退学')])),
                ('score', models.SmallIntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (75, 'B+'), (70, 'C+'), (60, 'C'), (40, 'C-'), (-50, 'D'), (-100, 'copy'), (0, 'N/A')])),
                ('memo', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course_record', models.ForeignKey(to='app01.CourseRecord')),
                ('student', models.ForeignKey(to='app01.Enrollment')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('role', models.ManyToManyField(blank=True, null=True, to='app01.Role')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='consultant',
            field=models.ForeignKey(verbose_name='咨询顾问', to='app01.UserProfile'),
        ),
        migrations.AddField(
            model_name='payment',
            name='course',
            field=models.ForeignKey(verbose_name='所报课程', to='app01.Course'),
        ),
        migrations.AddField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(to='app01.Customer'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='consultant',
            field=models.ForeignKey(verbose_name='咨询顾问', to='app01.UserProfile'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='enrolled_class',
            field=models.ForeignKey(verbose_name='报名班级', to='app01.ClassList'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(to='app01.Customer'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='consultant',
            field=models.ForeignKey(verbose_name='咨询顾问', to='app01.UserProfile'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='customer',
            field=models.ForeignKey(to='app01.Customer'),
        ),
        migrations.AddField(
            model_name='customer',
            name='consultant',
            field=models.ForeignKey(verbose_name='咨询顾问', to='app01.UserProfile'),
        ),
        migrations.AddField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='app01.Tag'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(to='app01.UserProfile'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ForeignKey(to='app01.Course'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teacher',
            field=models.ManyToManyField(to='app01.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('student', 'enrolled_class')]),
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together=set([('from_class', 'day_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together=set([('branch', 'course', 'semester')]),
        ),
    ]
