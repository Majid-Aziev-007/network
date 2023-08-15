from django import forms

class KeyForm(forms.Form):
    key_input = forms.CharField(label="Ключ")
