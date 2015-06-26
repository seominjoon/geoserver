import os
import time
import uuid

from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
class QuestionTag(models.Model):
    '''
    Tag for grouping questionsm
    '''
    word = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.word


class ChoiceWord(models.Model):
    text = models.CharField(max_length=32)
    index = models.IntegerField()
    choice = models.ForeignKey('questions.Choice', related_name='words')

    def __unicode__(self):
        return self.text


class SentenceWord(models.Model):
    text = models.CharField(max_length=32)
    index = models.IntegerField()
    sentence = models.ForeignKey('questions.Sentence', related_name='words')

    def __unicode__(self):
        return self.text


class Sentence(models.Model):
    text = models.TextField()
    index = models.IntegerField()
    question = models.ForeignKey('questions.Question', related_name='sentences')

    def __unicode__(self):
        return "%d-%d" % (self.question.pk, self.index)


class Choice(models.Model):
    '''
    Each choice corresponds to one question.
    Each question can have multiple choices.
    Number is the choice number (e.g. 1 through 5)
    '''
    text = models.TextField()
    number = models.IntegerField()
    question = models.ForeignKey('questions.Question', related_name='choices')
    
    def __unicode__(self):
        return "%d-%d" % (self.question.pk, self.number)


class SentenceExpression(models.Model):
    text = models.CharField(max_length=64)
    index = models.CharField(max_length=32)
    sentence = models.ForeignKey('questions.Sentence', related_name='expressions')

    def __unicode__(self):
        return unicode(self.sentence) + "-" + self.index


class ChoiceExpression(models.Model):
    text = models.CharField(max_length=64)
    index = models.CharField(max_length=32)
    choice = models.ForeignKey('questions.Choice', related_name='expressions')

    def __unicode__(self):
        return unicode(self.choice) + "-" + self.index


def get_upload_path(instance, filename):
    '''
    Upload path function for Question model
    '''
    ext = os.path.splitext(filename)[1]
    name = "question-%d-%s%s" %(round(time.time()),uuid.uuid4(), ext)
    return os.path.join('questions', name)


class Question(models.Model):
    '''
    Each question contains text and diagram image.
    Each question is tagged for filtering purpose.
    Each question can have more than one tags (thus M2M relationship).
    Each question has several choices (see Choice class).
    '''
    text = models.TextField()
    diagram = models.ImageField(upload_to=get_upload_path)
    has_choices = models.BooleanField(default=True, blank=True)
    valid = models.BooleanField(default=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(QuestionTag, blank=True)

    def __unicode__(self):
        return str(self.pk)
    
    def get_absolute_url(self):
        return reverse('questions-detail', kwargs={'slug': self.pk})
    
    def repr(self, request=None):
        choices = dict([(choice.number,choice.text) for choice in self.choices.all()])
        if request is None:
            diagram_url = self.diagram.url
        else:
            diagram_url = request.build_absolute_uri(self.diagram.url)
        return {'pk': self.pk,
                'text': self.text,
                'words': {sentence.index: {word.index: word.text for word in sentence.words.all()} for sentence in self.sentences.all()},
                'diagram_url': diagram_url,
                'has_choices': self.has_choices,
                'valid': self.valid,
                'answer': self.answer,
                'choices': choices,
                }
