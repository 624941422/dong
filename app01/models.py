from django.db import models

class Customer(models.Model):
    """
    客户信息表
    """
    name = models.CharField(max_length=32, blank=True, null=True)
    qq = models.CharField(max_length=64, unique=True)
    qq_name = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True, unique=True)
    source_choices = ((0, '转介绍'),
                      (1, 'QQ群'),
                      (2, '微信群'),
                      (3, '百度推广'),
                      (4, '51CTO'),
                      (5, '知乎'),)
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.CharField(max_length=64, blank=True, null=True, verbose_name='转介绍人QQ')
    consult_course = models.ForeignKey('Course', verbose_name='咨询课程')
    content = models.TextField(verbose_name='咨询详情')
    consultant = models.ForeignKey('UserProfile', verbose_name='咨询顾问')
    memo = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qq

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class CustomerFollowUp(models.Model):
    """
    客户跟进表
    """
    customer = models.ForeignKey('Customer')
    content = models.TextField(verbose_name='跟踪内容')
    consultant = models.ForeignKey('UserProfile', verbose_name='咨询顾问')
    intention_choice = ((0, '一星'),
                        (1, '二星'),
                        (3, '三星'),
                        (4, '四星'),
                        (5, '五星'),)
    intention = models.SmallIntegerField(intention_choice)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<%s : %s>" % (self.customer.qq, self.content)


class Course(models.Model):
    """
    课程表
    """
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name='周期(月)')

    def __str__(self):
        return self.name

class Branch(models.Model):
    """
    校区表
    """
    name = models.CharField(max_length=64, unique=True)
    addr = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class ClassList(models.Model):
    """
    班级表
    """
    course = models.ForeignKey('Course')
    semester = models.PositiveSmallIntegerField(verbose_name='学期')
    teacher = models.ManyToManyField('UserProfile')
    branch = models.ForeignKey('Branch')
    class_type_choice = ((0, '面授(脱产)'),
                         (1, '面授(周末)'),
                         (2, '网络班'),)
    class_type = models.SmallIntegerField(class_type_choice, verbose_name='班级类型')
    start_date = models.DateField(verbose_name='开班日期')
    end_date = models.DateField(verbose_name='结业日期', blank=True, null=True)
    def __str__(self):
        return '<%s : %s : %s>' % (self.branch, self.course, self.semester)

    class Meta:
        unique_together = ('branch', 'course', 'semester')

class CourseRecord(models.Model):
    """
    上课记录表
    """
    pass

class StudyRecord(models.Model):
    """
    学习记录表
    """
    pass

class Enrollment(models.Model):
    """
    报名表
    """
    pass

class Payment(models.Model):
    """
    缴费记录
    """
    pass

class UserProfile(models.Model):
    """
    账号表
    """
    pass

class Role(models.Model):
    """
    角色表
    """
    pass

