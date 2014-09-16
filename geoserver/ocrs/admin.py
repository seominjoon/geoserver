from django.contrib import admin

from ocrs.models import OCR, OCRTag, Variable


# Register your models here.
admin.site.register(OCR)
admin.site.register(OCRTag)
admin.site.register(Variable)

