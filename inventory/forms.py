from django import forms
from .models import ProductList

class PurchaseForm(forms.Form):
    product = forms.ModelChoiceField(queryset=ProductList.objects.all(), label='产品')
    quantity = forms.IntegerField(label='购买数量', min_value=1)