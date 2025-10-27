from django import forms
from app01.models import (
    Client, VisitRecord, ClientEquipment, Competitor,
    FollowUpPlan, AnnualPlan,CustomUser,WeeklyReport,
    MonthlyReport,ClientContact,ClientGeneration,
    ClientPurchase,SellsQuotation
)
import datetime
from django.core.exceptions import ValidationError
import json
from django.contrib.auth.models import Group
class JSONEditorWidget(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        if isinstance(value, dict):  # 如果值是字典就转为 JSON 字符串
            value = json.dumps(value, indent=2, ensure_ascii=False)
        return super().render(name, value, attrs, renderer)

class JSONFormField(forms.CharField):
    widget = JSONEditorWidget

    def clean(self, value):
        value = super().clean(value)
        try:
            if value:  # 如果不是空值就解析为 JSON
                return json.loads(value)
            return None
        except json.JSONDecodeError as e:
            raise ValidationError(f"无效的 JSON 格式: {e}")
class BootstrapFormMixin:
    """为所有表单字段添加Bootstrap样式"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })
            if field.required:
                field.widget.attrs['required'] = 'required'

class UserRegistrationForm(BootstrapFormMixin, forms.ModelForm):
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
        min_length=8,
        help_text="密码至少8个字符"
    )
    password_confirm = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = [ 'username','user_name','phone', 'email', 'user_type','groups']
        labels = {
            'username': '用户名',
            'user_name':'真实姓名',
            'user_type': '用户类型',
            'groups':'所属团队'
        }
        # widgets = {
        #     'user_type': forms.HiddenInput()  # 默认设置为销售人员
        # }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "两次输入的密码不一致")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ClientForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class VisitRecordForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 如果是销售人员，只能选择分配给自己的客户
        if user and user.user_type == 'sales':
            self.fields['client'].queryset = Client.objects.filter(
                assigned_salesperson=user
            )

    class Meta:
        model = VisitRecord
        fields = [
            'client', 'visit_date', 'purpose', 'method', 'custom_method',
            'planned_duration', 'actual_duration', 'has_purchase_plan',
            'purchase_time', 'required_equipment', 'special_requirements',
            'feedback_on_products', 'competitor_satisfaction', 'other_comments',
            'featured_products', 'solutions_provided', 'cooperation_intention',
            'next_steps', 'issues_encountered', 'proposed_solutions','other_message'
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'purchase_time': forms.DateInput(attrs={'type': 'date'}),
            'purpose': forms.Select(choices=VisitRecord.PURPOSE_CHOICES),
            'method': forms.Select(choices=VisitRecord.METHOD_CHOICES),
            'cooperation_intention': forms.Select(choices=VisitRecord.INTENTION_CHOICES),
            'special_requirements': forms.Textarea(attrs={'rows': 3}),
            'next_steps': forms.Textarea(attrs={'rows': 3}),
            'proposed_solutions': forms.Textarea(attrs={'rows': 3}),
        }


class EquipmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ClientEquipment
        fields = [
            'model', 'years_in_use', 'condition',
            'condition_description', 'evaluation'
        ]
        widgets = {
            'condition': forms.Select(choices=ClientEquipment.CONDITION_CHOICES),
            'evaluation': forms.Textarea(attrs={'rows': 3}),
        }

class ContactForm(BootstrapFormMixin,forms.ModelForm):
    class Meta:
        model = ClientContact
        fields = ['name','phone']

class ClientGenerationForm(forms.ModelForm):
    class Meta:
        model = ClientGeneration
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入产品名称'
            })
        }
        labels = {
            'name': '产品名称'
        }

class CompetitorForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Competitor
        fields = ['name', 'advantages', 'comparison']
        widgets = {
            'advantages': forms.Textarea(attrs={'rows': 3}),
            'comparison': forms.Textarea(attrs={'rows': 3}),
        }

class ClientPurchaseForm(BootstrapFormMixin,forms.ModelForm):
    class Meta:
        model = ClientPurchase
        fields = ['name', 'count', 'purchase_date']
        widgets ={
            'purchase_date' : forms.DateInput(attrs={'type': 'date'})
        }

class SellsQuotationForm(BootstrapFormMixin,forms.ModelForm):
    class Meta:
        model = SellsQuotation
        fields = ['name', 'unit_price', 'quotation_date']
        widgets ={
            'quotation_date' : forms.DateInput(attrs={'type': 'date'})
        }

class FollowUpForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 限制负责人只能选择销售人员
        if user:
            self.fields['responsible_person'].queryset = CustomUser.objects.filter(
                user_type='sales'
            )

    class Meta:
        model = FollowUpPlan
        fields = ['responsible_person', 'follow_up_date', 'expected_outcome']
        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_outcome': forms.Textarea(attrs={'rows': 3}),
        }


class SalespersonEditForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label='用户组'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'user_name', 'phone', 'email', 'groups')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 如果需要，可以在这里添加额外的初始化代码

class AnnualPlanForm(BootstrapFormMixin, forms.ModelForm):
    personnel_targets = JSONFormField(label='人员目标',help_text='请输入JSON格式的人员目标，例如: {"销售A": {"销售额": 10222,"销售设备": 10,"开发新客户": 20},"销售B": {"销售额": 10222,"销售设备": 5,"开发新客户": 10}},每一个销售人员目标之间要打逗号', required=False)
    class Meta:
        model = AnnualPlan
        fields = [
            'year', 'total_sales_target', 'sqz_target', 'qz_target',
            'ol_target', 'ro_target', 'new_clients_target',
            'q1_sales_target', 'q2_sales_target', 'q3_sales_target', 'q4_sales_target',
            'q1_equipment_target', 'q2_equipment_target',
            'q3_equipment_target', 'q4_equipment_target',
            'q1_new_clients_target', 'q2_new_clients_target',
            'q3_new_clients_target', 'q4_new_clients_target','personnel_targets',
            'market_analysis', 'competitor_analysis', 'customer_insights',
            'product_strategy', 'pricing_strategy', 'channel_strategy',
            'promotion_strategy', 'phase1_plan', 'phase2_plan',
            'phase3_plan', 'phase4_plan', 'hr_requirements',
            'financial_requirements', 'technical_requirements',
            'market_risks', 'competition_risks', 'credit_risks',
            'technical_risks', 'monitoring_plan'
        ]

        widgets = {
            'market_analysis': forms.Textarea(attrs={'rows': 4}),
            'product_strategy': forms.Textarea(attrs={'rows': 4}),
            'phase1_plan': forms.Textarea(attrs={'rows': 3}),
            'market_risks': forms.Textarea(attrs={'rows': 3}),
        }


class MonthlyReportForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置月份的初始值为当前月份的第一天
        if not self.instance.pk and 'month' not in self.data:
            today = datetime.date.today()
            self.initial['month'] = datetime.date(today.year, today.month, 1)

    class Meta:
        model = MonthlyReport
        fields = [
            'month', 'team', 'monthly_sales', 'equipment_sold',
            'equipment_details', 'sales_analysis', 'new_clients_count',
            'new_clients_details', 'new_client_challenges',
            'existing_clients_visited', 'existing_client_feedback',
            'repeat_purchase_amount', 'repeat_purchase_details',
            'promotion_activities', 'strategy_implementation',
            'industry_trends', 'competitor_analysis', 'customer_demand_changes',
            'training_progress', 'skill_improvements', 'product_challenges',
            'market_challenges', 'customer_challenges', 'personal_challenges',
            'challenge_solutions', 'next_month_sales_target',
            'next_month_equipment_target', 'next_month_new_clients_target',
            'next_month_repeat_purchase_target', 'key_tasks', 'hr_needs',
            'financial_needs', 'technical_needs'
        ]
        widgets = {
            'month': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'equipment_details': forms.Textarea(attrs={'rows': 3}),
            'sales_analysis': forms.Textarea(attrs={'rows': 4}),
            'new_clients_details': forms.Textarea(attrs={'rows': 3}),
            'new_client_challenges': forms.Textarea(attrs={'rows': 3}),
            'existing_client_feedback': forms.Textarea(attrs={'rows': 3}),
            'repeat_purchase_details': forms.Textarea(attrs={'rows': 3}),
            'promotion_activities': forms.Textarea(attrs={'rows': 3}),
            'strategy_implementation': forms.Textarea(attrs={'rows': 3}),
            'industry_trends': forms.Textarea(attrs={'rows': 3}),
            'competitor_analysis': forms.Textarea(attrs={'rows': 3}),
            'customer_demand_changes': forms.Textarea(attrs={'rows': 3}),
            'challenge_solutions': forms.Textarea(attrs={'rows': 3}),
            'key_tasks': forms.Textarea(attrs={'rows': 3}),
            'hr_needs': forms.Textarea(attrs={'rows': 2}),
            'financial_needs': forms.Textarea(attrs={'rows': 2}),
            'technical_needs': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'month': '报表月份',
            'monthly_sales': '本月销售额(元)',
            'equipment_sold': '本月销售设备数量',
            'new_clients_count': '新开发客户数',
            'existing_clients_visited': '老客户回访数',
            'repeat_purchase_amount': '老客户复购金额(元)',
        }

    def clean_month(self):
        month = self.cleaned_data['month']
        # 确保日期是该月的第一天
        if month.day != 1:
            month = month.replace(day=1)
        return month


class WeeklyReportForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置默认周范围为当前周
        if not self.instance.pk and not self.data:
            today = datetime.date.today()
            start = today - datetime.timedelta(days=today.weekday())
            end = start + datetime.timedelta(days=6)
            self.initial['week_start'] = start
            self.initial['week_end'] = end

    class Meta:
        model = WeeklyReport
        fields = [
            'week_start', 'week_end', 'team', 'weekly_sales', 'last_week_sales',
            'weekly_target', 'equipment_sold', 'equipment_details',
            'new_clients_count', 'new_clients_details', 'existing_clients_visited',
            'next_week_sales_target', 'next_week_equipment_target',
            'next_week_new_clients_target', 'next_week_repeat_purchase_target'
        ]
        widgets = {
            'week_start': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'week_end': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'equipment_details': forms.Textarea(attrs={'rows': 3}),
            'new_clients_details': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'week_start': '周开始日期',
            'week_end': '周结束日期',
            'weekly_sales': '本周销售额(元)',
            'last_week_sales': '上周销售额(元)',
            'weekly_target': '本周目标销售额(元)',
            'equipment_sold': '本周销售设备数量',
            'new_clients_count': '新开发客户数',
            'existing_clients_visited': '老客户回访数',
        }

    def clean(self):
        cleaned_data = super().clean()
        week_start = cleaned_data.get('week_start')
        week_end = cleaned_data.get('week_end')

        if week_start and week_end:
            # 验证周范围不超过7天
            if (week_end - week_start).days > 6:
                raise forms.ValidationError("周报时间范围不能超过7天")

            # 确保开始日期是周一
            if week_start.weekday() != 0:
                raise forms.ValidationError({
                    'week_start': "周开始日期必须是星期一"
                })

            # 确保结束日期是周日
            if week_end.weekday() != 6:
                raise forms.ValidationError({
                    'week_end': "周结束日期必须是星期日"
                })

        return cleaned_data