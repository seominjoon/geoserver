from django.db import models
from jsonfield import JSONField

# Create your models here.


class SemanticParse(models.Model):
    # question = models.OneToOneField('questions.Question', null=True, blank=True, related_name='semantic_parse')
    sentence = models.ForeignKey("questions.Sentence", related_name='semantic_parses', null=True)
    number = models.IntegerField()
    parse = models.TextField()

    # text_formulas = JSONField()

    def __unicode__(self):
        return "%s-%d" % (unicode(self.sentence), self.number)

