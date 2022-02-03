from django.urls import path
from rest_framework import routers
from .views import *

app_name = 'main'

router = routers.DefaultRouter()
router.register('student-view',StudentViewSet , basename='student-view')
router.register('job-application',JobApplicationViewSet , basename='job-application')
# router.register('upload-company-cv',UploadCompanyCV , basename='job-application')

# urlpatterns = [
#     path('cv/', UploadCompanyCV.as_view() ,name= 'cv'),
# ]

urlpatterns = router.urls 