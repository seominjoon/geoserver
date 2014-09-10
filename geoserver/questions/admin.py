from django.contrib import admin
from geoserver.questions.models import Question, QuestionTag

# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionTag)