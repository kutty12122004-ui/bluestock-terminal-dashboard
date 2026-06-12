from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyCoreViewSet

router = DefaultRouter()
router.register(r'profiles', CompanyCoreViewSet, basename='company-profile')

urlpatterns = [
    path('', include(router.urls)),
]