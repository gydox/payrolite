from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main.urls')), 
    path('', include('authentication.urls')), 
    path('employee/', include('employee.urls')), 
    path('payroll/', include('payroll.urls')), 

]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

