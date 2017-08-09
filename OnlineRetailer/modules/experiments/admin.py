from django.contrib import admin

from .models import Record, Settings, Purchase


class RecordAdmin(admin.ModelAdmin):
    list_display = ['created']


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['finish_code']


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['products', 'amount']


admin.site.register(Record, RecordAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Purchase, PurchaseAdmin)
