from django.urls import path
from app01 import views
from djangoProject import settings
from django.views.static import serve
#销售系统

    # ==================== 用户认证 ====================
    path('sells_register/', views.register, name='register'),
    path('sells_login/', views.user_login, name='login'),
    path('sells_logout/', views.user_logout, name='logout'),

    # ==================== 仪表盘 ====================
    path('sells_dashboard', views.dashboard, name='dashboard'),

    # ==================== 客户管理 ====================
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/update/', views.client_update, name='client_update'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    path('clients/<int:client_id>/equipment/add/',
         views.add_equipment, name='add_equipment'),
    path('clients/<int:client_id>/competitor/add/',
         views.add_competitor, name='add_competitor'),

    # ==================== 拜访记录 ====================
    path('visits/', views.visit_list, name='visit_list'),
    path('visits/create/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visits/<int:pk>/update/', views.visit_update, name='visit_update'),
    path('visits/<int:visit_id>/followup/add/',
         views.add_followup, name='add_followup'),

    # ==================== 年度计划 ====================
    path('plans/annual/', views.annual_plan_list, name='annual_plan_list'),
    path('plans/annual/create/', views.annual_plan_create, name='annual_plan_create'),
    path('plans/annual/<int:pk>/', views.annual_plan_detail, name='annual_plan_detail'),

    # ==================== 报表管理 ====================
    path('reports/monthly/create/',
         views.monthly_report_create, name='monthly_report_create'),
    path('reports/weekly/create/',
         views.weekly_report_create, name='weekly_report_create'),