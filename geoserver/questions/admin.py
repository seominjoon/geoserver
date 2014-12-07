from django.contrib import admin

from questions.models import Question, QuestionTag, Choice


# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuestionTag)