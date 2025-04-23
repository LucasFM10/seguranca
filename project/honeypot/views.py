from django.shortcuts import render
from django.utils import timezone
from .models import HoneypotLog
import requests

def honeypot_login(request):
    if request.method == 'POST':
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')

        location_data = {
                    'latitude': None,
                    'longitude': None,
                    'country': None,
                    'region': None,
                    'city': None,
                }
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
            pass
   
        HoneypotLog.objects.create(
            timestamp=timezone.now(),
            username=request.user, 
            user_agent=user_agent,
            ipv4_address=ip_address,
            user_host=request.get_host(),
            latitude = location_data['latitude'],
            longitude = location_data['longitude'],
            country = location_data['country'],
            region = location_data['region'],
            city = location_data['city'],
            post_params=dict(request.POST)
        )
        return render(request, 'admin_login.html', {
            'error_message': "Please enter the correct username and password.",
        })

    return render(request, 'admin_login.html')