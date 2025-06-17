from importlib.metadata import entry_points

from car_park import CarPark
from abc import ABC, abstractmethod
import random

class Sensor(ABC):
    def __init__(self, sensor_id: int, car_park: CarPark, is_active: bool):
        self.id = sensor_id
        self.is_active = is_active
        self.car_park = car_park

    def _scan_plate(self):
        return f"FAKE-{random.randint(0, 9999): 04d}"

    def detect_vehicle(self):
        plate = self._scan_plate()
        self.update_car_park(plate)

    @abstractmethod
    def update_car_park(self, plate):
        pass


    def __str__(self):
        return f"Sensor {self.id}: In {self.car_park}, Active: { self.is_active}"


class EntrySensor(Sensor):
    def update_car_park(self, plate):
        self.car_park.add_car(plate)
        print(f"Inbound Vehicle Detected. Plate: {plate}")

class ExitSensor(Sensor):
    def update_car_park(self, plate):
        self.car_park.remove_car(plate)
        print(f"Outbound Vehicle Detected. Plate: {plate}")

    def _scan_plate(self):
        return random.choice(self.car_park.plates)