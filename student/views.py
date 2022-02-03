from django.shortcuts import render
from main.models import JobApplication
from main.serializers import JobApplicationSerializer,StudentOtherDetailSerializer
# from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from  rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from student.models import Student, StudentOtherDetail
# from student.serializers import StudentOtherDetailSerializer




# Create your views here.
class StudentApplyView(ModelViewSet):
    serializer_class = StudentOtherDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print("user ",user)
        print("request ",self.request)

        if user.is_superuser:
            return StudentOtherDetail.objects.all()
        else:
            return StudentOtherDetail.objects.filter(student__user=user)
    
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        print("444444444444444444444444")

        student = Student.objects.filter(user = request.user).last()
        print("000000000000000000000")

        request.data['student'] = student.id
        if serializer.is_valid():
            serializer.save()
            student.application_submitted = True
            student.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobApplicationReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return JobApplication.objects.filter(student__user =user)