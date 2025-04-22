from django.shortcuts import render
from django.utils import timezone
from .models import HoneypotLog
import requests

def honeypot_login(request):
    if request.method == 'POST':
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')

        location_data = {}
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()
            if data.get('status') == 'success':
                location_data = {
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'country': data.get('country'),
                    'region': data.get('regionName'),
                    'city': data.get('city'),
                }
        except Exception as e:
            location_data = {}
        
        HoneypotLog.objects.create(
            timestamp=timezone.now(),
            username=request.user, 
            ipv4_address=ip_address, 
            post_params=dict(request.POST),
            **location_data
        )
        return render(request, 'admin_login.html', {
            'error_message': "Please enter the correct username and password.",
        })

    return render(request, 'admin_login.html')