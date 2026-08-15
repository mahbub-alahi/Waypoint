from django.shortcuts import render
from .models import Trail


def catalog(request):
    park_name = request.GET.get("park", "")

    trails = Trail.objects.filter(is_open=True)

    if park_name:
        trails = trails.filter(park__name__icontains=park_name)

    trails = trails.order_by("distance_km")

    return render(
        request,
        "catalog.html",
        {
            "trails": trails,
            "park_name": park_name,
        }
    )