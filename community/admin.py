from django.contrib import admin
from community.models import Tag,Comment,Discussion,DiscussionCategory
# Register your models here.

admin.site.register(Comment)
admin.site.register(Discussion)
admin.site.register(DiscussionCategory)
admin.site.register(Tag)
