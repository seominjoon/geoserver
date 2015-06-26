from django.contrib import admin

# Register your models here.
from semantics.models import SentenceAnnotation, ChoiceAnnotation

admin.site.register(SentenceAnnotation)
admin.site.register(ChoiceAnnotation)
