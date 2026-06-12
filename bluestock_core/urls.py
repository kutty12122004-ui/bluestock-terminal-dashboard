from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from companies.views import CompanyCoreViewSet

# Register API routes safely using DefaultRouter
router = DefaultRouter()
router.register(r'profiles', CompanyCoreViewSet, basename='company-profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core Data APIs
    path('api/', include(router.urls)),
    
    # User-Facing Views and Layouts
    path('', include('dashboard.urls')),
]