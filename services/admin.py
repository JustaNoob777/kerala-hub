from django.contrib import admin
from .models import Service, Office, Document, ServiceDocument, ServicePhoto

class ServiceDocumentInline(admin.TabularInline):
    model = ServiceDocument
    extra = 1

class ServicePhotoInline(admin.TabularInline):
    model = ServicePhoto
    extra = 1

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "office", "service_type", "processing_time", "validity", "is_popular")
    list_filter = ("office", "service_type", "is_popular")
    search_fields = ("title",)

    list_editable = ("is_popular",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "office", "description", "icon", "photo_url", "is_popular")
        }),
        ("Service Details", {
            "fields": ("service_type", "processing_time", "validity")
        }),
    )

    inlines = [ServiceDocumentInline, ServicePhotoInline]


admin.site.register(Service, ServiceAdmin)
admin.site.register(Office)
admin.site.register(Document)
admin.site.register(ServiceDocument)
admin.site.register(ServicePhoto)