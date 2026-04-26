from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def home(request):
    from django.urls import reverse
    context = {
        'today': timezone.now(),
        'currency': getattr(request.tenant, 'currency', 'KES') if request.tenant else 'KES',
        'stats': {
            'today_sales': '0.00',
            'today_transactions': 0,
            'product_count': 0,
            'low_stock_count': 0,
            'sales_change': 0,
        },
        'top_products': [],
        'recent_sales': [],
        'chart_labels': '[]',
        'chart_data': '[]',
        'onboarding': None,
        'license_warning': None,
        'low_stock_count': 0,
        'products_url': reverse('products:list'),
        'pos_url': reverse('sales:pos'),
        'staff_url': reverse('staff:list'),
        'reports_url': reverse('reports:overview'),
    }
    return render(request, 'dashboard/home.html', context)