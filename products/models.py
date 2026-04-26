from django.db import models
from django.conf import settings


class Category(models.Model):
    tenant = models.ForeignKey(
        'tenants.Business', on_delete=models.CASCADE, related_name='categories'
    )
    name   = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ('tenant', 'name')


class Product(models.Model):
    tenant     = models.ForeignKey(
        'tenants.Business', on_delete=models.CASCADE, related_name='products'
    )
    category   = models.ForeignKey(
        Category, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='products'
    )
    name       = models.CharField(max_length=180)
    barcode    = models.CharField(max_length=60, blank=True)
    price      = models.DecimalField(max_digits=12, decimal_places=2)
    cost_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text='Cost price for profit calculations'
    )
    stock          = models.PositiveIntegerField(default=0)
    low_stock_alert = models.PositiveIntegerField(
        default=5, help_text='Alert when stock falls below this'
    )
    image      = models.ImageField(upload_to='products/', blank=True)
    is_active  = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        on_delete=models.SET_NULL, related_name='products_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_low_stock(self):
        return self.stock <= self.low_stock_alert

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']