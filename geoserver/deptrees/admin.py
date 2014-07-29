from django.contrib import admin

from deptrees.models import DepTree, DepTreeImage, Parser


# Register your models here.
admin.site.register(DepTree)
admin.site.register(DepTreeImage)
admin.site.register(Parser)