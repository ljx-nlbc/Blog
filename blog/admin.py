from django.contrib import admin
from .models import Tag,Article,Category

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
