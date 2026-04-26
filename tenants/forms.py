from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
from .models import Business

CURRENCY_CHOICES = [
    ('KES', 'KES — Kenyan Shilling'),
    ('UGX', 'UGX — Ugandan Shilling'),
    ('TZS', 'TZS — Tanzanian Shilling'),
    ('USD', 'USD — US Dollar'),
    ('GBP', 'GBP — British Pound'),
    ('EUR', 'EUR — Euro'),
    ('NGN', 'NGN — Nigerian Naira'),
    ('GHS', 'GHS — Ghanaian Cedi'),
    ('ZAR', 'ZAR — South African Rand'),
]

COUNTRY_CHOICES = [
    ('Kenya',        'Kenya'),
    ('Uganda',       'Uganda'),
    ('Tanzania',     'Tanzania'),
    ('Nigeria',      'Nigeria'),
    ('Ghana',        'Ghana'),
    ('South Africa', 'South Africa'),
    ('Rwanda',       'Rwanda'),
    ('Ethiopia',     'Ethiopia'),
    ('Other',        'Other'),
]


class Step1BusinessForm(forms.Form):
    """Business name + type."""
    name          = forms.CharField(
        max_length=120,
        label='Business name',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Mama Njeri Shop'}),
    )
    business_type = forms.ChoiceField(
        choices=Business.BUSINESS_TYPES,
        label='Business type',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('name',          css_class='vendly-input'),
            Field('business_type', css_class='vendly-input'),
        )


class Step2LocationForm(forms.Form):
    """Country + currency."""
    country  = forms.ChoiceField(choices=COUNTRY_CHOICES, label='Country')
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES, label='Currency')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('country',  css_class='vendly-input'),
            Field('currency', css_class='vendly-input'),
        )


class Step3ProductForm(forms.Form):
    """First product — skippable."""
    product_name  = forms.CharField(
        max_length=120, label='Product name',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Bread 400g'}),
    )
    product_price = forms.DecimalField(
        max_digits=10, decimal_places=2, label='Selling price',
        widget=forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01'}),
    )
    product_stock = forms.IntegerField(
        label='Opening stock (units)', initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )

    def clean_product_price(self):
        return float(self.cleaned_data['product_price'])  # session-safe
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('product_name',  css_class='vendly-input'),
            Field('product_price', css_class='vendly-input'),
            Field('product_stock', css_class='vendly-input'),
        )


class Step4StaffForm(forms.Form):
    """First staff member — skippable."""
    staff_name     = forms.CharField(
        max_length=150, label='Full name',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Jane Wanjiru'}),
    )
    staff_email    = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={'placeholder': 'jane@example.com'}),
    )
    staff_password = forms.CharField(
        label='Temporary password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Min 8 characters'}),
        min_length=8,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('staff_name',     css_class='vendly-input'),
            Field('staff_email',    css_class='vendly-input'),
            Field('staff_password', css_class='vendly-input'),
        )


class Step5ConfirmForm(forms.Form):
    """Owner account creation — final step."""
    username  = forms.CharField(
        max_length=150, label='Choose a username',
        widget=forms.TextInput(attrs={'placeholder': 'yourname'}),
    )
    email     = forms.EmailField(
        label='Your email',
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Min 8 characters'}),
        min_length=8,
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned