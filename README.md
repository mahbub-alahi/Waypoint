class Distance:
    """Represents a distance in kilometers or miles."""

    KM_TO_MI = 0.621371
    MI_TO_KM = 1.60934

    def __init__(self, magnitude, unit):
        if magnitude < 0:
            raise ValueError("Distance cannot be negative.")

        if unit not in ("km", "mi"):
            raise ValueError("Unit must be 'km' or 'mi'.")

        self._magnitude = float(magnitude)
        self._unit = unit

    @property
    def magnitude(self):
        return self._magnitude

    @property
    def unit(self):
        return self._unit

    def convert(self):
        if self._unit == "km":
            return Distance(self._magnitude * self.KM_TO_MI, "mi")

        return Distance(self._magnitude * self.MI_TO_KM, "km")


class Trail:
    """Represents a trail."""

    default_unit = "km"
    allowed_difficulties = {"easy", "moderate", "hard", "expert"}

    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty
    ):
        if not isinstance(distance, Distance):
            raise TypeError("distance must be a Distance object.")

        self.id = trail_id
        self.name = name
        self.distance = distance
        self.elevation_gain_m = elevation_gain_m
        self._difficulty = None

        self.set_difficulty(difficulty)

    @property
    def difficulty(self):
        return self._difficulty

    def set_difficulty(self, difficulty):
        if not self.is_valid_difficulty(difficulty):
            raise ValueError("Invalid difficulty.")

        self._difficulty = difficulty

    @staticmethod
    def is_valid_difficulty(difficulty):
        return difficulty in Trail.allowed_difficulties

    @staticmethod
    def is_valid_unit(unit):
        return unit in ("km", "mi")

    @classmethod
    def from_dict(cls, data):
        unit = data.get("unit", cls.default_unit)

        if not cls.is_valid_unit(unit):
            raise ValueError("Invalid unit.")

        distance = Distance(data["distance"], unit)

        return cls(
            trail_id=data["id"],
            name=data["name"],
            distance=distance,
            elevation_gain_m=data["elevation_gain_m"],
            difficulty=data["difficulty"]
        )

    @classmethod
    def change_default_unit(cls, unit):
        if not cls.is_valid_unit(unit):
            raise ValueError("Invalid default unit.")

        cls.default_unit = unit

    def __eq__(self, other):
        if not isinstance(other, Trail):
            return NotImplemented

        return self.id == other.id


class Itinerary:
    """Represents an ordered collection of trails."""

    def __init__(self):
        self._trails = []

    @property
    def trails(self):
        return tuple(self._trails)

    def add_trail(self, trail):
        if not isinstance(trail, Trail):
            raise TypeError("Only Trail objects can be added.")

        self._trails.append(trail)

    def total_distance(self):
        if not self._trails:
            return Distance(0, Trail.default_unit)

        target_unit = self._trails[0].distance.unit
        total = 0

        for trail in self._trails:
            distance = trail.distance

            if distance.unit != target_unit:
                distance = distance.convert()

            total += distance.magnitude

        return Distance(total, target_unit)