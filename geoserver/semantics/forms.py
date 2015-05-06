from django import forms
from django.forms import ModelForm
from semantics.models import SemanticParse

__author__ = 'minjoon'


class SentenceParseForm(forms.Form):
    parses = forms.CharField(widget=forms.Textarea(attrs={'cols': 128, 'rows': 10}))
