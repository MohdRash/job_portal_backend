from django.contrib import admin

from student.models import Specialization, Student, StudentOtherDetail
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','fees_paid')

admin.site.register(Student,StudentAdmin)
admin.site.register(StudentOtherDetail)
admin.site.register(Specialization)
