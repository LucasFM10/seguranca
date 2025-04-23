from django.contrib import admin
from .models import HoneypotLog

class HoneypotLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'username', 'ipv4_address', 'country', 'region', 'city')
    readonly_fields = ('timestamp', 'username', 'user_agent', 'ipv4_address', 'user_host', 'country', 'region', 'city', 'latitude', 'longitude', 'post_params')

admin.site.register(HoneypotLog, HoneypotLogAdmin)
