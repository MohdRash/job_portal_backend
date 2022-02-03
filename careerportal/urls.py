from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/student/', include('student.urls', namespace='student_api')),
    path('api/v1/account/', include('account.urls', namespace='account_api')),
    path('api/v1/main/', include('main.urls', namespace='main_api')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)