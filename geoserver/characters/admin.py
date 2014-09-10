from django.contrib import admin

from geoserver.characters.models import Character, CharacterTag


# Register your models here.
admin.site.register(Character)
admin.site.register(CharacterTag)