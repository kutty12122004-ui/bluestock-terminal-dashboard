from django.db import models

class Company(models.Model):
    symbol = models.CharField(max_length=20, primary_key=True)
    company_name = models.CharField(max_length=150)
    sector = models.CharField(max_length=100)
    website = models.URLField(max_length=255, null=True, blank=True)
    about_company = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'dim_company'
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.symbol} - {self.company_name}"

class FiscalYear(models.Model):
    year_id = models.IntegerField(primary_key=True)
    year_label = models.CharField(max_length=10)
    is_ttm = models.BooleanField(default=False)
    sort_order = models.IntegerField()

    class Meta:
        db_table = 'dim_year'

class ProfitLossStatement(models.Model):
    # Explicitly adding an auto-incrementing ID primary key so Django can query it safely
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, to_field='symbol', db_column='symbol')
    year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE, to_field='year_id', db_column='year_id')
    revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ebitda = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    operating_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    opm_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    eps = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sales_growth = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        db_table = 'fact_profit_loss'

class BalanceSheet(models.Model):
    # Explicitly adding an auto-incrementing ID primary key so Django can query it safely
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, to_field='symbol', db_column='symbol')
    year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE, to_field='year_id', db_column='year_id')
    equity_capital = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    reserves = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    borrowings = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    other_liabilities = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    book_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    face_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'fact_balance_sheet'