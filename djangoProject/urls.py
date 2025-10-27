"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views
from djangoProject import settings
from django.views.static import serve




urlpatterns = [
    #前端登录页面
    path('login/', views.loginView.as_view()),
    path('register/', views.registerView.as_view()),
    path('search_company/', views.searchCompany.as_view()),
    path('register_password/',views.registerPwd.as_view()),
    #前端报修页面
    path('get_machine/', views.getMachine.as_view()),

    path('repair_image/', views.RepairImage.as_view()),
    path('upload_repairOrder/', views.RepairOrder.as_view()),
    path('download/', views.downloadFile.as_view()),
    path('showQuotation/',views.showQuotation.as_view()),
    #前端反馈页面
    path('advice_image/', views.AdviceImage.as_view()),
    path('upload_advice/',views.RepairAdvice.as_view()),
    #前端历史记录页面
    path('login_history/',views.loginHistory.as_view()),
    path('repairHistory/',views.repairHistory.as_view()),
    path('adviceHistory/',views.adviceHistory.as_view()),
    #前端工作人员维修界面
    path('workerRepair/', views.workerRepair.as_view()),
    path('workerRepairDetail/', views.workerRepairDetail.as_view()),
    path('changeRepairStatus/', views.changeRepairStatus.as_view()),
    #前端工作人员完成报告页面
    path('reportImages/', views.reportImages.as_view()),
    path('repairReport/', views.repairReport.as_view()),
    #临时图片存储
    # path('tempImage/', views.tempImage.as_view()),
    #后台管理系统
    path('',views.managerLogin.as_view()),
    #企业信息管理
    path('c_info_list/',views.companyInfoView.as_view()),
    path('c_info_add/',views.companyInfoAdd.as_view()),
    path('c_info/<int:id>/reform/',views.companyInfoReform.as_view()),
    path('c_info/<int:id>/delete/',views.companyInfoDelete.as_view()),
    path('c_info_import/',views.companyInfoImport.as_view()),
    path('c_info_machineImport/',views.companyMachineImport.as_view()),
    path('c_machine_delete/',views.MachineDelete.as_view()),
    #机器信息管理
    path('machine_info/',views.machineInfoView.as_view()),
    path('machine_info_add/',views.machineInfoAdd.as_view()),
    path('machine_info/<int:id>/delete/',views.machineInfoDelete.as_view()),
    path('machine_info_import/',views.machineInfoImport.as_view()),
    #工作人员信息管理
    path('worker_info/',views.workerInfoView.as_view()),
    path('changePassword/',views.workerChangePassword.as_view()),
    path('worker_info_add/',views.workerInfoAdd.as_view()),
    path('worker_info/<int:id>/reform/',views.workerInfoReform.as_view()),
    path('worker_info/<int:id>/delete/',views.workerInfoDelete.as_view()),
    path('worker_info_import/',views.workerInfoImport.as_view()),
    #报修订单管理
    path('repairOrder_info/',views.repairOrderInfoView.as_view()),
    path('repair_info/<int:id>/detail/',views.repairOrderInfoDetail.as_view()),
    path('repair_info/<int:id>/quotation/',views.repairOrderInfoQuotation.as_view()),
    path('repair_info/<int:id>/delete/',views.repairOrderInfoDelete.as_view()),
    path('quotation_import/',views.QuotationImport.as_view()),
    path('repair_info/<int:id>/add_worker/',views.repairOrderInfoAddworker.as_view()),
    path('repair_info/<int:id>/report/',views.repairInfoReport.as_view()),
    #完成报告管理
    path('report_confirm/<int:id>/',views.reportConfirm.as_view()),
    #反馈信息管理
    path('advice_info/',views.adviceInfoView.as_view()),
    path('advice_info/<int:id>/detail/',views.adviceInfoDetail.as_view()),
    path('advice_info/<int:id>/reply/',views.adviceInfoReply.as_view()),
    path('advice_info/<int:id>/delete/',views.adviceInfoDelete.as_view()),
    #出勤数据处理
    path('attendance_info/',views.workerTime.as_view()),
    #静态文件设置
    path('static/<path:path>',serve,{"document_root":settings.STATIC_ROOT}),
    path('media/<path:path>',serve,{"document_root":settings.MEDIA_ROOT}),

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
    #设备
    path('clients/<int:client_id>/equipment/add/',
         views.add_equipment, name='add_equipment'),
    path('equipment/update/<int:pk>/', views.update_equipment, name='update_equipment'),
    path('delete-equipment/<int:pk>/', views.delete_equipment, name='delete_equipment'),
    #额外联系方式
    path('clients/<int:client_id>/contact/add/',
         views.add_contact, name='add_contact'),
    path('contact/update/<int:pk>/', views.update_contact, name='update_contact'),
    path('delete-contact/<int:pk>/', views.delete_contact, name='delete_contact'),
    #竞争对手
    path('clients/<int:client_id>/competitor/add/',
         views.add_competitor, name='add_competitor'),
    path('competitor/update/<int:pk>/', views.update_competitor, name='update_competitor'),
    path('delete-competitor/<int:pk>/', views.delete_competitor, name='delete_competitor'),
    #所做产品
    path('clients/<int:client_id>/generation/add/',
         views.add_client_generation, name='add_generation'),
    path('generation/update/<int:pk>/', views.update_generation, name='update_generation'),
    path('delete-generation/<int:pk>/', views.delete_generation, name='delete_generation'),
    #购买记录
    path('clients/<int:client_id>/purchase/add/',
         views.add_client_purchase, name='add_purchase'),
    path('purchase/update/<int:pk>/', views.update_client_purchase, name='update_purchase'),
    path('delete-purchase/<int:pk>/', views.delete_purchase, name='delete_purchase'),
    #报价
    path('clients/<int:client_id>/quotation/add/',
         views.add_client_quotation, name='add_quotation'),
    path('quotation/update/<int:pk>/', views.update_client_quotation, name='update_quotation'),
    path('delete-quotation/<int:pk>/', views.delete_quotation, name='delete_quotation'),

    # ==================== 拜访记录 ====================
    path('visits/', views.visit_list, name='visit_list'),
    path('visits/create/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visit_record/<int:record_id>/', views.visit_record_detail, name='visit_record_detail'),
    path('visits/<int:pk>/update/', views.visit_update, name='visit_update'),
    path('visit/delete/<int:pk>/', views.visit_delete, name='visit_delete'),
    path('visits/<int:visit_id>/followup/add/',
         views.add_followup, name='add_followup'),

    # ==================== 年度计划 ====================
    path('plans/annual/', views.annual_plan_list, name='annual_plan_list'),
    path('plans/annual/create/', views.annual_plan_create, name='annual_plan_create'),
    path('plans/annual/<int:pk>/', views.annual_plan_detail, name='annual_plan_detail'),
    path('plans/annual/<int:pk>/update/', views.annual_plan_update, name='annual_plan_update'),
    path('plans/annual/<int:pk>/delete/', views.annual_plan_delete, name='annual_plan_delete'),

    # ==================== 报表管理 ====================
    #月度报表
    path('reports/monthly/create/',
         views.monthly_report_create, name='monthly_report_create'),
    path('reports/monthly/<int:pk>/edit/', views.monthly_report_edit, name='monthly_report_edit'),
    path('reports/monthly/<int:pk>/', views.monthly_report_detail, name='monthly_report_detail'),
    path('reports/monthly/<int:pk>/delete/', views.monthly_report_delete, name='monthly_report_delete'),

    #周报表
    path('reports/weekly/create/',
             views.weekly_report_create, name='weekly_report_create'),
    path('reports/weekly/<int:pk>/', views.weekly_report_detail, name='weekly_report_detail'),
    path('reports/weekly/<int:pk>/edit/', views.weekly_report_edit, name='weekly_report_edit'),
    path('reports/weekly/<int:pk>/delete/', views.weekly_report_delete, name='weekly_report_delete'),
    # ==================== 文档下载 ====================
    #拜访记录下载
    path('visit-record/<int:record_id>/download/', views.generate_visit_record_docx, name='download_visit_record'),

    #销售人员管理
    path('salespersons/', views.salesperson_list, name='salesperson_list'),
    path('salespersons/<int:pk>/', views.salesperson_detail, name='salesperson_detail'),
    path('salespersons/edit/<int:pk>/', views.edit_salesperson, name='edit_salesperson'),
    path('salespersons/reset_password/<int:pk>/', views.reset_salesperson_password, name='reset_salesperson_password'),
    path('salespersons/delete/<int:pk>/', views.delete_salesperson, name='delete_salesperson'),
    #用户组管理
    path('groups/', views.group_list, name='group_list'),
    path('groups/add/', views.group_add, name='group_add'),
    path('groups/<int:group_id>/edit/', views.group_edit, name='group_edit'),
    path('groups/<int:group_id>/delete/', views.group_delete, name='group_delete'),

    #年度计划下载
    path('plans/annual/<int:pk>/download/', views.download_annual_plan, name='download_annual_plan'),
    # # ==================== API接口 ====================
    # path('api/client/<int:client_id>/equipments/',
    #      views.get_client_equipments, name='client_equipments_api'),
    # path('api/sales-targets/',
    #      views.get_sales_targets, name='sales_targets_api'),

    #导入数据
    # path('visit/data/load',views.data_load,name = 'data_load')

]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
