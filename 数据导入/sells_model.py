from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_name = models.CharField(max_length=32, unique=True, verbose_name='用户名', help_text='用户名必须唯一',null=True)
    USER_TYPE_CHOICES = (
        ('sales', '销售人员'),
        ('admin', '总管理员'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='sales')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    email = models.EmailField(unique=True, verbose_name='联系邮箱')
    # Add related_name to resolve the clash
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_set', # Unique related_name for CustomUser's groups
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_permissions_set', # Unique related_name for CustomUser's user_permissions
        related_query_name='customuser_permission',
    )

    class Meta:
        verbose_name = '销售人员'
        verbose_name_plural = '销售人员'

    def __str__(self):
        return self.username

class Client(models.Model):
    INDUSTRY_CHOICES = (
        ('manufacturing', '制造业'),
        ('construction', '建筑业'),
        ('energy', '能源行业'),
        # 可根据需要添加更多行业
    )

    client_id = models.AutoField(primary_key=True, verbose_name='客户编号')
    name = models.CharField(max_length=100, verbose_name='客户名称')
    contact_person = models.CharField(max_length=50, verbose_name='客户联系人',null=True)
    # contact_person_2 = models.CharField(max_length=50, verbose_name='客户联系人',null=True)
    # contact_person_3 = models.CharField(max_length=50, verbose_name='客户联系人',null=True)
    phone = models.CharField(max_length=20, verbose_name='联系电话',null=True)
    email = models.EmailField(verbose_name='电子邮箱',null=True)
    address = models.TextField(verbose_name='客户地址',null=True)
    # industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, verbose_name='所属行业',null=True)
    industry = models.CharField(max_length=50,verbose_name='所属行业', null=True)
    assigned_salesperson = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients',
        verbose_name='负责销售人员'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '客户信息'
        verbose_name_plural = '客户信息'

    def __str__(self):
        return self.name


class VisitRecord(models.Model):
    PURPOSE_CHOICES = (
        ('usage', '了解客户设备使用情况'),
        ('promotion', '推广新设备产品'),
        ('project', '洽谈合作项目'),
        ('complaint', '处理客户投诉'),
    )

    METHOD_CHOICES = (
        ('onsite', '上门拜访'),
        ('phone', '电话拜访'),
        ('video', '视频会议'),
        ('other', '其他'),
    )

    INTENTION_CHOICES = (
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
        ('none', '无'),
    )

    record_id = models.AutoField(primary_key=True, verbose_name='拜访记录编号')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='visit_records',
        verbose_name='客户'
    )
    salesperson = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='visit_records',
        verbose_name='销售人员'
    )
    visit_date = models.DateField(verbose_name='拜访日期')
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES, verbose_name='拜访目的',null=True)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES, verbose_name='拜访方式',null=True)
    custom_method = models.CharField(max_length=100, blank=True, null=True, verbose_name='自定义拜访方式')
    planned_duration = models.FloatField(verbose_name='预计拜访时长(小时)',null=True)
    actual_duration = models.FloatField(verbose_name='实际拜访时长(小时)',null=True)

    # 客户需求与反馈
    has_purchase_plan = models.BooleanField(default=False, verbose_name='有采购新设备计划')
    purchase_time = models.DateField(blank=True, null=True, verbose_name='计划采购时间')
    required_equipment = models.TextField(blank=True, null=True, verbose_name='需求设备类型及规格')
    special_requirements = models.TextField(blank=True, null=True, verbose_name='特殊需求或关注点')
    feedback_on_products = models.TextField(blank=True, null=True, verbose_name='对公司现有设备产品的看法')
    competitor_satisfaction = models.TextField(blank=True, null=True, verbose_name='对手服务的满意度')
    other_comments = models.TextField(blank=True, null=True, verbose_name='其他意见或建议')

    # 销售进展
    featured_products = models.TextField(verbose_name='本次重点介绍的设备产品',null=True)
    solutions_provided = models.TextField(verbose_name='产品优势与解决方案',null=True)
    cooperation_intention = models.CharField(
        max_length=20,
        choices=INTENTION_CHOICES,
        verbose_name='合作意向程度'
    )
    next_steps = models.TextField(verbose_name='下一步行动',null=True)

    # 问题与建议
    issues_encountered = models.TextField(blank=True, null=True, verbose_name='拜访过程中遇到的问题')
    proposed_solutions = models.TextField(blank=True, null=True, verbose_name='针对问题的解决建议')
    other_message = models.TextField(blank=True, null=True, verbose_name='其他信息')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '拜访记录'
        verbose_name_plural = '拜访记录'
        ordering = ['-visit_date']

    def __str__(self):
        return f"{self.client.name} - {self.visit_date}"

class ClientContact(models.Model):
    contact_id = models.AutoField(primary_key=True, verbose_name='联系人编号')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name='客户'
    )
    name = models.CharField(max_length=100, verbose_name='联系人名称')
    phone = models.CharField(max_length=20,verbose_name="联系人电话")
    class Meta:
        verbose_name = '客户联系人'
        verbose_name_plural = '客户联系人'

class ClientEquipment(models.Model):
    CONDITION_CHOICES = (
        ('good', '良好'),
        ('fair', '一般'),
        ('poor', '存在故障'),
    )

    equipment_id = models.AutoField(primary_key=True, verbose_name='设备编号')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='equipments',
        verbose_name='客户'
    )
    model = models.CharField(max_length=100, verbose_name='设备型号')
    years_in_use = models.IntegerField(verbose_name='使用年限',null=True)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, verbose_name='运行状况')
    condition_description = models.TextField(blank=True, null=True, verbose_name='运行状况描述')
    evaluation = models.TextField(verbose_name='对现有设备的评价',null=True)

    class Meta:
        verbose_name = '客户设备信息'
        verbose_name_plural = '客户设备信息'

    def __str__(self):
        return f"{self.client.name} - {self.model}"

class ClientGeneration(models.Model):
    generation_id = models.AutoField(primary_key=True, verbose_name='产品编号')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='generations',
        verbose_name='客户'
    )
    name = models.CharField(max_length=100, verbose_name='产品名称')
    class Meta:
        verbose_name = '客户所做产品'
        verbose_name_plural = '客户所做产品'

class ClientPurchase(models.Model):
    Purchase_id = models.AutoField(primary_key=True, verbose_name='记录编号')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='purchase',
        verbose_name='客户'
    )
    name = models.CharField(max_length=100, verbose_name='设备名称')
    count = models.IntegerField(verbose_name="购买数量")
    purchase_date = models.DateField(verbose_name='购买日期',null=True)
    class Meta:
        verbose_name = '客户购买记录'
        verbose_name_plural = '客户购买记录'

class SellsQuotation(models.Model):
    quotation = models.AutoField(primary_key=True, verbose_name='报价编号')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='sells_quotations',
        verbose_name='客户'
    )
    name = models.CharField(max_length=100, verbose_name='设备名称')
    unit_price = models.IntegerField(verbose_name="单价")
    quotation_date = models.DateField(verbose_name='报价日期',null=True)

    class Meta:
        verbose_name = '报价记录'
        verbose_name_plural = '报价记录'


class Competitor(models.Model):
    competitor_id = models.AutoField(primary_key=True, verbose_name='竞争对手编号')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='competitors',
        verbose_name='客户'
    )
    name = models.CharField(max_length=100, verbose_name='竞争对手名称')
    advantages = models.TextField(verbose_name='竞争对手产品优势',null=True)
    comparison = models.TextField(verbose_name='与本公司产品对比',null=True)

    class Meta:
        verbose_name = '竞争对手信息'
        verbose_name_plural = '竞争对手信息'

    def __str__(self):
        return f"{self.client.name} - {self.name}"


class FollowUpPlan(models.Model):
    plan_id = models.AutoField(primary_key=True, verbose_name='计划编号')
    visit_record = models.ForeignKey(
        VisitRecord,
        on_delete=models.CASCADE,
        related_name='follow_up_plans',
        verbose_name='拜访记录'
    )
    responsible_person = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follow_up_plans',
        verbose_name='跟进负责人'
    )
    follow_up_date = models.DateField(verbose_name='跟进时间')
    expected_outcome = models.TextField(verbose_name='预期达成目标')

    class Meta:
        verbose_name = '跟进计划'
        verbose_name_plural = '跟进计划'

    def __str__(self):
        return f"跟进计划 {self.plan_id} - {self.visit_record.client.name}"

