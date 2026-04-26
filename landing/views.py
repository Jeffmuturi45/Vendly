from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from accounts.models import CustomUser
from tenants.models import Business, OnboardingProgress
from django.utils import timezone

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    features = [
        {
            'icon': 'fa-cash-register',
            'color': 'green',
            'title': 'Fast Point of Sale',
            'description': 'Ring up sales in seconds. Add products to cart, apply discounts, and accept cash or MPESA instantly.',
        },
        {
            'icon': 'fa-boxes-stacked',
            'color': 'yellow',
            'title': 'Inventory Tracking',
            'description': 'Stock levels update automatically on every sale. Get alerts before you run out of your best sellers.',
        },
        {
            'icon': 'fa-chart-line',
            'color': 'green',
            'title': 'Sales Analytics',
            'description': 'Daily, weekly, and monthly reports. See your best products, busiest hours, and revenue trends.',
        },
        {
            'icon': 'fa-users',
            'color': 'yellow',
            'title': 'Staff Management',
            'description': 'Add cashiers and managers with their own logins. Control exactly what each person can see and do.',
        },
        {
            'icon': 'fa-receipt',
            'color': 'green',
            'title': 'Digital Receipts',
            'description': 'Print receipts or share them via WhatsApp instantly. Customers love it, paper waste gone.',
        },
        {
            'icon': 'fa-shield-halved',
            'color': 'yellow',
            'title': 'Secure & Isolated',
            'description': 'Every business is completely isolated. Your data is yours — no sharing, no mixing, ever.',
        },
    ]

    basic_features = [
        'Up to 500 products',
        'Unlimited daily sales',
        'Cash & MPESA payments',
        'Basic sales reports',
        '2 staff accounts',
        'Digital receipts',
        'Email support',
    ]
    business_types: [
    ('fa-store',    'Retail'),
    ('fa-pills',    'Pharmacy'),
    ('fa-scissors', 'Salon'),
    ('fa-utensils', 'Restaurant'),
    ('fa-warehouse','Wholesale'),
    ('fa-seedling', 'Agro'),
]
    pro_features = [
        'Unlimited products',
        'Unlimited daily sales',
        'Cash, MPESA & Paystack',
        'Advanced analytics',
        'Unlimited staff accounts',
        'WhatsApp receipts',
        'Low stock alerts',
        'CSV import/export',
        'Priority support',
    ]

    return render(request, 'landing/index.html', {
        'features':       features,
        'basic_features': basic_features,
        'pro_features':   pro_features,
        'today':          timezone.now(),
    })


def enter_demo(request):
    """
    Creates (or reuses) a shared demo tenant and logs the visitor in
    as a read-write demo cashier. Session is flagged as demo_mode.
    """
    DEMO_SLUG = 'vendly-demo'

    business, _ = Business.objects.get_or_create(
        slug=DEMO_SLUG,
        defaults={
            'name':          'Vendly Demo Store',
            'business_type': 'retail',
            'country':       'Kenya',
            'currency':      'KES',
        }
    )

    demo_user, created = CustomUser.objects.get_or_create(
        username='demo_user',
        defaults={
            'email':      'demo@vendly.app',
            'tenant':     business,
            'role':       CustomUser.ROLE_CASHIER,
            'first_name': 'Demo',
            'last_name':  'User',
        }
    )
    if created:
        demo_user.set_password('VendlyDemo2024!')
        demo_user.save()

    # Ensure demo tenant has some sample products
    _seed_demo_products(business, demo_user)

    request.session['demo_mode'] = True
    request.session.set_expiry(1800)   # 30 min
    login(request, demo_user,
          backend='django.contrib.auth.backends.ModelBackend')
    messages.info(request, 'You are in demo mode. Explore freely!')
    return redirect('dashboard:home')


def _seed_demo_products(business, user):
    from products.models import Product
    if Product.objects.filter(tenant=business).exists():
        return
    samples = [
        ('Mineral Water 500ml', 50,  30,  100),
        ('Bread 400g',          80,  55,  60),
        ('Cooking Oil 1L',      250, 190, 30),
        ('Sugar 1kg',           130, 95,  80),
        ('Milk 500ml',          65,  50,  50),
        ('Soda 300ml',          60,  42,  120),
        ('Rice 1kg',            140, 105, 45),
        ('Eggs (tray 30)',      480, 390, 20),
    ]
    for name, price, cost, stock in samples:
        Product.objects.create(
            tenant=business, name=name, price=price,
            cost_price=cost, stock=stock, created_by=user
        )