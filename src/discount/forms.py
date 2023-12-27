from django import forms


class DiscountForm(forms.Form):
    code = forms.CharField(label='Купон', max_length=100)
