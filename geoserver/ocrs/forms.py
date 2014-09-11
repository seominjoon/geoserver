'''
Created on Sep 10, 2014

@author: minjoon
'''

from django.forms import ModelForm

from ocrs.models import OCR


class OCRForm(ModelForm):
    class Meta:
        model = OCR
        fields = ['ocr', 'learner_name', 'descriptor_name']