from django.contrib import admin

from .models import Record, Settings


class RecordAdmin(admin.ModelAdmin):
	list_display = ['created']


class SettingsAdmin(admin.ModelAdmin):
	list_display = ['finish_code']


admin.site.register(Record, RecordAdmin)
admin.site.register(Settings, SettingsAdmin)
