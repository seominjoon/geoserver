from django.db import models
from jsonfield import JSONField

# Create your models here.


class SemanticParse(models.Model):
    question = models.OneToOneField('questions.Question', null=True, blank=True, related_name='semantic_parse')
    text_formulas = JSONField()

    def __unicode__(self):
        return str(self.question.pk)

