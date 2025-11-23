from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {'Verified' if self.is_verified else 'Pending'}"


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_path = models.FileField(upload_to='uploads/')
    
    total_equipment = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class Equipment(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"