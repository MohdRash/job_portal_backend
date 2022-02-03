from django.shortcuts import render
from main.models import JobApplication
from main.serializers import JobApplicationSerializer, StudentSerializer, StudentSingleViewSerializer

from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from student.models import Student
from rest_framework.response import Response
from  rest_framework import status
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    # queryset = Student.objects.all()
    permission_classes = [IsAdminUser]


    def get_queryset(self):
        # user = self.request.user
        try:
            if self.request.GET['payment']=="paid":
                return Student.objects.filter(fees_paid=True)
            if self.request.GET['payment']=="not_paid":
                return Student.objects.filter(fees_paid=False)
            else:
                return Student.objects.all()
        except:
            return Student.objects.all()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data['fees_paid'] == "True":
            instance.fees_paid = True
            instance.save()
            serializer = self.serializer_class(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        item = self.get_object()
        serializer = StudentSingleViewSerializer(item)
        return Response(serializer.data,status=status.HTTP_200_OK)

class JobApplicationViewSet(ModelViewSet):
    serializer_class = JobApplicationSerializer
    queryset = JobApplication.objects.all()
    permission_classes = [IsAdminUser]