from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from datetime import datetime,timedelta
from .models import (
    CustomUser, Client, VisitRecord, ClientEquipment, Competitor,
    FollowUpPlan, AnnualPlan, MonthlyReport, WeeklyReport,
)
from app01.serializers.sells import (
    ClientForm, VisitRecordForm, EquipmentForm,
    CompetitorForm, FollowUpForm, AnnualPlanForm,
    MonthlyReportForm, WeeklyReportForm,UserRegistrationForm
)
from django.contrib.auth import get_user_model
# ==================用户注册模块 ====================
def register(request):
    # 如果用户已登录，重定向到首页
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        # 强制设置用户类型为销售人员
        mutable_data = request.POST.copy()
        # mutable_data['user_type'] = 'sales'
        if mutable_data['user_type'] == 'admin':
            if mutable_data['admin_code'] != settings.SELLS_ADMIN_PASSWORD:
                messages.error(request, '管理员注册专用码错误！')
                # return redirect('register')
        form = UserRegistrationForm(mutable_data)

        if form.is_valid():
            user = form.save()
            messages.success(request, '注册成功！请登录')
            return redirect('login')
    else:
        form = UserRegistrationForm(initial={'user_type': 'sales'})

    return render(request, 'sells/auth/register.html', {'form': form})

# ==================== 用户认证模块 ====================
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                print("密码正确但authenticate失败，可能是认证后端问题")
            else:
                print("密码错误")
        except User.DoesNotExist:
            print("用户不存在")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, '用户名或密码错误')

    return render(request, 'sells/auth/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# ==================== 仪表盘 ====================
@login_required
def dashboard(request):
    # 基础统计
    User = request.user
    if User.user_type == 'admin':
        stats = {
            'clients_count': Client.objects.count(),
            'visits_count': VisitRecord.objects.count(),
            'plans_count': AnnualPlan.objects.count(),
        }
    else:
        stats = {
            'clients_count': Client.objects.filter(assigned_salesperson=User).count(),
            'visits_count': VisitRecord.objects.filter(salesperson=User).count(),
            'plans_count': AnnualPlan.objects.count(),
        }

    # 最近动态
    if User.user_type == 'admin':
        recent_visits = VisitRecord.objects.order_by('-visit_date')[:5]
        upcoming_followups = FollowUpPlan.objects.filter(
            follow_up_date__gte=datetime.now().date()
        ).order_by('follow_up_date')[:5]
    else:
        recent_visits = VisitRecord.objects.filter(salesperson=User).order_by('-visit_date')[:5]
        upcoming_followups = FollowUpPlan.objects.filter(
            follow_up_date__gte=datetime.now().date(),responsible_person= User
        ).order_by('follow_up_date')[:5]

    # 销售数据概览
    if User.user_type == 'admin':
        monthly_reports = MonthlyReport.objects.order_by('-month')[:3]
    else:
        monthly_reports = MonthlyReport.objects.filter(
            reporter=User
        ).order_by('-month')[:3]

    return render(request, 'sells/dashboard.html', {
        'stats': stats,
        'recent_visits': recent_visits,
        'upcoming_followups': upcoming_followups,
        'monthly_reports': monthly_reports,
    })


# ==================== 客户管理 ====================
@login_required
def client_list(request):
    query = request.GET.get('q', '')
    clients = Client.objects.all()

    if query:
        clients = clients.filter(
            Q(name__icontains=query) |
            Q(contact_person__icontains=query) |
            Q(phone__icontains=query)
        )

    if request.user.user_type == 'sales':
        clients = clients.filter(assigned_salesperson=request.user)

    return render(request, 'sells/clients/list.html', {
        'clients': clients,
        'search_query': query,
    })


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)

    # 权限检查
    if request.user.user_type == 'sales' and client.assigned_salesperson != request.user:
        raise Http404("无权查看此客户")

    visits = VisitRecord.objects.filter(client=client).order_by('-visit_date')
    equipments = ClientEquipment.objects.filter(client=client)
    competitors = Competitor.objects.filter(client=client)

    return render(request, 'sells/clients/detail.html', {
        'client': client,
        'visits': visits,
        'equipments': equipments,
        'competitors': competitors,
    })


@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, f'客户 {client.name} 创建成功')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm()

    return render(request, 'sells/form.html', {
        'form': form,
        'title': '创建新客户',
        'submit_text': '创建客户',
    })


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    # 权限检查
    if request.user.user_type != 'admin':
        raise Http404("无权修改客户信息")

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f'客户 {client.name} 更新成功')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)

    return render(request, 'sells/form.html', {
        'form': form,
        'title': f'编辑客户 - {client.name}',
        'submit_text': '更新信息',
    })


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    # 权限检查
    if request.user.user_type != 'admin':
        raise Http404("无权删除客户")

    if request.method == 'POST':
        client_name = client.name
        client.delete()
        messages.success(request, f'客户 {client_name} 已删除')
        return redirect('client_list')

    return render(request, 'sells/confirm_delete.html', {
        'object': client,
        'title': '确认删除客户',
        'cancel_url': 'client_detail',
    })


# ==================== 拜访记录 ====================
@login_required
def visit_list(request):
    visits = VisitRecord.objects.all().order_by('-visit_date')

    if request.user.user_type == 'sales':
        visits = visits.filter(salesperson=request.user)

    return render(request, 'sells/visits/list.html', {
        'visits': visits,
    })


@login_required
def visit_detail(request, pk):
    visit = get_object_or_404(VisitRecord, pk=pk)

    # 权限检查
    if request.user.user_type == 'sales' and visit.salesperson != request.user:
        raise Http404("无权查看此拜访记录")

    followups = FollowUpPlan.objects.filter(visit_record=visit)

    return render(request, 'sells/visits/detail.html', {
        'visit': visit,
        'followups': followups,
    })


@login_required
def visit_create(request):
    if request.method == 'POST':
        form = VisitRecordForm(request.POST, user=request.user)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.salesperson = request.user
            visit.save()
            messages.success(request, '拜访记录创建成功')
            return redirect('visit_detail', pk=visit.pk)
    else:
        initial = {}
        if 'client_id' in request.GET:
            initial['client'] = request.GET['client_id']
        form = VisitRecordForm(user=request.user, initial=initial)

    return render(request, 'sells/form.html', {
        'form': form,
        'title': '新建拜访记录',
        'submit_text': '保存记录',
    })


@login_required
def visit_update(request, pk):
    visit = get_object_or_404(VisitRecord, pk=pk)

    # 权限检查
    if request.user.user_type == 'sales' and visit.salesperson != request.user:
        raise Http404("无权修改此拜访记录")

    if request.method == 'POST':
        form = VisitRecordForm(request.POST, instance=visit, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '拜访记录更新成功')
            return redirect('visit_detail', pk=visit.pk)
    else:
        form = VisitRecordForm(instance=visit, user=request.user)

    return render(request, 'sells/form.html', {
        'form': form,
        'title': '编辑拜访记录',
        'submit_text': '更新记录',
    })


# ==================== 年度计划 ====================
@login_required
def annual_plan_list(request):
    plans = AnnualPlan.objects.all().order_by('-year')
    return render(request, 'sells/plans/annual_list.html', {
        'plans': plans,
    })


@login_required
def annual_plan_detail(request, pk):
    plan = get_object_or_404(AnnualPlan, pk=pk)
    return render(request, 'sells/plans/annual_detail.html', {
        'plan': plan,
    })


@login_required
def annual_plan_create(request):
    if request.user.user_type != 'admin':
        raise Http404("无权创建年度计划")

    if request.method == 'POST':
        form = AnnualPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.created_by = request.user
            plan.save()
            messages.success(request, f'{plan.year}年度计划创建成功')
            return redirect('annual_plan_detail', pk=plan.pk)
    else:
        form = AnnualPlanForm(initial={'year': datetime.now().year})

    return render(request, 'sells/form.html', {
        'form': form,
        'title': '创建年度销售计划',
        'submit_text': '创建计划',
    })


# ==================== 报表管理 ====================
@login_required
def monthly_report_create(request):
    if request.method == 'POST':
        form = MonthlyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            messages.success(request, f'{report.month.strftime("%Y年%m月")}月报提交成功')
            return redirect('dashboard')
    else:
        form = MonthlyReportForm(initial={
            'month': datetime.now().date().replace(day=1),
            'team': request.user.groups.first().name if request.user.groups.exists() else ''
        })

    return render(request, 'sells/reports/monthly/monthly_form.html', {
        'form': form,
        'title': '创建月度报表',
    })


@login_required
def weekly_report_create(request):
    if request.method == 'POST':
        form = WeeklyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            messages.success(request, '周报提交成功')
            return redirect('dashboard')
    else:
        today = datetime.now().date()
        start = today - datetime.timedelta(days=today.weekday())
        end = start + datetime.timedelta(days=6)

        form = WeeklyReportForm(initial={
            'week_start': start,
            'week_end': end,
            'team': request.user.groups.first().name if request.user.groups.exists() else ''
        })

    return render(request, 'sells/reports/weekly/weekly_form.html', {
        'form': form,
        'title': '创建周报',
    })


# ==================== 其他功能 ====================
@login_required
def add_equipment(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.client = client
            equipment.save()
            messages.success(request, '设备信息添加成功')
            return redirect('client_detail', pk=client.pk)
    else:
        form = EquipmentForm()

    return render(request, 'sells/form.html', {
        'form': form,
        'title': f'为 {client.name} 添加设备',
        'submit_text': '添加设备',
    })


@login_required
def add_competitor(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = CompetitorForm(request.POST)
        if form.is_valid():
            competitor = form.save(commit=False)
            competitor.client = client
            competitor.save()
            messages.success(request, '竞争对手信息添加成功')
            return redirect('client_detail', pk=client.pk)
    else:
        form = CompetitorForm()

    return render(request, 'sells/form.html', {
        'form': form,
        'title': f'为 {client.name} 添加竞争对手',
        'submit_text': '添加信息',
    })


@login_required
def add_followup(request, visit_id):
    visit = get_object_or_404(VisitRecord, pk=visit_id)

    if request.method == 'POST':
        form = FollowUpForm(request.POST)
        if form.is_valid():
            followup = form.save(commit=False)
            followup.visit_record = visit
            followup.save()
            messages.success(request, '跟进计划添加成功')
            return redirect('visit_detail', pk=visit.pk)
    else:
        form = FollowUpForm(initial={
            'responsible_person': request.user,
            'follow_up_date': datetime.now().date() + timedelta(days=7)
        })

    return render(request, 'sells/form.html', {
        'form': form,
        'title': f'为 {visit.client.name} 拜访添加跟进',
        'submit_text': '添加跟进',
    })