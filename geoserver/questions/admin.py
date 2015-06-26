from django.contrib import admin

from questions.models import Question, QuestionTag, Choice, Sentence, SentenceWord, ChoiceWord, SentenceExpression, \
    ChoiceExpression


# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuestionTag)
admin.site.register(Sentence)
admin.site.register(SentenceWord)
admin.site.register(ChoiceWord)
admin.site.register(SentenceExpression)
admin.site.register(ChoiceExpression)