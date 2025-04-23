from django.db import models


class HoneypotLog(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)

	username = models.CharField(max_length=255, null=True, blank=True)
	user_agent = models.CharField(max_length=255, null=True, blank=True)
	ipv4_address = models.GenericIPAddressField(null=True, blank=True)
	user_host = models.CharField(max_length=255, null=True, blank=True)

	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
	country = models.CharField(max_length=255, blank=True, null=True)
	region = models.CharField(max_length=255, blank=True, null=True)
	city = models.CharField(max_length=255, blank=True, null=True)

	post_params = models.JSONField(default=dict)

	def __str__(self):
		return(f'[{self.timestamp}] - {self.username} - {self.ipv4_address}')
