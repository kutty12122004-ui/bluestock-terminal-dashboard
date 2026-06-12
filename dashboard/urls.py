from django.urls import path
from . import views

urlpatterns = [
    # 1. Main Terminal Landing Workspace (Dynamic Portfolio Overview Matrix)
    path('', views.home_page, name='home'),
    
    # 2. Complete Filterable Market Capital Asset Matrix Table view
    path('companies/', views.company_list, name='company_list'),
    path('companies/upload/', views.upload_companies_csv, name='upload_companies_csv'),
    
    # 3. Deep Analytical View Layer Tracking Interface (8-Chart Canvas Widget View)
    path('company/<str:symbol>/', views.company_detail, name='company_detail'),
    
    # 4. Multi-Asset Comparative Stock Analysis Engine Panel
    path('compare/', views.compare_engine, name='compare_engine'),
    
    # 5. Multi-Parameter Quantitative Financial Ratio Screener
    path('screener/', views.market_screener, name='market_screener'),
    
    # 6. Sectoral Index Breakdown Performance Matrix
    path('sector/<str:name>/', views.sector_detail, name='sector_detail'),
]