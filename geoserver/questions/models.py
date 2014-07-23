from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

class QuestionTag(models.Model):
    '''
    Tag for grouping questions.
    '''
    word = models.CharField(max_length=32)

class Question(models.Model):
    '''
    Each question contains text and diagram image.
    Each question is tagged for filtering purpose.
    '''
    text = models.TextField()
    diagram = models.ImageField(upload_to="questions/")
    tag = models.ManyToManyField(QuestionTag)
    
    def __unicode__(self):
        return self.text
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk', self.pk})

