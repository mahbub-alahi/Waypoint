from abc import ABC, abstractmethod


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

    def _check_unit(self, other):
        if not isinstance(other, Distance):
            raise TypeError("Operand must be a Distance object.")

        if self.unit != other.unit:
            raise ValueError("Distance units must match.")

    def __add__(self, other):
        self._check_unit(other)
        return Distance(
            self.magnitude + other.magnitude,
            self.unit
        )

    def __sub__(self, other):
        self._check_unit(other)

        result = self.magnitude - other.magnitude

        if result < 0:
            raise ValueError("Distance cannot be negative.")

        return Distance(result, self.unit)

    def __eq__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented

        if self.unit != other.unit:
            return False

        return abs(
            self.magnitude - other.magnitude
        ) < 0.0001

    def __lt__(self, other):
        self._check_unit(other)
        return self.magnitude < other.magnitude

    def __gt__(self, other):
        self._check_unit(other)
        return self.magnitude > other.magnitude

    def __str__(self):
        return f"{self.magnitude:.2f} {self.unit}"

    def __repr__(self):
        return (
            f"Distance({self.magnitude}, "
            f"'{self.unit}')"
        )


class Trail(ABC):
    """Abstract base class representing a trail."""

    default_unit = "km"

    allowed_difficulties = {
        "easy",
        "moderate",
        "hard",
        "expert"
    }

    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty
    ):
        if not isinstance(distance, Distance):
            raise TypeError(
                "distance must be a Distance object."
            )

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
        unit = data.get(
            "unit",
            cls.default_unit
        )

        if not cls.is_valid_unit(unit):
            raise ValueError("Invalid unit.")

        distance = Distance(
            data["distance"],
            unit
        )

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
            raise ValueError(
                "Invalid default unit."
            )

        cls.default_unit = unit

    def __eq__(self, other):
        if not isinstance(other, Trail):
            return NotImplemented

        return self.id == other.id

    @abstractmethod
    def estimated_time(self):
        pass

    @abstractmethod
    def summary(self):
        pass


class ElevationMixin:
    def grade_percent(self):
        if self.distance.magnitude == 0:
            return 0

        distance_m = (
            self.distance.magnitude * 1000
        )

        return (
            self.elevation_gain_m
            / distance_m
        ) * 100

    def mixin_name(self):
        return "ElevationMixin"


class RatingMixin:
    def __init__(
        self,
        *args,
        rating=0.0,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.rating = rating

    def average_rating(self):
        return self.rating

    def mixin_name(self):
        return "RatingMixin"


class DayHike(Trail):
    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty
    ):
        super().__init__(
            trail_id,
            name,
            distance,
            elevation_gain_m,
            difficulty
        )

    def estimated_time(self):
        return self.distance.magnitude / 4.0

    def summary(self):
        return (
            f"Day hike: {self.name} - "
            f"{self.distance}"
        )


class BackpackingRoute(Trail):
    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty
    ):
        super().__init__(
            trail_id,
            name,
            distance,
            elevation_gain_m,
            difficulty
        )

    def estimated_time(self):
        return self.distance.magnitude / 3.0

    def summary(self):
        return (
            f"Backpacking route: "
            f"{self.name} - "
            f"{self.distance}"
        )


class TrailRun(Trail):
    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty
    ):
        super().__init__(
            trail_id,
            name,
            distance,
            elevation_gain_m,
            difficulty
        )

    def estimated_time(self):
        return self.distance.magnitude / 8.0

    def summary(self):
        return (
            f"Trail run: {self.name} - "
            f"{self.distance}"
        )


class GuidedDayHike(DayHike):
    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty,
        guide_name
    ):
        super().__init__(
            trail_id,
            name,
            distance,
            elevation_gain_m,
            difficulty
        )

        self.guide_name = guide_name

    def summary(self):
        base_summary = super().summary()

        return (
            f"{base_summary} | "
            f"Guide: {self.guide_name}"
        )


class RatedDayHike(
    RatingMixin,
    ElevationMixin,
    DayHike
):
    pass


class Itinerary:
    """Represents an ordered collection of trails."""

    def __init__(self):
        self._trails = []

    @property
    def trails(self):
        return tuple(self._trails)

    def add_trail(self, trail):
        if not isinstance(trail, Trail):
            raise TypeError(
                "Only Trail objects can be added."
            )

        self._trails.append(trail)

    def total_distance(self):
        if not self._trails:
            return Distance(
                0,
                Trail.default_unit
            )

        target_unit = (
            self._trails[0].distance.unit
        )

        total = 0

        for trail in self._trails:
            distance = trail.distance

            if distance.unit != target_unit:
                distance = distance.convert()

            total += distance.magnitude

        return Distance(
            total,
            target_unit
        )