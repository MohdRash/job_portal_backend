from django.contrib import admin
from account.models import OtpVerification

class OtpVerificationAdmin(admin.ModelAdmin):
    list_display = ('id','user','count','otp')
admin.site.register(OtpVerification,OtpVerificationAdmin)