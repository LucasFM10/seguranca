from django.db import models


class HoneypotLog(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	username = models.CharField(max_length=255, null=True, blank=True)
	ipv4_address = models.GenericIPAddressField()
	post_params = models.JSONField(default=dict)

	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
	country = models.CharField(max_length=100, blank=True, null=True)
	region = models.CharField(max_length=100, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return(f'[{self.timestamp}] - {self.username} - {self.ipv4_address}')
