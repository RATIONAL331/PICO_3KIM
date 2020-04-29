from django import forms

from django.contrib.auth.models import User

class ChargeForm(forms.Form):
    PICOIN = forms.IntegerField(max_value=5000, min_value=1)

class DonateForm(forms.Form):
    PICOIN = forms.IntegerField(max_value=2000, min_value=1)