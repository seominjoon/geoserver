'''
Created on Jul 21, 2014

@author: minjoon

functions for updating the database
'''

from questions.models import QuestionTag, Question, Sentence
from questions.views import _split_text


def add_question(text, imgpath, tagwords=None):
    '''
    text: question text
    imgpath: path to the image
    '''
    if tagwords is None:
        tagwords = []
        
    question = Question(text=text,diagram=imgpath)
    question.save()
    
    for tagword in tagwords:
        if QuestionTag.objects.filter(word=tagword).exists():
            tag = QuestionTag.objects.get(word=tagword)
        else:
            tag = QuestionTag(word=tagword)
            tag.save()
        question.tags.add(tag)

    # Update new tags
    question.save()

