from rest_framework import serializers
from .models import ContactMessage, CallSchedule
from datetime import datetime, date


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for contact messages"""
    
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'project', 'message', 'created_at', 'is_read']
        read_only_fields = ['id', 'created_at', 'is_read']
    
    def validate_email(self, value):
        """Validate email format"""
        if not value or '@' not in value:
            raise serializers.ValidationError("Please provide a valid email address.")
        return value.lower()
    
    def validate_name(self, value):
        """Validate name"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value.strip()
    
    def validate_message(self, value):
        """Validate message"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        return value.strip()


class CallScheduleSerializer(serializers.ModelSerializer):
    """Serializer for call scheduling"""
    is_upcoming = serializers.ReadOnlyField()
    
    class Meta:
        model = CallSchedule
        fields = [
            'id', 'name', 'email', 'phone', 'preferred_date', 
            'preferred_time', 'timezone', 'topic', 'message', 
            'status', 'created_at', 'updated_at', 'is_upcoming'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'is_upcoming']
    
    def validate_email(self, value):
        """Validate email format"""
        if not value or '@' not in value:
            raise serializers.ValidationError("Please provide a valid email address.")
        return value.lower()
    
    def validate_phone(self, value):
        """Validate phone number"""
        # Remove common separators
        cleaned = value.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        if not cleaned.replace('+', '').isdigit():
            raise serializers.ValidationError("Please provide a valid phone number.")
        if len(cleaned) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value
    
    def validate_preferred_date(self, value):
        """Validate that the date is not in the past"""
        if value < date.today():
            raise serializers.ValidationError("Cannot schedule a call in the past.")
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        preferred_date = data.get('preferred_date')
        preferred_time = data.get('preferred_time')
        
        if preferred_date and preferred_time:
            # Check if datetime is in the past
            from django.utils import timezone
            call_datetime = timezone.make_aware(
                datetime.combine(preferred_date, preferred_time)
            )
            if call_datetime < timezone.now():
                raise serializers.ValidationError(
                    "Cannot schedule a call in the past. Please choose a future date and time."
                )
        
        return data
