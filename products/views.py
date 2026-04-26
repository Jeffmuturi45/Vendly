from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm, CategoryForm


def tenant_required(view_func):
    """Ensures user has a tenant attached."""
    def wrapper(request, *args, **kwargs):
        if not request.tenant:
            messages.error(request, 'No business found for your account.')
            return redirect('landing:index')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return login_required(wrapper)


@tenant_required
def list_view(request):
    qs = Product.objects.filter(tenant=request.tenant)

    # Search
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(barcode__icontains=q))

    # Category filter
    cat_id = request.GET.get('cat', '')
    if cat_id:
        qs = qs.filter(category_id=cat_id)

    # Status filter
    status = request.GET.get('status', '')
    if status == 'active':
        qs = qs.filter(is_active=True)
    elif status == 'inactive':
        qs = qs.filter(is_active=False)
    elif status == 'low':
        qs = [p for p in qs if p.is_low_stock]

    categories = Category.objects.filter(tenant=request.tenant)

    context = {
        'products':   qs,
        'categories': categories,
        'q':          q,
        'cat_id':     cat_id,
        'status':     status,
        'total':      Product.objects.filter(tenant=request.tenant).count(),
        'low_count':  sum(1 for p in Product.objects.filter(tenant=request.tenant) if p.is_low_stock),
    }
    return render(request, 'products/list.html', context)


@tenant_required
def add_view(request):
    form = ProductForm(
        tenant=request.tenant,
        data=request.POST or None,
        files=request.FILES or None,
    )
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.tenant     = request.tenant
        product.created_by = request.user
        product.save()
        # Update onboarding flag
        if hasattr(request.tenant, 'onboarding'):
            ob = request.tenant.onboarding
            if not ob.added_product:
                ob.added_product = True
                ob.save()
        messages.success(request, f'"{product.name}" added successfully.')
        if request.POST.get('add_another'):
            return redirect('products:add')
        return redirect('products:list')

    return render(request, 'products/form.html', {
        'form': form, 'action': 'Add product', 'is_edit': False
    })


@tenant_required
def edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk, tenant=request.tenant)
    form = ProductForm(
        tenant=request.tenant,
        data=request.POST or None,
        files=request.FILES or None,
        instance=product,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'"{product.name}" updated.')
        return redirect('products:list')

    return render(request, 'products/form.html', {
        'form': form, 'action': 'Edit product',
        'is_edit': True, 'product': product,
    })


@tenant_required
def delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk, tenant=request.tenant)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('products:list')
    return render(request, 'products/confirm_delete.html', {'product': product})


@tenant_required
def toggle_active(request, pk):
    product = get_object_or_404(Product, pk=pk, tenant=request.tenant)
    product.is_active = not product.is_active
    product.save()
    state = 'activated' if product.is_active else 'deactivated'
    messages.success(request, f'"{product.name}" {state}.')
    return redirect('products:list')

# @login_required
# def list_view(request):
#     return render(request, 'products/list.html')