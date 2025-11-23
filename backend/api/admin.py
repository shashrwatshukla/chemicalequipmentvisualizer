from django.contrib import admin
from .models import Dataset, Equipment, EmailVerification


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'code']


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_by', 'uploaded_at', 'total_equipment']
    list_filter = ['uploaded_at', 'uploaded_by']
    search_fields = ['name']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['equipment_type', 'dataset']
    search_fields = ['equipment_name']