from django.contrib import admin

from .models import Record, Settings, Survey


class RecordAdmin(admin.ModelAdmin):
	list_display = ['user_ip', 'created']


class SettingsAdmin(admin.ModelAdmin):
	list_display = ['finish_code']


class SurveyAdmin(admin.ModelAdmin):
	list_display = ['user_ip', 'created']


admin.site.register(Record, RecordAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Survey, SurveyAdmin)
