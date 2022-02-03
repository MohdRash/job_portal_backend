from django.db.models import fields
from rest_framework import serializers
from student.models import Specialization, StudentOtherDetail
# from main.serializers import StudentSerializer


# class SpecializationSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Specialization
#         # fields = '__all__'
#         fields = ['title','status','description']

# class StudentOtherDetailSerializer(serializers.ModelSerializer):
#     specialization = SpecializationSerializer(many=True)
#     # student_detail = StudentSerializer(read_only =True)
#     class Meta:
#         model = StudentOtherDetail
#         # exclude = ['id']
#         fields = '__all__'
#         extra_kwargs = {
# 			# 'company_cv':{'read_only':True}
# 		} 

#     def create(self, validated_data):
#         specializations = validated_data.pop('specialization')
#         student_other_detail = StudentOtherDetail.objects.create(**validated_data)
#         for specialization in specializations:
#             Specialization.objects.create(student_other_detail=student_other_detail, **specialization)
#         return student_other_detail


