from datetime import datetime
from display import Display

class CarPark:
    displays: list[Display]
    def __init__(self, location, capacity, _plates=None, _displays=None):
        self.location = location
        self.displays = _displays or []
        self.capacity = capacity
        self.plates = _plates or []

    @property
    def available_bays(self):
        return max(0, self.capacity - len(self.plates))

    def register(self, component):
        if not isinstance(component, Display):
            raise TypeError("Object needs to be a Sensor or Display")
        elif isinstance(component, Display):
            self.displays.append(component)

    def add_car(self, plate: str):
        if plate not in self.plates:
            self.plates.append(plate)
        self.update_displays()

    def remove_car(self, plate: str):
        if plate in self.plates:
            self.plates.remove(plate)
        else:
            raise(ValueError)
        self.update_displays()

    def update_displays(self):
        current_datetime = datetime.now()
        data = {"Available Bays": self.available_bays, "Current Temperature": 41, "Current Time": current_datetime}
        for display in self.displays:
            display.update(data)

    def __str__(self):
        return f"{self.location} Car Park - {self.capacity - len(self.plates)} bays available"