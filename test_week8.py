from waypoint_core.models import (
    Distance,
    Trail,
    DayHike,
    BackpackingRoute,
    TrailRun,
    GuidedDayHike,
    RatedDayHike,
)


class FakeTrail:
    def estimated_time(self):
        return 1.25


def run_tests():
    # 1. Distance operator overloading
    d1 = Distance(3, "km")
    d2 = Distance(2, "km")

    assert d1 + d2 == Distance(5, "km")
    assert d1 - d2 == Distance(1, "km")
    assert d2 < d1
    assert d1 > d2

    distances = [
        Distance(5, "km"),
        Distance(1, "km"),
        Distance(3, "km"),
    ]
    distances.sort()

    assert distances[0] == Distance(1, "km")
    print("PASS: Distance operators work")

    # 2. Mixed units should be rejected
    try:
        Distance(3, "km") + Distance(2, "mi")
        print("FAIL: Mixed units were accepted")
    except ValueError:
        print("PASS: Mixed units rejected")

    # 3. Trail should be abstract
    try:
        Trail(
            1,
            "Base Trail",
            Distance(5, "km"),
            100,
            "easy",
        )
        print("FAIL: Abstract Trail was instantiated")
    except TypeError:
        print("PASS: Trail is abstract")

    # 4. Create different trail types
    day_hike = DayHike(
        2,
        "Maple Loop",
        Distance(8, "km"),
        250,
        "moderate",
    )

    backpacking = BackpackingRoute(
        3,
        "Mountain Route",
        Distance(12, "km"),
        600,
        "hard",
    )

    trail_run = TrailRun(
        4,
        "Forest Run",
        Distance(8, "km"),
        150,
        "easy",
    )

    # 5. Polymorphism + duck typing
    mixed_trails = [
        day_hike,
        backpacking,
        trail_run,
        FakeTrail(),
    ]

    print("\nEstimated times:")

    for trail in mixed_trails:
        print(trail.estimated_time())

    assert day_hike.estimated_time() == 2.0
    assert backpacking.estimated_time() == 4.0
    assert trail_run.estimated_time() == 1.0
    print("PASS: Polymorphism and FakeTrail work")

    # 6. GuidedDayHike inheritance and super()
    guided = GuidedDayHike(
        5,
        "Guided Lake Trail",
        Distance(6, "km"),
        180,
        "easy",
        "Alex",
    )

    assert guided.guide_name == "Alex"
    assert "Guide: Alex" in guided.summary()
    print("PASS: GuidedDayHike inheritance works")

    # 7. Mixins and MRO
    rated = RatedDayHike(
        6,
        "Rated Ridge Trail",
        Distance(10, "km"),
        500,
        "hard",
        rating=4.7,
    )

    assert rated.average_rating() == 4.7
    assert rated.grade_percent() == 5.0
    assert rated.mixin_name() == "RatingMixin"

    print("PASS: Mixins work")

    print("\nMRO:")
    print(RatedDayHike.__mro__)

    print("\nAll Week 8 tests passed successfully!")


if __name__ == "__main__":
    run_tests()