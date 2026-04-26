from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('products/', include('products.urls', namespace='products')),
    path('sales/', include('sales.urls', namespace='sales')),
    path('staff/', include('staff.urls', namespace='staff')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('licensing/', include('licensing.urls', namespace='licensing')),
    # path('payments/', include('payments.urls', namespace='payments')),
    path('tenants/', include('tenants.urls', namespace='tenants')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)