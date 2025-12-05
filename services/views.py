from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Service, Office, ServicePhoto, SavedService

# =============================
# HOME PAGE
# =============================
def home(request):
    services = Service.objects.filter(is_popular=True)[:6]
    offices = Office.objects.all()

    return render(request, "services/index.html", {
        "services": services,
        "offices": offices,
    })


# =============================
# SERVICE DETAIL PAGE
# =============================
def service_detail(request, id):
    service = get_object_or_404(Service, id=id)

    # Documents (ManyToMany)
    documents = service.documents.all()

    # Photos
    photos = ServicePhoto.objects.filter(service=service)

    # Check if user has saved this service
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedService.objects.filter(user=request.user, service=service).exists()

    return render(request, "services/service_detail.html", {
        "service": service,
        "documents": documents,
        "photos": photos,
        "is_saved": is_saved,
    })


# =============================
# OFFICE DETAIL PAGE
# =============================
def office_detail(request, id):
    office = get_object_or_404(Office, id=id)
    services = office.services.all()

    return render(request, "services/office_detail.html", {
        "office": office,
        "services": services,
    })


# =============================
# SEARCH ENDPOINT
# =============================
def search(request):
    q = request.GET.get("q", "").strip().lower()
    results = []

    if not q:
        return JsonResponse(results, safe=False)

    # Services Search
    for s in Service.objects.all():
        if q in s.title.lower():
            results.append({
                "type": "service",
                "id": s.id,
                "name": s.title,
            })

    # Offices Search
    for o in Office.objects.all():
        if q in o.office_name.lower():
            results.append({
                "type": "office",
                "id": o.id,
                "name": o.office_name,
            })

    return JsonResponse(results, safe=False)


# =============================
# SAVE / UNSAVE SERVICE AJAX
# =============================
@login_required
def save_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    saved, created = SavedService.objects.get_or_create(user=request.user, service=service)
    status = "saved" if created else "already_saved"
    return JsonResponse({"status": status})


@login_required
def unsave_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    deleted, _ = SavedService.objects.filter(user=request.user, service=service).delete()
    status = "removed" if deleted else "not_saved"
    return JsonResponse({"status": status})
    

from django.shortcuts import render

def google_login_only(request):
    return render(request, "services/login_google_only.html")