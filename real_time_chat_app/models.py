from django.db import models
# from timezone_field import TimeZoneField
from django.contrib.auth.models import User
from django.utils import timezone

class UserMessages(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="send_message")
    message = models.TextField()
    time_stamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username
    
class GroupName(models.Model):
    name = models.CharField(max_length=50)
    user = models.ManyToManyField(User)
    def __str__(self):
        return self.name
    