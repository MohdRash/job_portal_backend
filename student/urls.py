from django.urls import path
from rest_framework import routers
from .views import *

app_name = 'student'

router = routers.DefaultRouter()
router.register('student-application', StudentApplyView, basename='student-application')
router.register('job-application', JobApplicationReadOnlyViewSet, basename='job-application')


urlpatterns = [
    # path('apply/', StudentApplyView.as_view() ,name= 'apply'),
]
urlpatterns += router.urls 