"""This module defines the Sensor class that monitors when a vehicle enters or exits and notifies the car park"""

from importlib.metadata import entry_points

from car_park import CarPark
from abc import ABC, abstractmethod
import random
import time
import sys

class Sensor(ABC):
    def __init__(self, sensor_id: int, car_park: CarPark, is_active: bool, temp=42.7):
        self.id = sensor_id
        self.is_active = is_active
        self.car_park = car_park
        self.car_park.set_temperature(f"{temp}C")

    def _scan_plate(self):
        """Generates fake plate details to simulate a vehicle."""
        return f"FAKE-{random.randint(0, 999):03d}"

    def detect_vehicle(self):
        """Calls the update_car_park method with the plate string."""
        plate = self._scan_plate()
        self.update_car_park(plate)

    @abstractmethod
    def update_car_park(self, plate):
        pass


    def __str__(self):
        return f"Sensor {self.id}: In {self.car_park}, Active: { self.is_active}" # can be used if the Display needs to call the Sensor.


class EntrySensor(Sensor):
    def update_car_park(self, plate):
        """Tells the car park to add the plate to its list of plates."""
        self.car_park.add_car(plate)

class ExitSensor(Sensor):
    def update_car_park(self, plate):
        """Tells the car park to remove the plate from its list of plates."""
        self.car_park.remove_car(plate)

    def _scan_plate(self):
        """Picks a plate at random from the list to remove."""
        return random.choice(self.car_park.plates)