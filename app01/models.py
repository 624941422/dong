from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """
    客户信息表
    """
    name = models.CharField(max_length=32, blank=True, null=True)
    qq = models.CharField(max_length=64, unique=True, verbose_name='QQ')
    qq_name = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True, unique=True)
    source_choices = ((0, '转介绍'),
                      (1, 'QQ群'),
                      (2, '微信群'),
                      (3, '百度推广'),
                      (4, '51CTO'),
                      (5, '知乎'),)
    source = models.SmallIntegerField(choices=source_choices, verbose_name='来源')
    referral_from = models.CharField(max_length=64, blank=True, null=True, verbose_name='转介绍人QQ')
    consult_course = models.ForeignKey('Course', verbose_name='咨询课程')
    content = models.TextField(verbose_name='咨询详情')
    consultant = models.ForeignKey('UserProfile', verbose_name='咨询顾问')
    memo = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name = '客户表'
        verbose_name_plural = '客户表'

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'


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
    intention = models.SmallIntegerField(choices=intention_choice, verbose_name='报名意向')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<%s : %s>" % (self.customer.qq, self.content)

    class Meta:
        verbose_name = '客户跟进表'
        verbose_name_plural = '客户跟进表'


class Course(models.Model):
    """
    课程表
    """
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name='周期(月)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程表'
        verbose_name_plural = '课程表'


class Branch(models.Model):
    """
    校区表
    """
    name = models.CharField(max_length=64, unique=True)
    addr = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '校区表'


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
    class_type = models.SmallIntegerField(choices=class_type_choice, verbose_name='班级类型')
    start_date = models.DateField(verbose_name='开班日期')
    end_date = models.DateField(verbose_name='结业日期', blank=True, null=True)

    def __str__(self):
        return '<%s : %s : %s>' % (self.branch, self.course, self.semester)

    class Meta:
        unique_together = ('branch', 'course', 'semester')
        verbose_name_plural = '班级表'


class CourseRecord(models.Model):
    """
    上课记录表
    """
    from_class = models.ForeignKey("ClassList", verbose_name='班级')
    day_num = models.SmallIntegerField(verbose_name='第几节(天)')
    teacher = models.ForeignKey('UserProfile')
    has_work = models.BooleanField(default=True)
    work_title = models.CharField(max_length=128, blank=True, null=True)
    work_content = models.TextField(blank=True, null=True)
    outline = models.TextField(verbose_name='本节大纲')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s : %s" % (self.from_class, self.day_num)

    class Meta:
        unique_together = ('from_class', 'day_num')
        verbose_name_plural = '上课记录表'


class StudyRecord(models.Model):
    """
    学习记录表
    """
    student = models.ForeignKey('Enrollment')
    course_record = models.ForeignKey('CourseRecord')
    attendance_choice = ((0, '已签到'),
                         (1, '迟到'),
                         (2, '请假'),
                         (0, '退学'),)
    attendace = models.SmallIntegerField(choices=attendance_choice, default=0)
    score_choice = ((100, 'A+'),
                    (90, 'A'),
                    (85, 'B+'),
                    (80, 'B'),
                    (75, 'B+'),
                    (70, 'C+'),
                    (60, 'C'),
                    (40, 'C-'),
                    (-50, 'D'),
                    (-100, 'copy'),
                    (0, 'N/A'))
    score = models.SmallIntegerField(choices=score_choice, verbose_name='分数')
    memo = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" % (self.student, self.course_record, self.score)

    class Meta:
        verbose_name = '学习记录表'
        verbose_name_plural = '学习记录表'


class Enrollment(models.Model):
    """
    报名表
    """
    student = models.ForeignKey('Customer')
    enrolled_class = models.ForeignKey('ClassList', verbose_name='报名班级')
    consultant = models.ForeignKey('UserProfile', verbose_name='咨询顾问')
    contract_agreed = models.BooleanField(default=False, verbose_name='学员已同意合同条款')
    contract_approved = models.BooleanField(default=False, verbose_name='合同已审核')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s : %s" % (self.student, self.enrolled_class)

    class Meta:
        unique_together = ('student', 'enrolled_class')
        verbose_name = '报名表'
        verbose_name_plural = '报名表'


class Payment(models.Model):
    """
    缴费记录
    """
    student = models.ForeignKey('Customer')
    course = models.ForeignKey('Course', verbose_name='所报课程')
    amount = models.PositiveSmallIntegerField(default=500, verbose_name='数额')
    consultant = models.ForeignKey('UserProfile', verbose_name='咨询顾问')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.student,)

    class Meta:
        verbose_name = '缴费记录'
        verbose_name_plural = '缴费记录'


class UserProfile(models.Model):
    """
    账号表
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    role = models.ManyToManyField('Role', blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name,)

    class Meta:
        verbose_name = '账号表'
        verbose_name_plural = '账号表'


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, unique=True)
    menu = models.ManyToManyField('Menu', blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name,)

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = '角色表'

class Menu(models.Model):
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '菜单表'
