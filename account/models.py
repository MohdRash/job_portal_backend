from django.db import models
import uuid 
from django.contrib.auth.models import User

class OtpVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10, null=True,blank=True)
    count = models.IntegerField(default=5)
    class Meta:
        db_table = 'otp_verification'
    def __str__(self):
        return self.otp
        