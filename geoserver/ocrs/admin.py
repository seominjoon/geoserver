from django.contrib import admin

from ocrs.models import OCR, OCRTag


# Register your models here.
admin.site.register(OCR)
admin.site.register(OCRTag)
