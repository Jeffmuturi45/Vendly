import shortuuid
from django.db import models
from django.utils.text import slugify


class Business(models.Model):
    BUSINESS_TYPES = [
        ('retail',     'Retail shop'),
        ('salon',      'Salon / Barbershop'),
        ('pharmacy',   'Pharmacy'),
        ('restaurant', 'Restaurant / Café'),
        ('wholesale',  'Wholesale'),
        ('other',      'Other'),
    ]

    uid           = models.CharField(max_length=12, unique=True, editable=False)
    name          = models.CharField(max_length=120)
    slug          = models.SlugField(max_length=80, unique=True)
    business_type = models.CharField(max_length=30, choices=BUSINESS_TYPES)
    country       = models.CharField(max_length=60)
    currency      = models.CharField(max_length=10, default='KES')
    logo          = models.ImageField(upload_to='logos/', blank=True)
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = shortuuid.ShortUUID().random(length=10)
        if not self.slug:
            base = slugify(self.name)
            slug = base
            n = 1
            while Business.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class OnboardingProgress(models.Model):
    business        = models.OneToOneField(
        Business, on_delete=models.CASCADE, related_name='onboarding'
    )
    added_product   = models.BooleanField(default=False)
    made_first_sale = models.BooleanField(default=False)
    added_staff     = models.BooleanField(default=False)
    viewed_reports  = models.BooleanField(default=False)

    @property
    def percent_complete(self):
        flags = [self.added_product, self.made_first_sale,
                 self.added_staff, self.viewed_reports]
        return int(sum(flags) / len(flags) * 100)