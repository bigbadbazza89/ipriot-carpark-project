"""This module defines the CarPark class which holds information related to the state of the car park. This information
is provided by the sensor and passed through the displays when vehicles enter and exit."""

from pathlib import Path
from datetime import datetime
from display import Display
import json


class CarPark:
    def __init__(self, location, capacity, _plates=None, _displays=None, log_file=Path("log.txt"), config_file=Path("config.json")):
        self.location = location
        self.displays = _displays or []
        self.capacity = capacity
        self.temperature = None
        self.plates = _plates or []
        self.log_file = log_file if isinstance(log_file, Path) else Path(log_file)
        self.config_file = Path(config_file) if not isinstance(config_file, Path) else config_file
        self.log_file.touch(exist_ok=True)

    def set_temperature(self, temp):
        """sets a default temp value as an attribute from the sensor."""
        self.temperature = temp

    def get_temperature(self):
        return self.temperature

    @property
    def available_bays(self):
        """Holds the state of the number of available bays."""
        return max(0, self.capacity - len(self.plates))

    @classmethod
    def from_config(cls, config_file=Path("config.json")):
        """Pulls the information needed for the car park settings from the config file."""
        config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        with config_file.open() as f:
            config = json.load(f)
        return cls(config["location"], config["capacity"], log_file=config["log_file"])

    def register(self, component):
        """Checks to make sure the component type is a Display object and then adds the display to a list if true."""
        if not isinstance(component, Display):
            raise TypeError("Object needs to be a Display") # will raise if not a Display object.
        elif isinstance(component, Display):
            self.displays.append(component)

    def add_car(self, plate: str):
        """When a car enters the car park, it's plate details are added to the list of plates, sent to the displays and logged."""
        if plate not in self.plates:
            self.plates.append(plate)
        self._log_car_activity(plate, "entered")
        plate = f"Inbound {plate}" # refactor plate variable so that the data library can distinguish when a plate is inbound.
        self.update_displays(plate)


    def remove_car(self, plate: str):
        """When a car leaves the car park, it's plate details are removed from the list of plates, sent to the displays and logged."""
        if plate in self.plates:
            self.plates.remove(plate)
        else:
            raise(ValueError)
        self._log_car_activity(plate, "exited")
        plate = f"Outbound {plate}" # refactor plate variable so that the data library can distinguish when a plate is outbound.
        self.update_displays(plate)


    def update_displays(self, plate):
        """Calls the display to be updated with the current available bays, temp and time when a vehicle enters or exits."""
        current_datetime = datetime.now().replace(microsecond=0)
        data = {"Vehicle": plate , "Available Bays": self.available_bays, "Temperature": self.temperature, "Time": current_datetime}
        for display in self.displays:
            display.update(data)

    def _log_car_activity(self, plate, action):
        """Logs the details of the vehicle entering or exiting."""
        with self.log_file.open("a") as f:
            f.write(f"{plate} {action} at {datetime.now():%Y-%m-%d %H:%M:%S}\n")

    def write_config(self):
        """Adds the provided car park config information as a json supported file."""
        with self.config_file.open("w") as f:
            json.dump({"location": self.location,
                       "capacity": self.capacity,
                       "log_file": str(self.log_file)}, f)

    def __str__(self):
        return f"{self.location} Car Park - {self.capacity - len(self.plates)} bays available" # can be used if the Display has to call the CarPark.