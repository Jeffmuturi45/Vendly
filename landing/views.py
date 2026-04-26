from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from accounts.models import CustomUser
from tenants.models import Business


def index(request):
    return render(request, 'landing/index.html')


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