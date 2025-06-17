from time import CLOCK_REALTIME
from display import Display
from sensor import Sensor

class CarPark:
    displays: list[Display]
    def __init__(self, location, capacity, _plates=None, _sensors=None, _displays=None):
        self.location = location
        self.displays = _displays or []
        self.capacity = capacity
        self.plates = _plates or []
        self.sensors = _sensors or []

    @property
    def available_bays(self):
        return max(0, self.capacity - len(self.plates))

    def register(self, component):
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object needs to be a Sensor or Display")
        if isinstance(component, Sensor):
            self.sensors.append(component)
        elif isinstance(component, Display):
            self.displays.append(component)

    def add_car(self, plate: str):
        if plate not in self.plates:
            self.plates.append(plate)
        self.update_displays()
        # TODO: What do i do if plate already in the list?

    def remove_car(self, plate: str):
        if plate in self.plates:
            self.plates.remove(plate)
        self.update_displays()
        # TODO: What if the plate isn't there?

    def update_displays(self):
        data = {"Available Bays": self.available_bays, "Current Temperature": 41, "Current Time": CLOCK_REALTIME}
        for display in self.displays:
            display.update(data)

    def __str__(self):
        return f"{self.location} Car Park - {self.capacity - len(self.plates)} bays available"