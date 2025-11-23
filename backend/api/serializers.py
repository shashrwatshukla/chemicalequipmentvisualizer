from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, Equipment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'uploaded_by', 'uploaded_at', 
            'total_equipment', 'avg_flowrate', 'avg_pressure', 
            'avg_temperature', 'equipment'
        ]


class DatasetListSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'uploaded_by', 'uploaded_at',
            'total_equipment', 'avg_flowrate', 'avg_pressure', 'avg_temperature'
        ]