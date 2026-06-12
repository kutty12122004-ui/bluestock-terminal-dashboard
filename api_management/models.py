from django.db import models
from django.contrib.auth.models import User

class ChannelPartner(models.Model):
    TIER_CHOICES = [
        ('BASIC', 'Basic'),
        ('PRO', 'Pro'),
        ('ENTERPRISE', 'Enterprise'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner_profile')
    partner_name = models.CharField(max_length=100)
    tier = models.CharField(max_length=15, choices=TIER_CHOICES, default='BASIC')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.partner_name} [{self.tier}]"

class APIKey(models.Model):
    partner = models.ForeignKey(ChannelPartner, on_delete=models.CASCADE, related_name='api_keys')
    key_id = models.CharField(max_length=40, unique=True)
    secret_hash = models.CharField(max_length=128, help_text="Bcrypt hashed secret string storage")
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)

class APIUsageLog(models.Model):
    partner = models.ForeignKey(ChannelPartner, on_delete=models.SET_NULL, null=True)
    endpoint = models.CharField(max_length=255)
    http_method = models.CharField(max_length=10)
    response_status = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)