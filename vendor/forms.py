from django import forms
from .models import Vendor

class VendorForm(forms.ModelForm):
    vendor_licence = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_licence']