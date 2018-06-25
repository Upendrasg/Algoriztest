from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    pnl = models.CharField(max_length=10000, null=True, blank=True)
    position = models.CharField(max_length=10000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
