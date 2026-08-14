from django.shortcuts import render


def home(request):
    context = {
        "greeting": "Welcome to Waypoint!"
    }
    return render(request, "home.html", context)


def report(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        trail = request.POST.get("trail", "")
        note = request.POST.get("note", "")

        context = {
            "name": name,
            "email": email,
            "trail": trail,
            "note": note,
        }

        return render(request, "thank_you.html", context)

    return render(request, "report.html")


def search(request):
    query = request.GET.get("q", "")

    context = {
        "query": query
    }

    return render(request, "search.html", context)


def catalog(request):
    trails = [
        {
            "name": "Bruce Trail",
            "distance": 12.4,
            "elevation": 320,
            "difficulty": "moderate",
            "is_open": True,
        },
        {
            "name": "Rouge Valley Trail",
            "distance": 8.7,
            "elevation": 180,
            "difficulty": "easy",
            "is_open": True,
        },
        {
            "name": "Algonquin Ridge",
            "distance": 15.2,
            "elevation": 540,
            "difficulty": "hard",
            "is_open": False,
        },
        {
            "name": "Niagara Escarpment",
            "distance": 10.6,
            "elevation": 410,
            "difficulty": "expert",
            "is_open": True,
        },
        {
            "name": "High Park Loop",
            "distance": 5.3,
            "elevation": 90,
            "difficulty": "easy",
            "is_open": True,
        },
        {
            "name": "Scarborough Bluffs Trail",
            "distance": 7.9,
            "elevation": 230,
            "difficulty": "moderate",
            "is_open": False,
        },
    ]

    return render(request, "catalog.html", {"trails": trails})