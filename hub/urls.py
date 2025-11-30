from django.contrib import admin
from django.urls import path
from services.views import home, service_detail, office_detail, search

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("service/<int:id>/", service_detail, name="service_detail"),
    path("office/<int:id>/", office_detail, name="office_detail"),
    path("search/", search, name="search"),
]