from django.db import models
import uuid 
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your models here.
class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fees_paid = models.BooleanField(default = False)
    application_submitted = models.BooleanField(default = False)
    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.user.username
        
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance) 

class StudentOtherDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(Student,related_name='student_other_detail', on_delete=models.CASCADE)
    address = models.CharField(max_length=140,null=True,blank=True)
    dob = models.DateField(max_length=30,null=True,blank=True)
    phone = models.CharField(max_length=10, null=True,blank=True)
    profilepic = models.ImageField(upload_to='Profile_pic' ,null= True,blank=True)
    cv = models.FileField(upload_to ='cv',null=True,blank=True)
    company_cv = models.FileField(upload_to ='company_cv',null=True,blank=True)

    linkedin_username = models.CharField(max_length=30, null=True,blank=True)
    linkedin_password = models.CharField(max_length=30, null=True,blank=True)


    university = models.CharField(max_length=140,null=True,blank=True)
    course_campus = models.CharField(max_length=140,null=True,blank=True)
    course_title = models.CharField(max_length=140,null=True,blank=True)
    course_start_date = models.DateField(max_length=30,null=True,blank=True)
    course_end_date = models.DateField(max_length=30,null=True,blank=True)
    course_duration = models.IntegerField(null=True)

    company_name = models.CharField(max_length=140,null=True,blank=True)
    working_type = models.CharField(max_length=140,null=True,blank=True)
    work_duration = models.IntegerField(null=True)

    contract_submit_date = models.DateField(max_length=30,null=True,blank=True)
    expr_certi_submit_date = models.DateField(max_length=30,null=True,blank=True)
    visa_expiry_date = models.DateField(max_length=30,null=True,blank=True)
    
    first_job_sector = models.CharField(max_length=50,null=True,blank=True)
    second_job_sector = models.CharField(max_length=50,null=True,blank=True)
    third_job_sector = models.CharField(max_length=50,null=True,blank=True)

    first_job_role = models.CharField(max_length=50,null=True,blank=True)
    second_job_role = models.CharField(max_length=50,null=True,blank=True)
    third_job_role = models.CharField(max_length=50,null=True,blank=True)

    first_job_role_reason = models.TextField(null=True,blank=True)
    second_job_role_reason = models.TextField(null=True,blank=True)
    third_job_role_reason = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'student_other_detail'

    def __str__(self):
        return self.student.user.username


class Specialization(models.Model):
    STATUS_CHOICES= [
        ('passed','Passed'),
        ('not_assigned_yet','Not Assigned yet'),
        ('ongoing','Ongoing'),
        ('failed','Failed'),
        ('submitted',"Submitted"),
        ('not_selected','Not selected')]

    id = models.AutoField(primary_key=True)
    student_other_detail =  models.ForeignKey(StudentOtherDetail,related_name='specialization',on_delete=models.CASCADE)

    title = models.CharField(max_length=50,null=False,blank=False)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES, null=False,blank=False)
    description = models.CharField(max_length=140,null=True,blank=True)

    class Meta:
        db_table = 'specilizations'

    def __str__(self):
        return self.title
