from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 'shipping_address', 'payment_method', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-400',
                'placeholder': 'Nama lengkap penerima'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-400',
                'placeholder': 'email@example.com'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-400',
                'placeholder': 'Contoh: 081234567890'
            }),
            'shipping_address': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-400',
                'rows': 3,
                'placeholder': 'Alamat lengkap pengiriman, kelurahan, kecamatan, kota, kode pos'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:outline-none focus:border-neutral-400'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-400',
                'rows': 2,
                'placeholder': 'Catatan khusus pesanan (opsional)'
            }),
        }


class OrderTrackForm(forms.Form):
    order_number = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-400',
            'placeholder': 'Contoh: ORD-1A2B3C4D'
        })
    )
