from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class workerInfo(models.Model):
    name = models.CharField(verbose_name="姓名",max_length=16)
    Tele = models.CharField(verbose_name="联系电话",max_length=16,null=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    openid = models.CharField(max_length=64, unique=False,null=True)
    token = models.CharField(verbose_name="认证码", max_length=64, null=True)

class machine(models.Model):
    name = models.CharField(verbose_name="机器型号",max_length=32)
    machine_id = models.CharField(verbose_name="机器编号",max_length=32,null=True)

class companyInfo(models.Model):
    name = models.CharField(verbose_name="企业名称",max_length=32)
    Tele = models.CharField(verbose_name="联系电话",max_length=16)
    email = models.CharField(verbose_name="联系邮箱",max_length=16,null=True)
    manager = models.CharField(verbose_name="管理者姓名",max_length=16,null=True)
    gender_choices = (
        (1,"男"),
        (2,"女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, default=1,null=True)  # default指默认值
    adress = models.CharField(verbose_name="企业地址",max_length=255,null=True)
    password = models.CharField(verbose_name="用于查询历史记录的密码", max_length=64,null=True)
    token = models.CharField(verbose_name="认证码", max_length=64,null=True)
    machine = models.ManyToManyField(verbose_name="所购机器",to="machine")
    openid = models.CharField(max_length=64, unique=True,null=True)


class RepairOrder(models.Model):
    EMERGENCY_CHOICES = [
        ('low', '一般'),
        ('medium', '紧急'),
        ('high', '加急'),
    ]
    order_id = models.CharField(verbose_name='报修单号',max_length=32,null=True,unique=True)
    customer_name = models.CharField(verbose_name='企业名称', max_length=32)
    responsible_name = models.CharField(verbose_name='负责人姓名', max_length=32, null = True)
    customer_phone = models.CharField(verbose_name='联系方式', max_length=20)
    emergency_level = models.CharField(verbose_name='紧急程度', max_length=10, choices=EMERGENCY_CHOICES)
    machine_model = models.CharField(verbose_name='机器型号', max_length=50, null=True)
    machine_id = models.CharField(verbose_name='机器编号', max_length=50, null=True)
    purchase_date = models.CharField(verbose_name='购买日期', max_length=16,null=True)
    repair_date = models.DateField(verbose_name='报修日期', null=True)
    # 图片存储（多张图片）
    repair_images = models.JSONField(
        verbose_name="上传文件",
        default=list,  # 存储图片URL列表，如 ["url1", "url2"]
        blank=True,
        null=True
    )
    description = models.TextField(verbose_name='故障描述', null=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True)
    company = models.ForeignKey(verbose_name="表单拥有者",to="companyInfo", null=True,on_delete=models.CASCADE,related_name='companies')
    worker = models.ForeignKey(verbose_name="负责工作人员",to="workerInfo",null=True,on_delete=models.SET_NULL,related_name='repairOrders')
    STATUS_CHOICES = [
        ( 0 , '待受理'),
        ( 1 , '待处理'),
        ( 2 , '处理中'),
        ( 3 , '已完成'),
    ]
    status = models.IntegerField(verbose_name="订单状态",default=0,choices=STATUS_CHOICES)
    DISPATCH_CHOICES = [
        (0, '未派遣'),
        (1, '已派遣'),
    ]
    dispatch_status = models.IntegerField(verbose_name="派遣状态",default=0,choices=DISPATCH_CHOICES)
    QUOTATION_CHOICES = [
        (0, '未报价'),
        (1, '已报价'),
        (2,'保内无需报价')
    ]
    quotation_status = models.IntegerField(verbose_name="报价状态", default=0, choices=QUOTATION_CHOICES)
    process_date = models.CharField(verbose_name="开始处理时间",max_length=16,null=True)
    finished_date = models.CharField(verbose_name="处理完成时间",max_length=16,null=True)

class Report(models.Model):
    repairOrder = models.ForeignKey(verbose_name="对应报修单",to="RepairOrder",on_delete=models.CASCADE,related_name="reports")
    report = models.TextField(verbose_name="完成报告",null=True)
    finished_images = models.JSONField(
        verbose_name="完成文件",
        default=list,  # 存储图片URL列表，如 ["url1", "url2"]
        blank=True,
        null=True
    )
    STATUS_CHOICES = [
        (0,'未确认'),
        (1,'已确认')
    ]
    confirm_status = models.IntegerField(verbose_name="确认状态", default=0, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True)

class Quotation(models.Model):
    repairOrder = models.ForeignKey(to="RepairOrder",verbose_name="对应报修单",on_delete=models.CASCADE,related_name='Quotations')
    quotation = models.JSONField(
        verbose_name="报价内容",
        default=list,
        blank=True,
        null=True
    )
    file_position = models.CharField(verbose_name="报价单存储位置",max_length=128,null=True)
    responsible_manager = models.CharField(verbose_name="报价负责人",max_length=16)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True)

class RepairAdvice(models.Model):
    # 基础信息
    companyName = models.CharField(verbose_name='企业名称',max_length=50,null=True)
    customer_name = models.CharField(verbose_name="姓名", max_length=50)
    customer_phone = models.CharField(verbose_name="联系方式", max_length=20)

    # 关联报修单（选填，允许为空）
    repair_order = models.ForeignKey(
        to='RepairOrder',  # 假设你已有报修单模型
        verbose_name="关联报修单",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='repairs'
    )


    # 满意度评分
    SATISFACTION_CHOICES = [
        (3, '满意'),
        (2, '一般'),
        (1, '不满意'),

    ]
    satisfaction = models.IntegerField(
        verbose_name="满意度",
        choices=SATISFACTION_CHOICES,
        null = True
    )
    STATUS_CHOICES =[
        (1, '待回复'),
        (2, '已回复'),
    ]
    status = models.IntegerField(
        verbose_name="回复状态",
        choices=STATUS_CHOICES,
        null=True,
        default=1
    )
    # 反馈内容
    advice = models.TextField(verbose_name="反馈说明", blank=True)

    #回复内容
    reply = models.TextField(verbose_name="反馈回复", blank=True,null=True)
    #回复日期
    reply_date = models.DateTimeField(verbose_name="回复日期",null=True)
    # 图片存储（多张图片）
    images = models.JSONField(
        verbose_name="上传图片",
        default=list,  # 存储图片URL列表，如 ["url1", "url2"]
        blank=True,
        null=True
    )

    # 元信息
    created_at = models.DateTimeField(verbose_name="提交时间", auto_now_add=True)
    created_by = models.CharField(verbose_name="表单上传者",max_length=16)

class ManagerInfo(models.Model):
    name = models.CharField(verbose_name="管理者姓名",max_length=32)
    account = models.CharField(verbose_name="管理者账号",max_length=16)
    password = models.CharField(verbose_name="管理者密码",max_length=32)
    token = models.CharField(verbose_name="认证码", max_length=64,null=True)



# 营销系统部分
from django.db import models
from django.contrib.auth.models import AbstractUser



# 对于其他数据库，使用：
# from django.db.models import JSONField


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
    phone = models.CharField(max_length=50,verbose_name='联系电话',null=True,blank=True)
    email = models.EmailField(verbose_name='电子邮箱',null=True,blank=True)
    address = models.TextField(verbose_name='客户地址',null=True,blank=True)
    # industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, verbose_name='所属行业',null=True)
    industry = models.CharField(max_length=50,verbose_name='所属行业', null=True,blank=True)
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
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES, verbose_name='拜访目的',null=True,blank=True)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES, verbose_name='拜访方式',null=True,blank=True)
    custom_method = models.CharField(max_length=100, blank=True, null=True, verbose_name='自定义拜访方式')
    planned_duration = models.FloatField(verbose_name='预计拜访时长(小时)',null=True,blank=True)
    actual_duration = models.FloatField(verbose_name='实际拜访时长(小时)',null=True,blank=True)

    # 客户需求与反馈
    has_purchase_plan = models.BooleanField(default=False, verbose_name='有采购新设备计划')
    purchase_time = models.DateField(blank=True, null=True, verbose_name='计划采购时间')
    required_equipment = models.TextField(blank=True, null=True, verbose_name='需求设备类型及规格')
    special_requirements = models.TextField(blank=True, null=True, verbose_name='特殊需求或关注点')
    feedback_on_products = models.TextField(blank=True, null=True, verbose_name='对公司现有设备产品的看法')
    competitor_satisfaction = models.TextField(blank=True, null=True, verbose_name='对手服务的满意度')
    other_comments = models.TextField(blank=True, null=True, verbose_name='其他意见或建议')

    # 销售进展
    featured_products = models.TextField(verbose_name='本次重点介绍的设备产品',null=True,blank=True)
    solutions_provided = models.TextField(verbose_name='产品优势与解决方案',null=True,blank=True)
    cooperation_intention = models.CharField(
        max_length=20,
        choices=INTENTION_CHOICES,
        verbose_name='合作意向程度'
    )
    next_steps = models.TextField(verbose_name='下一步行动',null=True)

    # 问题与建议
    issues_encountered = models.TextField(blank=True, null=True, verbose_name='拜访过程中遇到的问题')
    proposed_solutions = models.TextField(blank=True, null=True, verbose_name='针对问题的解决建议')
    other_message = models.TextField(blank=True,null=True,verbose_name='其他信息')
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
    phone = models.CharField(max_length=20,verbose_name="联系人电话",null=True,blank=True)
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
    years_in_use = models.IntegerField(verbose_name='使用年限',null=True,blank=True)
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
    count = models.IntegerField(verbose_name="购买数量",null=True,blank=True)
    purchase_date = models.DateField(verbose_name='购买日期',null=True,blank=True)
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
    advantages = models.TextField(verbose_name='竞争对手产品优势',null=True,blank=True)
    comparison = models.TextField(verbose_name='与本公司产品对比',null=True,blank=True)

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


class AnnualPlan(models.Model):
    plan_id = models.AutoField(primary_key=True, verbose_name='计划编号')
    year = models.IntegerField(verbose_name='计划年度', unique=True)

    # 总体目标
    total_sales_target = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='总计划销售额',null=True,blank=True)
    sqz_target = models.IntegerField(verbose_name='SQZ系列钻靶机售卖数量',null=True,blank=True)
    qz_target = models.IntegerField(verbose_name='QZ系列钻靶机售卖数量',null=True,blank=True)
    ol_target = models.IntegerField(verbose_name='OL连线系列钻靶机售卖数量',null=True,blank=True)
    ro_target = models.IntegerField(verbose_name='Ro机器人系列钻靶机售卖数量',null=True,blank=True)
    new_clients_target = models.IntegerField(verbose_name='新客户开发数量',null=True,blank=True)
    inner_layer_market_share = models.IntegerField(verbose_name='内层市场份额目标(%)',null=True, blank=True)
    high_end_metal_market_share = models.IntegerField(verbose_name='高端金属市场份额目标(%)',null=True, blank=True)

    # 分解目标
    q1_sales_target = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='第一季度目标金额',null=True,blank=True)
    q2_sales_target = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='第二季度目标金额',null=True,blank=True)
    q3_sales_target = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='第三季度目标金额',null=True,blank=True)
    q4_sales_target = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='第四季度目标金额',null=True,blank=True)

    q1_equipment_target = models.IntegerField(verbose_name='第一季度销售设备数量',null=True,blank=True)
    q2_equipment_target = models.IntegerField(verbose_name='第二季度销售设备数量',null=True,blank=True)
    q3_equipment_target = models.IntegerField(verbose_name='第三季度销售设备数量',null=True,blank=True)
    q4_equipment_target = models.IntegerField(verbose_name='第四季度销售设备数量',null=True,blank=True)

    q1_new_clients_target = models.IntegerField(verbose_name='第一季度新客户开发数量',null=True,blank=True)
    q2_new_clients_target = models.IntegerField(verbose_name='第二季度新客户开发数量',null=True,blank=True)
    q3_new_clients_target = models.IntegerField(verbose_name='第三季度新客户开发数量',null=True,blank=True)
    q4_new_clients_target = models.IntegerField(verbose_name='第四季度新客户开发数量',null=True,blank=True)

    # 人员目标 (使用JSON存储字典数据)
    personnel_targets = models.JSONField(verbose_name='人员目标',null=True,blank=True)

    # 其他部分
    market_analysis = models.TextField(verbose_name='市场分析',null=True,blank=True)
    competitor_analysis = models.TextField(verbose_name='竞争对手分析',null=True,blank=True)
    customer_insights = models.TextField(verbose_name='客户需求洞察',null=True,blank=True)

    product_strategy = models.TextField(verbose_name='产品策略',null=True,blank=True)
    pricing_strategy = models.TextField(verbose_name='价格策略',null=True,blank=True)
    channel_strategy = models.TextField(verbose_name='渠道策略',null=True,blank=True)
    promotion_strategy = models.TextField(verbose_name='促销策略',null=True,blank=True)

    phase1_plan = models.TextField(verbose_name='第一阶段计划',null=True,blank=True)
    phase2_plan = models.TextField(verbose_name='第二阶段计划',null=True,blank=True)
    phase3_plan = models.TextField(verbose_name='第三阶段计划',null=True,blank=True)
    phase4_plan = models.TextField(verbose_name='第四阶段计划',null=True,blank=True)

    hr_requirements = models.TextField(verbose_name='人力资源需求',null=True,blank=True)
    financial_requirements = models.TextField(verbose_name='财务资源需求',null=True,blank=True)
    technical_requirements = models.TextField(verbose_name='技术资源需求',null=True,blank=True)

    market_risks = models.TextField(verbose_name='市场风险',null=True,blank=True)
    competition_risks = models.TextField(verbose_name='竞争风险',null=True,blank=True)
    credit_risks = models.TextField(verbose_name='客户信用风险',null=True,blank=True)
    technical_risks = models.TextField(verbose_name='技术风险',null=True,blank=True)
    monitoring_plan = models.TextField(verbose_name='监督与评估方案',null=True,blank=True)

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='annual_plans',
        verbose_name='创建人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '年度计划'
        verbose_name_plural = '年度计划'

    def __str__(self):
        return f"{self.year}年度销售计划"


class MonthlyReport(models.Model):
    report_id = models.AutoField(primary_key=True, verbose_name='报表编号')
    month = models.DateField(verbose_name='报表月份')  # 存储年月，格式为YYYY-MM-01
    reporter = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='monthly_reports',
        verbose_name='填报人'
    )
    team = models.CharField(max_length=100, verbose_name='所属团队',null=True,blank=True)

    # 销售业绩完成情况
    monthly_sales = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='本月销售额',null=True,blank=True)
    equipment_sold = models.IntegerField(verbose_name='本月销售设备数量',null=True,blank=True)
    equipment_details = models.JSONField(verbose_name='不同型号设备销售数量明细',null=True,blank=True)
    sales_analysis = models.TextField(verbose_name='销售业绩分析',null=True,blank=True)

    # 客户开发与维护
    new_clients_count = models.IntegerField(verbose_name='新客户开发数量',null=True,blank=True)
    new_clients_details = models.JSONField(verbose_name='新客户名单及简要情况',null=True,blank=True)
    new_client_challenges = models.JSONField(verbose_name='新客户开发困难及解决方案',null=True,blank=True)

    existing_clients_visited = models.IntegerField(verbose_name='老客户回访数量',null=True,blank=True)
    existing_client_feedback = models.TextField(verbose_name='老客户反馈问题及解决情况',null=True,blank=True)
    repeat_purchase_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='老客户复购金额',null=True,blank=True)
    repeat_purchase_details = models.JSONField(verbose_name='复购客户名单及复购情况',null=True,blank=True)

    # 其他部分
    promotion_activities = models.TextField(verbose_name='市场推广活动参与情况',null=True,blank=True)
    strategy_implementation = models.TextField(verbose_name='销售策略实施情况',null=True,blank=True)

    industry_trends = models.TextField(verbose_name='行业动态',null=True,blank=True)
    competitor_analysis = models.TextField(verbose_name='竞争对手分析',null=True,blank=True)
    customer_demand_changes = models.TextField(verbose_name='客户需求变化',null=True,blank=True)

    training_progress = models.TextField(verbose_name='培训与学习情况',null=True,blank=True)
    skill_improvements = models.TextField(verbose_name='工作技能提升表现',null=True,blank=True)

    product_challenges = models.TextField(verbose_name='产品方面问题',null=True,blank=True)
    market_challenges = models.TextField(verbose_name='市场方面问题',null=True,blank=True)
    customer_challenges = models.TextField(verbose_name='客户方面问题',null=True,blank=True)
    personal_challenges = models.TextField(verbose_name='个人方面问题',null=True,blank=True)
    challenge_solutions = models.TextField(verbose_name='解决措施及效果评估',null=True,blank=True)

    # 下月计划
    next_month_sales_target = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='下月销售额目标',null=True,blank=True)
    next_month_equipment_target = models.IntegerField(verbose_name='下月销售设备数量目标',null=True,blank=True)
    next_month_new_clients_target = models.IntegerField(verbose_name='下月新客户开发数量目标',null=True,blank=True)
    next_month_repeat_purchase_target = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='下月老客户复购金额目标',null=True,blank=True)
    key_tasks = models.TextField(verbose_name='重点工作安排',null=True,blank=True)
    hr_needs = models.TextField(verbose_name='人力资源需求',null=True,blank=True)
    financial_needs = models.TextField(verbose_name='财务资源需求',null=True,blank=True)
    technical_needs = models.TextField(verbose_name='技术资源需求',null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '月度报表'
        verbose_name_plural = '月度报表'
        unique_together = ('reporter', 'month')

    def __str__(self):
        return f"{self.reporter.username} - {self.month.strftime('%Y-%m')}月报"


class WeeklyReport(models.Model):
    report_id = models.AutoField(primary_key=True, verbose_name='周报表编号')
    week_start = models.DateField(verbose_name='周开始日期')
    week_end = models.DateField(verbose_name='周结束日期')
    reporter = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='weekly_reports',
        verbose_name='填报人'
    )
    team = models.CharField(max_length=100, verbose_name='所属团队',null=True,blank=True)

    # 销售业绩汇总
    weekly_sales = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='本周销售额',null=True,blank=True)
    last_week_sales = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='上周销售额',null=True,blank=True)
    weekly_target = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='本周目标销售额',null=True,blank=True)
    equipment_sold = models.IntegerField(verbose_name='本周销售设备数量',null=True,blank=True)
    equipment_details = models.JSONField(verbose_name='设备销售详情',null=True,blank=True)

    # 客户工作进展
    new_clients_count = models.IntegerField(verbose_name='新开发客户数量',null=True,blank=True)
    new_clients_details = models.JSONField(verbose_name='新客户详情',null=True,blank=True)
    existing_clients_visited = models.IntegerField(verbose_name='回访老客户数量',null=True,blank=True)

    # 下周计划
    next_week_sales_target = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='下周销售额目标',null=True,blank=True)
    next_week_equipment_target = models.IntegerField(verbose_name='下周销售设备数量目标',null=True,blank=True)
    next_week_new_clients_target = models.IntegerField(verbose_name='下周新客户开发数量目标',null=True,blank=True)
    next_week_repeat_purchase_target = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='下周老客户复购金额目标',null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '周报表'
        verbose_name_plural = '周报表'

    def __str__(self):
        return f"{self.reporter.username} - {self.week_start}周报"

