from main.models import JobApplication
from rest_framework import serializers
from student.models import Student,StudentOtherDetail,Specialization
# from student.serializers import StudentOtherDetailSerializer,Specialization
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string

class SpecializationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialization
        # fields = '__all__'
        fields = ['title','status','description']


class StudentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='user.username',read_only = True)

    class Meta:
        model = Student
        # fields = '__all__'
        fields = ['id','student_name','fees_paid','application_submitted']

class StudentOtherDetailSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer(many=True)
    fees_paid = serializers.CharField(source='student.fees_paid',read_only = True)
    student_email = serializers.CharField(source='student.user.email',read_only = True)
    student_name = serializers.CharField(source='student.user.username',read_only = True)
    first_name = serializers.CharField(source='student.user.first_name',read_only = True)
    last_name = serializers.CharField(source='student.user.last_name',read_only = True)
    # fees_paid = serializers.CharField(source='student.fees_paid',read_only = True)
    class Meta:
        model = StudentOtherDetail
        # exclude = ['id']
        fields = '__all__'
        # extra_kwargs = {
		# 	'fees_paid':{'read_only':True},
		# 	'student_email':{'read_only':True},
		# 	'student_name':{'read_only':True}
		# } 

    def create(self, validated_data):
        specializations = validated_data.pop('specialization')
        student_other_detail = StudentOtherDetail.objects.create(**validated_data)
        for specialization in specializations:
            Specialization.objects.create(student_other_detail=student_other_detail, **specialization)
        return student_other_detail






class StudentSingleViewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='user.username',read_only = True)
    student_other_detail = StudentOtherDetailSerializer(read_only =True)
    class Meta:
        model = Student
        # fields = '__all__'
        fields = ['id','student_name','student_other_detail','fees_paid']


class JobApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username',read_only = True)
    class Meta:
        model = JobApplication
        fields = ['id','student','student_name','company','position','job_description','stage','last_date']

        extra_kwargs = {
                'id': {'read_only': True},
                'student_name': {'read_only': True},
        }	


    def create(self,validated_data):
        job_application = JobApplication.objects.create(
            **validated_data,
        )
        student = validated_data['student']
        email = student.user.email

        from_email = "careerportal.in <ecolumsmarketing@gmail.com>"
        subject = "New job Alert"
        # try:
        text_content = ""
        html_context = {
            "position" : job_application.position,
            "company":job_application.company,
            "student_name":student.user.username,
            "last_date":job_application.last_date,
            "website":"https://www.careerportal.com"
        }
        html_content = render_to_string('email/jobalert_email.html', html_context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Email send successfully")
        # except:
        #     print("error")

        return job_application
