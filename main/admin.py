from django.contrib import admin

from main.models import JobApplication

# Register your models here.

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('student','date','company','position','job_description','stage')
admin.site.register(JobApplication,JobApplicationAdmin)