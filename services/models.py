from django.db import models

# -----------------------------------
# Office Model
# -----------------------------------
class Office(models.Model):
    office_name = models.CharField(max_length=100)
    district = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "offices"

    def __str__(self):
        return self.office_name


# -----------------------------------
# Document Model
# -----------------------------------
class Document(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "documents"

    def __str__(self):
        return self.name


# -----------------------------------
# Service Model
# -----------------------------------
class Service(models.Model):
    title = models.CharField(max_length=255)
    is_popular = models.BooleanField(default=False)
    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        related_name="services"
    )

    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=20, null=True, blank=True)
    photo_url = models.CharField(max_length=500, null=True, blank=True)

    service_type = models.CharField(
        max_length=50,
        choices=[
            ("Online", "Online"),
            ("Offline", "Offline"),
            ("Offline/Online", "Offline/Online"),
        ],
        default="Offline"
    )
    processing_time = models.CharField(max_length=100, null=True, blank=True)
    validity = models.CharField(max_length=100, null=True, blank=True)
    documents = models.ManyToManyField(
        Document,
        through='ServiceDocument',
        related_name='services',
        blank=True
    )

    class Meta:
        db_table = "services"

    def __str__(self):
        return self.title


# -----------------------------------
# ServiceDocument (through table)
# -----------------------------------
class ServiceDocument(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    class Meta:
        db_table = "service_documents"

    def __str__(self):
        return f"{self.document.name} ({self.service.title})"


# -----------------------------------
# ServicePhoto Model
# -----------------------------------
class ServicePhoto(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=500, null=True, blank=True)
    caption = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "service_photos"

    def __str__(self):
        return f"Photo for {self.service.title}"
