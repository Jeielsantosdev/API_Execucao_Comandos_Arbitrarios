from django.db import models
import json
# Create your models here.

class Executionlog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    binary = models.CharField(max_length=255)
    command = models.CharField(max_length=255)
    args = models.JSONField(default=dict)
    stdout = models.TextField()
    stderr = models.TextField()
    status_code = models.IntegerField()

    def __str__(self):
        return f"{self.timestamp} | {self.binary} {self.command} | {''.join(self.args)}"