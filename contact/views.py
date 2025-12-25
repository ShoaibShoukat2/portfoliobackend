from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import ContactMessage, CallSchedule
from .serializers import ContactMessageSerializer, CallScheduleSerializer
from .tasks import send_contact_email, send_call_schedule_email


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling contact form submissions
    
    Endpoints:
    - POST /api/contact/ - Submit a contact message
    - GET /api/contact/ - List all messages (admin only)
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'head', 'options']
    
    def create(self, request, *args, **kwargs):
        """Handle contact form submission"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the message
        contact_message = serializer.save()
        
        # Send email notification asynchronously
        try:
            send_contact_email.delay(contact_message.id)
        except Exception as e:
            # If Celery is not running, send email synchronously
            print(f"Celery error: {e}. Sending email synchronously...")
            self._send_email_sync(contact_message)
        
        return Response(
            {
                'success': True,
                'message': 'Thank you for your message! I will get back to you soon.',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    def _send_email_sync(self, contact_message):
        """Send email synchronously if Celery is not available"""
        try:
            # Email to admin
            admin_subject = f'New Contact Message from {contact_message.name}'
            admin_message = f"""
New contact form submission:

Name: {contact_message.name}
Email: {contact_message.email}
Project: {contact_message.project}

Message:
{contact_message.message}

---
Received at: {contact_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            # Confirmation email to user
            user_subject = 'Thank you for contacting me!'
            user_message = f"""
Hi {contact_message.name},

Thank you for reaching out! I have received your message and will get back to you as soon as possible.

Your message:
{contact_message.message}

Best regards,
Shoaib Shoukat
Full Stack Software Engineer
            """
            
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact_message.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending email: {e}")


class CallScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling call scheduling
    
    Endpoints:
    - POST /api/schedule-call/ - Schedule a call
    - GET /api/schedule-call/ - List all scheduled calls (admin only)
    - GET /api/schedule-call/upcoming/ - Get upcoming calls
    """
    queryset = CallSchedule.objects.all()
    serializer_class = CallScheduleSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    
    def create(self, request, *args, **kwargs):
        """Handle call scheduling"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the schedule
        call_schedule = serializer.save()
        
        # Send email notification asynchronously
        try:
            send_call_schedule_email.delay(call_schedule.id)
        except Exception as e:
            # If Celery is not running, send email synchronously
            print(f"Celery error: {e}. Sending email synchronously...")
            self._send_email_sync(call_schedule)
        
        return Response(
            {
                'success': True,
                'message': 'Call scheduled successfully! You will receive a confirmation email shortly.',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get all upcoming calls"""
        upcoming_calls = self.queryset.filter(
            status__in=['pending', 'confirmed']
        ).filter(
            preferred_date__gte=timezone.now().date()
        )
        serializer = self.get_serializer(upcoming_calls, many=True)
        return Response(serializer.data)
    
    def _send_email_sync(self, call_schedule):
        """Send email synchronously if Celery is not available"""
        try:
            # Email to admin
            admin_subject = f'New Call Scheduled - {call_schedule.name}'
            admin_message = f"""
New call scheduling request:

Name: {call_schedule.name}
Email: {call_schedule.email}
Phone: {call_schedule.phone}
Preferred Date: {call_schedule.preferred_date}
Preferred Time: {call_schedule.preferred_time} {call_schedule.timezone}
Topic: {call_schedule.topic}

Message:
{call_schedule.message}

---
Scheduled at: {call_schedule.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            # Confirmation email to user
            user_subject = 'Call Scheduled - Confirmation'
            user_message = f"""
Hi {call_schedule.name},

Your call has been scheduled successfully!

Details:
- Date: {call_schedule.preferred_date.strftime('%B %d, %Y')}
- Time: {call_schedule.preferred_time.strftime('%I:%M %p')} {call_schedule.timezone}
- Topic: {call_schedule.topic}

I will reach out to you at {call_schedule.phone} at the scheduled time.

If you need to reschedule, please reply to this email.

Best regards,
Shoaib Shoukat
Full Stack Software Engineer
            """
            
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[call_schedule.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
