from django.contrib import admin
from django.urls import path, include
from services import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Service app URLs
    path("", views.home, name="home"),
    path("service/<int:id>/", views.service_detail, name="service_detail"),
    path("office/<int:id>/", views.office_detail, name="office_detail"),
    path("search/", views.search, name="search"),

    # AJAX save/unsave
    path("save/<int:service_id>/", views.save_service, name="save_service"),
    path("unsave/<int:service_id>/", views.unsave_service, name="unsave_service"),

    # Login/signup (allauth)
    path("accounts/", include("allauth.urls")),
]