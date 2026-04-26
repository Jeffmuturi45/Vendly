from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.utils.text import slugify

from accounts.models import CustomUser
from .models import Business, OnboardingProgress
from .forms import (
    Step1BusinessForm, Step2LocationForm,
    Step3ProductForm,  Step4StaffForm, Step5ConfirmForm,
)

STEPS = {
    1: {'form': Step1BusinessForm,  'title': 'Your business',    'skippable': False},
    2: {'form': Step2LocationForm,  'title': 'Location',         'skippable': False},
    3: {'form': Step3ProductForm,   'title': 'First product',    'skippable': True},
    4: {'form': Step4StaffForm,     'title': 'Add staff',        'skippable': True},
    5: {'form': Step5ConfirmForm,   'title': 'Create account',   'skippable': False},
}
TOTAL = len(STEPS)


def onboarding(request):
    step = int(request.GET.get('step', 1))
    step = max(1, min(step, TOTAL))

    # Initialise session bucket
    if 'onboarding' not in request.session:
        request.session['onboarding'] = {}

    data      = request.session['onboarding']
    step_meta = STEPS[step]
    FormClass = step_meta['form']
    skippable = step_meta['skippable']

    # ── Skip ───────────────────────────────────────────────────────────────
    if request.GET.get('skip') and skippable:
        return _advance(step)

    # ── POST ───────────────────────────────────────────────────────────────
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            data[f'step{step}'] = form.cleaned_data
            request.session.modified = True

            if step < TOTAL:
                return _advance(step)

            # ── Final step: create everything ──────────────────────────────
            return _finalise(request, data)
        # invalid — fall through to re-render with errors
    else:
        # Pre-fill if the user came back
        initial = data.get(f'step{step}', {})
        form    = FormClass(initial=initial)

    context = {
        'form':        form,
        'step':        step,
        'total_steps': TOTAL,
        'step_title':  step_meta['title'],
        'steps_range': range(1, TOTAL + 1),
        'skippable':   skippable,
    }
    return render(request, 'tenants/onboarding.html', context)


# ── helpers ────────────────────────────────────────────────────────────────

def _advance(current_step):
    return redirect(f'/tenants/onboarding/?step={current_step + 1}')


def _finalise(request, data):
    s1 = data.get('step1', {})
    s2 = data.get('step2', {})
    s3 = data.get('step3', {})
    s4 = data.get('step4', {})
    s5 = data.get('step5', {})

    business = Business.objects.create(
        name          = s1.get('name', 'My Business'),
        business_type = s1.get('business_type', 'retail'),
        country       = s2.get('country', 'Kenya'),
        currency      = s2.get('currency', 'KES'),
    )
    OnboardingProgress.objects.create(business=business)

    owner = CustomUser.objects.create_user(
        username   = s5.get('username'),
        email      = s5.get('email'),
        password   = s5.get('password1'),
        tenant     = business,
        role       = CustomUser.ROLE_OWNER,
        first_name = s1.get('name', '').split()[0],
    )

    if s3.get('product_name'):
        from products.models import Product
        Product.objects.create(
            tenant     = business,
            name       = s3['product_name'],
            price      = float(s3['product_price']),   # ← convert Decimal → float
            stock      = int(s3.get('product_stock', 0)),
            created_by = owner,
        )
        business.onboarding.added_product = True
        business.onboarding.save()

    if s4.get('staff_email'):
        CustomUser.objects.create_user(
            username   = s4['staff_email'].split('@')[0],
            email      = s4['staff_email'],
            password   = s4['staff_password'],
            first_name = s4['staff_name'].split()[0],
            last_name  = ' '.join(s4['staff_name'].split()[1:]),
            tenant     = business,
            role       = CustomUser.ROLE_CASHIER,
        )
        business.onboarding.added_staff = True
        business.onboarding.save()

    del request.session['onboarding']
    login(request, owner,
          backend='django.contrib.auth.backends.ModelBackend')
    messages.success(request, f'Welcome to Vendly, {business.name}!')
    return redirect('dashboard:home')