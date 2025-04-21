import requests
from django.contrib import admin
from .models import HoneypotLog

class HoneypotLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'username', 'ipv4_address', 'ip_location', 'post_params')
    readonly_fields = ('timestamp', 'username', 'ipv4_address', 'ip_location', 'post_params')

    def ip_location(self, obj):
        try:
            response = requests.get(f"http://ip-api.com/json/{obj.ipv4_address}")
            data = response.json()
            if data['status'] == 'success':
                return f"{data['city']}, {data['regionName']}, {data['country']}"
            else:
                return "Unknown"
        except Exception as e:
            return f"Error: {str(e)}"

    ip_location.short_description = "IP Location"

admin.site.register(HoneypotLog, HoneypotLogAdmin)
