from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Service, Office, ServiceDocument, ServicePhoto


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

    # Documents (supports old + new M2M setup)
    try:
        documents = service.documents.all()
    except Exception:
        documents = [
            sd.document.name if hasattr(sd, "document") else sd.document_name
            for sd in service.servicedocument_set.all()
        ]

    photos = ServicePhoto.objects.filter(service=service)

    return render(request, "services/service_detail.html", {
        "service": service,
        "documents": documents,
        "photos": photos,
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
# SEARCH ENDPOINT (USED BY HOMEPAGE JS)
# =============================
def search(request):
    q = request.GET.get("q", "").strip().lower()
    results = []

    if not q:
        return JsonResponse(results, safe=False)

    # --- SEARCH SERVICES (TITLE ONLY) ---
    services = Service.objects.all()

    for s in services:
        title = s.title.lower()

        if q in title:
            results.append({
                "type": "service",
                "id": s.id,
                "name": s.title,
            })

    # --- SEARCH OFFICES (NAME ONLY) ---
    offices = Office.objects.all()

    for o in offices:
        name = o.office_name.lower()

        if q in name:
            results.append({
                "type": "office",
                "id": o.id,
                "name": o.office_name,
            })

    return JsonResponse(results, safe=False)