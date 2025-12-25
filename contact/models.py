from django.db import models
from django.utils import timezone


class ContactMessage(models.Model):
    """Model for storing contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    project = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.email} ({self.created_at.strftime('%Y-%m-%d')})"


class CallSchedule(models.Model):
    """Model for scheduling calls"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    timezone = models.CharField(max_length=50, default='UTC')
    topic = models.CharField(max_length=300)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['preferred_date', 'preferred_time']
        verbose_name = 'Call Schedule'
        verbose_name_plural = 'Call Schedules'
    
    def __str__(self):
        return f"{self.name} - {self.preferred_date} {self.preferred_time} ({self.status})"
    
    @property
    def is_upcoming(self):
        """Check if the call is in the future"""
        from datetime import datetime, time
        now = timezone.now()
        call_datetime = timezone.make_aware(
            datetime.combine(self.preferred_date, self.preferred_time)
        )
        return call_datetime > now and self.status != 'cancelled'
