from django.db import models
from companies.models import Company, FiscalYear

class CompanyScore(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='ml_score')
    health_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Calculated 0-100 ML Score")
    health_label = models.CharField(max_length=20, help_text="Excellent, Good, Stable, Weak, Critical")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.symbol} - {self.health_score} ({self.health_label})"

class AnomalyFlag(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='anomalies')
    year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=50, help_text="e.g., debt_to_equity_ratio, sales_growth")
    z_score = models.FloatField()
    is_anomaly = models.BooleanField(default=False)
    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'year', 'metric_name')