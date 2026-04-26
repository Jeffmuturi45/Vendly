from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit
from .models import Product, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['name'].widget.attrs['placeholder'] = 'e.g. Beverages'


class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = [
            'name', 'category', 'barcode',
            'price', 'cost_price', 'stock',
            'low_stock_alert', 'image', 'is_active',
        ]
        widgets = {
            'name':    forms.TextInput(attrs={'placeholder': 'Product name'}),
            'barcode': forms.TextInput(attrs={'placeholder': 'Barcode / SKU (optional)'}),
            'price':   forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01'}),
            'cost_price': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01'}),
            'stock':   forms.NumberInput(attrs={'placeholder': '0'}),
            'low_stock_alert': forms.NumberInput(attrs={'placeholder': '5'}),
        }

    def __init__(self, tenant=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('name'),
            Row(
                Column('category', css_class='w-full sm:w-1/2 pr-0 sm:pr-2'),
                Column('barcode',  css_class='w-full sm:w-1/2'),
            ),
            Row(
                Column('price',      css_class='w-full sm:w-1/2 pr-0 sm:pr-2'),
                Column('cost_price', css_class='w-full sm:w-1/2'),
            ),
            Row(
                Column('stock',           css_class='w-full sm:w-1/2 pr-0 sm:pr-2'),
                Column('low_stock_alert', css_class='w-full sm:w-1/2'),
            ),
            Field('image'),
            Field('is_active'),
        )
        # Only show this tenant's categories
        if tenant:
            self.fields['category'].queryset = Category.objects.filter(tenant=tenant)
            self.fields['category'].empty_label = 'No category'