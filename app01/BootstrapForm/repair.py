from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from rest_framework import serializers


#表格设计
class c_info(BootStrapModelForm):
    class Meta:
        model = models.companyInfo
        # fields = '__all__'
        exclude = ['token','machine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'machine' in self.fields:  # 替换为你的ManyToManyField字段名
            self.fields['machine'].label_from_instance = lambda obj: f"{obj.name} ({obj.machine_id})"


class c_info_reform(BootStrapModelForm):
    class Meta:
        model = models.companyInfo
        # fields = '__all__'
        exclude = ['token','machine','openid','password']

class machine_info(BootStrapModelForm):
    class Meta:
        model = models.machine
        fields = '__all__'

class worker_info(BootStrapModelForm):
    class Meta:
        model = models.workerInfo
        # fields = '__all__'
        exclude = ['token','openid']

class repair_info(BootStrapModelForm):
    # dispatch_status = serializers.CharField(source='get_dispatch_status_display')
    # quotation_status = serializers.CharField(source='quotation_status')
    class Meta:
        model = models.RepairOrder
        fields = '__all__'
        # exclude = ['token']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'company' in self.fields:  # 替换为你的ManyToManyField字段名
            self.fields['company'].label_from_instance = lambda obj: f"{obj.name} "
        if 'worker' in self.fields:  # 替换为你的ManyToManyField字段名
            self.fields['worker'].label_from_instance = lambda obj: f"{obj.name} "

class report_info(BootStrapModelForm):
    class Meta:
        model = models.Report
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'repairOrder' in self.fields:  # 替换为你的ManyToManyField字段名
            self.fields['repairOrder'].label_from_instance = lambda obj: f"{obj.order_id} "

class advice_info(BootStrapModelForm):
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = models.RepairAdvice
        # fields = '__all__'
        exclude = ['companyName','reply','reply_date']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'repair_order' in self.fields:  # 替换为你的ManyToManyField字段名
            self.fields['repair_order'].label_from_instance = lambda obj: f"{obj.order_id} "

class reply_info(BootStrapModelForm):
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = models.RepairAdvice
        # fields = '__all__'
        fields = ['reply']