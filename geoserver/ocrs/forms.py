'''
Created on Sep 10, 2014

@author: minjoon
'''

from django import forms

from characters.models import Character
from ocrs.models import OCR


class OCRForm(forms.ModelForm):
    class Meta:
        model = OCR
        fields = ['ocr_pickle', 'learner_name', 'descriptor_name']
        
        
class TestCharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['image']
        
class OCRCreateForm(forms.Form):
    set_default = forms.BooleanField(
        label='Set this OCR to be default',
        required=False,
    )

class OCRForm2(forms.Form):
    ocr_manager_p = forms.FileField(
        label='Upload OCRManager pickle file'
    )