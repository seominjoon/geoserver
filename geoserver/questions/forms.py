'''
Created on Jul 22, 2014

@author: minjoon
'''

from django.forms import ModelForm

from questions.models import Question, Choice


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'diagram', 'has_choices', 'valid', 'answer']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['answer'].required = False
        
class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'text', 'number']

class ChoiceLimitedForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['text']