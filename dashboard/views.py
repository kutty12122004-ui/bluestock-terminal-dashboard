# dashboard/views.py
import csv
import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from companies.models import Company
from .forms import CSVUploadForm

def upload_companies_csv(request):
    """Handles parsing and uploading 'dim_company.csv' records from the UI browser."""
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            try:
                # Decode the uploaded file bytes to text strings
                data_set = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(data_set)
                
                created_count = 0
                updated_count = 0
                
                for row in reader:
                    ticker = row.get('symbol', '').strip()
                    name = row.get('company_name', '').strip().replace('\n', '')
                    industry = row.get('sector', '').strip()
                    
                    if ticker and name:  # Ensure key validation data structural criteria exist
                        obj, created = Company.objects.update_or_create(
                            symbol=ticker,
                            defaults={
                                'company_name': name,
                                'sector': industry,
                            }
                        )
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                
                messages.success(request, f"Successfully processed dataset! Added {created_count} new records, updated {updated_count}.")
                return redirect('/companies/')  # Redirect back to the complete asset list table matrix
                
            except Exception as e:
                messages.error(request, f"Error processing CSV file: {e}")
    else:
        form = CSVUploadForm()
        
    return render(request, 'dashboard/upload_csv.html', {'form': form})


def home_page(request):
    """Renders the Home page featuring global asset searches and unique sector lists."""
    # Dynamically extract all unique sectors from the Company records, ignoring null values
    sectors = Company.objects.values_list('sector', flat=True).distinct().exclude(sector__isnull=True).order_by('sector')
    featured = Company.objects.all()[:4]
    
    context = {
        'sectors': sectors,
        'featured': featured
    }
    return render(request, 'dashboard/home.html', context)


def company_list(request):
    """Renders the Complete Filterable Market Capital Asset Matrix Table View."""
    # Capture query parameter string submitted via client search requests
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        # Evaluates structural matching criteria across both tickers or official names
        companies = Company.objects.filter(
            Q(symbol__icontains=search_query) | 
            Q(company_name__icontains=search_query) |
            Q(sector__icontains=search_query)
        ).distinct()
    else:
        companies = Company.objects.all().order_by('symbol')
        
    context = {
        'companies': companies,
        'search_query': search_query,  # Matches the variable variable map inside company_list.html
    }
    return render(request, 'dashboard/company_list.html', context)


def company_detail(request, symbol):
    # Grab the specific company
    company = get_object_or_404(Company, symbol__iexact=symbol)
    
    # Generate a deterministic seed integer based on the company's ticker symbol string
    # This ensures ABB will always get its same unique curves, while TCS gets totally different ones!
    seed = int(hashlib.md5(company.symbol.encode('utf-8')).hexdigest(), 16)
    
    # Deterministic generation logic for unique corporate metrics
    rev_base = 500 + (seed % 400)
    rev_growth = 5 + (seed % 15)
    revenue_trend = [int(rev_base * (1 + (rev_growth / 100) * i)) for i in range(4)]
    
    npm_base = 8 + (seed % 18)
    npm_trend = [round(max(4.0, npm_base + ((-1)**i) * (seed % 3)), 1) for i in range(4)]
    
    de_base = round((seed % 120) / 100, 2)
    de_trend = [round(max(0.05, de_base - (i * 0.08)), 2) for i in range(4)]
    
    roce_base = 12 + (seed % 20)
    roce_trend = [int(roce_base + (i * (seed % 4))) for i in range(4)]
    
    # Shareholding patterns breakdown calculations (must add up to 100%)
    promoter = 40 + (seed % 30)
    fii = min(35, 100 - promoter - 10)
    dii = min(20, 100 - promoter - fii - 5)
    public = 100 - promoter - fii - dii
    shareholding = [promoter, fii, dii, public]
    
    asset_turnover = [round(1.0 + ((seed % 8) / 10) + (i * 0.1), 2) for i in range(4)]
    fcf_trend = [int((revenue_trend[i] * npm_trend[i] / 100) * 0.6) for i in range(4)]
    pe_trend = [round(15 + (seed % 35) + ((-1)**i) * (seed % 5), 1) for i in range(4)]

    context = {
        'company': company,
        'revenue_trend': revenue_trend,
        'npm_trend': npm_trend,
        'de_trend': de_trend,
        'roce_trend': roce_trend,
        'shareholding': shareholding,
        'asset_turnover': asset_turnover,
        'fcf_trend': fcf_trend,
        'pe_trend': pe_trend,
    }
    return render(request, 'dashboard/company_detail.html', context)


def compare_engine(request):
    """Handles multi-asset side-by-side comparative visualization matrix calculations."""
    return render(request, 'dashboard/compare.html')


def market_screener(request):
    """Multi-Parameter Quantitative Financial Ratio Screener."""
    companies = Company.objects.all()
    
    # Capture incoming filter queries from front-end user forms
    sector_filter = request.GET.get('sector', '')
    max_debt_equity = request.GET.get('max_de', '')
    min_net_profit = request.GET.get('min_npm', '')
    
    # Apply processing filter evaluation parameters
    if sector_filter:
        companies = companies.filter(sector__iexact=sector_filter)
    if max_debt_equity:
        try:
            companies = companies.filter(debt_to_equity__lte=float(max_debt_equity))
        except ValueError:
            pass  # Handles edge instances where data streams are submitted unparsed
    if min_net_profit:
        try:
            companies = companies.filter(net_profit_margin__gte=float(min_net_profit))
        except ValueError:
            pass
            
    all_sectors = Company.objects.values_list('sector', flat=True).distinct().exclude(sector__isnull=True).order_by('sector')
    
    context = {
        'companies': companies,
        'all_sectors': all_sectors,
        'selected_sector': sector_filter,
    }
    return render(request, 'dashboard/screener.html', context)


def sector_detail(request, name):
    """Renders consolidated sector summaries and micro-performance records."""
    companies = Company.objects.filter(sector__iexact=name).order_by('symbol')
    context = {
        'sector_name': name,
        'companies': companies
    }
    return render(request, 'dashboard/sector_detail.html', context)