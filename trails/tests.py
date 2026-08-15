from django.test import TestCase
from django.urls import reverse

from trails.models import Park, Trail
from waypoint_core.models import Distance


class TrailQueryTests(TestCase):
    def setUp(self):
        self.park = Park.objects.create(
            name="Rouge National Urban Park",
            region="Toronto"
        )

        Trail.objects.create(
            name="Open Trail",
            park=self.park,
            distance_km=5.00,
            elevation_gain=100,
            difficulty="easy",
            is_open=True,
        )

        Trail.objects.create(
            name="Closed Trail",
            park=self.park,
            distance_km=8.00,
            elevation_gain=200,
            difficulty="moderate",
            is_open=False,
        )

    def test_catalog_shows_only_open_trails(self):
        response = self.client.get("/trails/")

        self.assertContains(response, "Open Trail")
        self.assertNotContains(response, "Closed Trail")


class TrailDetailTests(TestCase):
    def test_missing_trail_returns_404(self):
        response = self.client.get("/trails/9999/")
        self.assertEqual(response.status_code, 404)


class DistanceDomainTests(TestCase):
    def test_negative_distance_raises_value_error(self):
        with self.assertRaises(ValueError):
            Distance(-1, "km")