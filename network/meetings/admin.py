from django.contrib import admin
from .models import Meeting, Topic, Presence

admin.site.register(Meeting)
admin.site.register(Topic)
admin.site.register(Presence)
