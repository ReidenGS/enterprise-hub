from rest_framework import serializers
from app01 import models

#数据库类

class machineInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.machine
        fields = '__all__'



class companyInfoSerializer(serializers.ModelSerializer):
    machine = machineInfoSerializer(many = True)
    gender = serializers.CharField(source='get_gender_display')
    class Meta:
        model = models.companyInfo
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'machine' in self.fields:  # 替换为你的ManyToManyField字段名
            self.fields['machine'].label_from_instance = lambda obj: f"{obj.name} ({obj.machine_id})"

class workerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.workerInfo
        exclude = ['token']

class RepairOrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    dispatch_status = serializers.CharField(source='get_dispatch_status_display')
    quotation_status = serializers.CharField(source='get_quotation_status_display')
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    emergency_level = serializers.CharField(source='get_emergency_level_display')
    class Meta:
        model = models.RepairOrder
        fields = '__all__'

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quotation
        fields = '__all__'

class RepairAdviceSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    satisfaction = serializers.CharField(source='get_satisfaction_display')
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    reply_date = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = models.RepairAdvice
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = models.Report
        fields = '__all__'
