from django.shortcuts import get_object_or_404, render
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


def detail(request, trail_id):
    trail = get_object_or_404(Trail, id=trail_id)

    return render(
        request,
        "trail_detail.html",
        {
            "trail": trail
        }
    )