from django.contrib import admin
from django.urls import path, include
from api.views import PeakAPIView, ZoneAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('peak/', PeakAPIView.as_view()),
    path('zone/', ZoneAPIView.as_view()),
    path('api-auth/', include('rest_framework.urls'))  # Adds 'Login' link in the top right of the page
]
