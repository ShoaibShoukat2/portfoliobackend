from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import ContactMessage, CallSchedule


@shared_task(bind=True, max_retries=3)
def send_contact_email(self, contact_message_id):
    """
    Celery task to send email notifications for contact form submissions
    """
    try:
        contact_message = ContactMessage.objects.get(id=contact_message_id)
        
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

Reply to: {contact_message.email}
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

I typically respond within 24-48 hours. If your inquiry is urgent, please feel free to reach out via LinkedIn or other social channels.

Best regards,
Shoaib Shoukat
Full Stack Software Engineer

---
This is an automated confirmation email.
        """
        
        send_mail(
            subject=user_subject,
            message=user_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact_message.email],
            fail_silently=True,
        )
        
        return f"Email sent successfully for contact message {contact_message_id}"
        
    except ContactMessage.DoesNotExist:
        return f"Contact message {contact_message_id} not found"
    except Exception as exc:
        # Retry the task if it fails
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_call_schedule_email(self, call_schedule_id):
    """
    Celery task to send email notifications for call scheduling
    """
    try:
        call_schedule = CallSchedule.objects.get(id=call_schedule_id)
        
        # Email to admin
        admin_subject = f'New Call Scheduled - {call_schedule.name}'
        admin_message = f"""
New call scheduling request:

Name: {call_schedule.name}
Email: {call_schedule.email}
Phone: {call_schedule.phone}
Preferred Date: {call_schedule.preferred_date.strftime('%B %d, %Y')}
Preferred Time: {call_schedule.preferred_time.strftime('%I:%M %p')} {call_schedule.timezone}
Topic: {call_schedule.topic}

Message:
{call_schedule.message}

---
Scheduled at: {call_schedule.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Contact: {call_schedule.phone}
Email: {call_schedule.email}
        """
        
        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        # Confirmation email to user
        user_subject = '📞 Call Scheduled - Confirmation'
        user_message = f"""
Hi {call_schedule.name},

Your call has been scheduled successfully! 🎉

📅 Call Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: {call_schedule.preferred_date.strftime('%B %d, %Y')}
Time: {call_schedule.preferred_time.strftime('%I:%M %p')} {call_schedule.timezone}
Topic: {call_schedule.topic}
Phone: {call_schedule.phone}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I will reach out to you at the scheduled time. Please ensure you're available at {call_schedule.phone}.

📝 Your Message:
{call_schedule.message}

Need to reschedule? Simply reply to this email and let me know your new preferred time.

Looking forward to speaking with you!

Best regards,
Shoaib Shoukat
Full Stack Software Engineer
LinkedIn: https://www.linkedin.com/in/shoaib-shoukat-722999228/
GitHub: https://github.com/ShoaibShoukat2

---
This is an automated confirmation email.
        """
        
        send_mail(
            subject=user_subject,
            message=user_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[call_schedule.email],
            fail_silently=True,
        )
        
        return f"Email sent successfully for call schedule {call_schedule_id}"
        
    except CallSchedule.DoesNotExist:
        return f"Call schedule {call_schedule_id} not found"
    except Exception as exc:
        # Retry the task if it fails
        raise self.retry(exc=exc, countdown=60)


@shared_task
def send_call_reminder(call_schedule_id):
    """
    Celery task to send reminder email 24 hours before the scheduled call
    """
    try:
        call_schedule = CallSchedule.objects.get(id=call_schedule_id)
        
        if call_schedule.status not in ['pending', 'confirmed']:
            return f"Call {call_schedule_id} is {call_schedule.status}, no reminder sent"
        
        subject = '⏰ Reminder: Scheduled Call Tomorrow'
        message = f"""
Hi {call_schedule.name},

This is a friendly reminder about our scheduled call tomorrow!

📅 Call Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: {call_schedule.preferred_date.strftime('%B %d, %Y')}
Time: {call_schedule.preferred_time.strftime('%I:%M %p')} {call_schedule.timezone}
Topic: {call_schedule.topic}
Phone: {call_schedule.phone}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please ensure you're available at {call_schedule.phone} at the scheduled time.

Need to reschedule? Reply to this email as soon as possible.

See you tomorrow!

Best regards,
Shoaib Shoukat
Full Stack Software Engineer
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[call_schedule.email],
            fail_silently=True,
        )
        
        return f"Reminder sent for call schedule {call_schedule_id}"
        
    except CallSchedule.DoesNotExist:
        return f"Call schedule {call_schedule_id} not found"
    except Exception as e:
        return f"Error sending reminder: {str(e)}"
