from django.contrib import admin
from .models import ContactMessage, CallSchedule


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'project', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'project', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'project')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
    
    actions = [mark_as_read, mark_as_unread]


@admin.register(CallSchedule)
class CallScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'preferred_date', 'preferred_time', 'status', 'created_at']
    list_filter = ['status', 'preferred_date', 'created_at']
    search_fields = ['name', 'email', 'phone', 'topic']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'preferred_date'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Schedule Details', {
            'fields': ('preferred_date', 'preferred_time', 'timezone', 'topic')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected calls as confirmed"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected calls as completed"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = "Mark selected calls as cancelled"
    
    actions = [mark_as_confirmed, mark_as_completed, mark_as_cancelled]
