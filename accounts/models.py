import shortuuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_SUPERADMIN = 'superadmin'
    ROLE_OWNER      = 'owner'
    ROLE_MANAGER    = 'manager'
    ROLE_CASHIER    = 'cashier'
    ROLES = [
        (ROLE_SUPERADMIN, 'Super Admin'),
        (ROLE_OWNER,      'Owner'),
        (ROLE_MANAGER,    'Manager'),
        (ROLE_CASHIER,    'Cashier'),
    ]

    tenant  = models.ForeignKey(
        'tenants.Business',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='users',
    )
    role    = models.CharField(max_length=20, choices=ROLES, default=ROLE_CASHIER)
    phone   = models.CharField(max_length=20, blank=True)
    avatar  = models.ImageField(upload_to='avatars/', blank=True)

    def save(self, *args, **kwargs):
        # Superusers always get superadmin role, no tenant required
        if self.is_superuser:
            self.role = self.ROLE_SUPERADMIN
        super().save(*args, **kwargs)

    def is_owner(self):
        return self.role == self.ROLE_OWNER

    def is_superadmin(self):
        return self.role == self.ROLE_SUPERADMIN

    def can_access_reports(self):
        return self.role in [self.ROLE_SUPERADMIN, self.ROLE_OWNER, self.ROLE_MANAGER]

    def can_manage_staff(self):
        return self.role in [self.ROLE_SUPERADMIN, self.ROLE_OWNER]

    def can_manage_products(self):
        return self.role in [self.ROLE_SUPERADMIN, self.ROLE_OWNER, self.ROLE_MANAGER]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"