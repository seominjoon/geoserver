'''
Created on Sep 10, 2014

@author: minjoon
'''

from django.forms import ModelForm

from characters.models import Character
from ocrs.models import OCR


class OCRForm(ModelForm):
    class Meta:
        model = OCR
        fields = ['ocr_pickle', 'learner_name', 'descriptor_name']
        
class TestCharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ['image']