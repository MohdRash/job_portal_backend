from django.db import models
import uuid

from student.models import Student

class JobApplication(models.Model):
    STAGE_CHOICES= [
        ('applied','Applied'),
        ('declined','Decline'),
        ('pending','Pending'),]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    company = models.CharField(max_length=140,null=False,blank=False)
    position = models.CharField(max_length=140,null=False,blank=False)
    job_description = models.CharField(max_length=140,null=False,blank=False)
    stage = models.CharField(max_length=140,choices=STAGE_CHOICES,blank=False)
    last_date =  models.DateField(null=True,blank=True)


    class Meta:
        db_table = 'job_applications'

    def __str__(self):
        return "{} - {}".format(self.company,self.student.user.username)