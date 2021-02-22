from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django_application import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    path('geocoding_excel',views.geocoding_excel,name='geocoding_excel'),
    path('admin/', admin.site.urls),
]
