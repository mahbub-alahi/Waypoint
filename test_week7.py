from waypoint_core.models import Distance, Trail, Itinerary


def run_tests():
    # 1. Negative distance should fail
    try:
        Distance(-5, "km")
        print("FAIL: Negative distance accepted")
    except ValueError:
        print("PASS: Negative distance rejected")

    # 2. Distance conversion round-trip
    original = Distance(10, "km")
    miles = original.convert()
    back_to_km = miles.convert()

    assert abs(back_to_km.magnitude - 10) < 0.01
    print("PASS: Distance conversion works")

    # 3. Trail from dictionary
    trail_data = {
        "id": 1,
        "name": "Maple Trail",
        "distance": 8,
        "unit": "km",
        "elevation_gain_m": 250,
        "difficulty": "moderate",
    }

    trail1 = Trail.from_dict(trail_data)

    assert trail1.name == "Maple Trail"
    assert trail1.difficulty == "moderate"
    print("PASS: Trail created from dictionary")

    # 4. Invalid difficulty should fail
    try:
        Trail(
            2,
            "Bad Trail",
            Distance(5, "km"),
            100,
            "impossible"
        )
        print("FAIL: Invalid difficulty accepted")
    except ValueError:
        print("PASS: Invalid difficulty rejected")

    # 5. Same ID should compare equal
    trail2 = Trail(
        1,
        "Different Name",
        Distance(20, "km"),
        700,
        "hard"
    )

    assert trail1 == trail2
    print("PASS: Same ID trails compare equal")

    # 6. Itinerary total distance
    trail3 = Trail(
        3,
        "Lake Trail",
        Distance(4, "km"),
        100,
        "easy"
    )

    trail4 = Trail(
        4,
        "Forest Trail",
        Distance(6, "km"),
        200,
        "moderate"
    )

    itinerary1 = Itinerary()
    itinerary1.add_trail(trail1)
    itinerary1.add_trail(trail3)
    itinerary1.add_trail(trail4)

    total = itinerary1.total_distance()

    assert abs(total.magnitude - 18) < 0.01
    print("PASS: Itinerary total is correct")

    # 7. Separate itinerary lists
    itinerary2 = Itinerary()

    assert len(itinerary1.trails) == 3
    assert len(itinerary2.trails) == 0
    print("PASS: Itineraries keep separate trail lists")

    # 8. Default unit affects new trails only
    old_trail = Trail.from_dict({
        "id": 5,
        "name": "Old Trail",
        "distance": 5,
        "elevation_gain_m": 100,
        "difficulty": "easy",
    })

    Trail.change_default_unit("mi")

    new_trail = Trail.from_dict({
        "id": 6,
        "name": "New Trail",
        "distance": 5,
        "elevation_gain_m": 100,
        "difficulty": "easy",
    })

    assert old_trail.distance.unit == "km"
    assert new_trail.distance.unit == "mi"
    print("PASS: Default unit affects new trails only")

    print("\nAll Week 7 tests passed successfully!")


if __name__ == "__main__":
    run_tests()