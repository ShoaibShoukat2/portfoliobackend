from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, CallScheduleViewSet

router = DefaultRouter()
router.register(r'contact', ContactMessageViewSet, basename='contact')
router.register(r'schedule-call', CallScheduleViewSet, basename='schedule-call')

urlpatterns = [
    path('', include(router.urls)),
]
