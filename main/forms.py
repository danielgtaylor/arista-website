from django import forms
from django.forms import widgets

class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField()
    message = forms.CharField(widget=widgets.Textarea())

