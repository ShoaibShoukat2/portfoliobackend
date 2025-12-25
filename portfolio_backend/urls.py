"""
URL configuration for portfolio_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        'message': 'Portfolio Backend API',
        'version': '1.0.0',
        'endpoints': {
            'contact': '/api/contact/',
            'schedule_call': '/api/schedule-call/',
            'admin': '/admin/',
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('contact.urls')),
    path('', api_root, name='api-root'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
