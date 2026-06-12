from django.shortcuts import render
from rest_framework import viewsets
from .models import Company
from .serializers import CompanyProfileSerializer

# 1. Django REST Framework Viewset for the API layer
class CompanyCoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows active company data records, 
    including nested income statements and balance sheets, 
    to be viewed as structured JSON.
    """
    queryset = Company.objects.all().order_by('symbol')
    serializer_class = CompanyProfileSerializer

# 2. Native HTML Template Render for the Frontend Dashboard
def analytics_dashboard(request):
    """
    Renders the Single-Page Tailwind CSS and Chart.js 
    executive financial metrics visualization board.
    """
    return render(request, 'companies/dashboard.html')