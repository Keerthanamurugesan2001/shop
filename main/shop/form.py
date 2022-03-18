from django import forms


class Addstock(forms.Form):
    productname = forms.CharField(max_length=200)
    price = forms.DecimalField(max_digits=5, decimal_places=2)
    description = forms.CharField()
    productimage = forms.ImageField(required=False)
    quantity = forms.IntegerField()
    checkbutton = forms.BooleanField(required=False)