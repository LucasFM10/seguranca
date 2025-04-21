from django.db import models

class RequestLog(models.Model):
    ip = models.GenericIPAddressField()
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.path} - {self.ip}"
