from django.shortcuts import render
from django.http import HttpResponse
from .models import RequestLog
import requests

def get_geolocation(ip):
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5)
        data = response.json()
        return f"{data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')} - ISP: {data.get('org', 'Unknown')}"
    except Exception:
        return "Geolocation lookup failed"

def home(request):
    return HttpResponse("<h1>Bem-vindo à Home do Aplicativo!</h1><p>Esta página não contém informações sobre as requisições.</p>")

def logging(request):
    logs = RequestLog.objects.order_by('-timestamp')[:100]
    return render(request, 'logging.html', {'logs': logs})

def honeypot(request, path=""):
    ip_address = request.META.get('REMOTE_ADDR')
    location = get_geolocation(ip_address)

    RequestLog.objects.create(
        ip=ip_address,
        method=request.method,
        path=request.path,
        location=location
    )

    return HttpResponse("403 Forbidden - Access Denied", status=403)
