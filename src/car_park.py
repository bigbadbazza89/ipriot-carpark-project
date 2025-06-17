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

    def register(self, component):
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object needs to be a Sensor or Display")
        if isinstance(component, Sensor):
            self.sensors.append(component)
        elif isinstance(component, Display):
            self.displays.append(component)


    def add_car(self, plate: str):
        ...

    def remove_car(self, plate: str):
        ...

    def update_displays(self):
        ...

    def __str__(self):
        return f"{self.location} Car Park - {self.capacity - len(self.plates)} bays available"