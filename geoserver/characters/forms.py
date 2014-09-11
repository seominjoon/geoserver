'''
Created on Sep 5, 2014

@author: minjoon
'''
from django.forms.models import ModelForm

from characters.models import Character


class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ['image', 'label', 'labeled', 'valid']
        
    def __init__(self, *args, **kwargs):
        super(CharacterForm, self).__init__(*args, **kwargs)
        # Label does not need to be defined when uploading.
        self.fields['label'].required = False
        #self.fields['tags'].required = False