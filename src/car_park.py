from pathlib import Path
from datetime import datetime
from display import Display
import json


class CarPark:
    def __init__(self, location, capacity, _plates=None, _displays=None, log_file=Path("log.txt"), config_file=Path("config.json")):
        self.location = location
        self.displays = _displays or []
        self.capacity = capacity
        self.plates = _plates or []
        self.log_file = log_file if isinstance(log_file, Path) else Path(log_file)
        self.config_file = Path(config_file) if not isinstance(config_file, Path) else config_file
        self.log_file.touch(exist_ok=True)

    @property
    def available_bays(self):
        return max(0, self.capacity - len(self.plates))

    @classmethod
    def from_config(cls, config_file=Path("config.json")):
        config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        with config_file.open() as f:
            config = json.load(f)
        return cls(config["location"], config["capacity"], log_file=config["log_file"])

    def register(self, component):
        if not isinstance(component, Display):
            raise TypeError("Object needs to be a Sensor or Display")
        elif isinstance(component, Display):
            self.displays.append(component)

    def add_car(self, plate: str):
        if plate not in self.plates:
            self.plates.append(plate)
        self.update_displays()
        self._log_car_activity(plate, "entered")

    def remove_car(self, plate: str):
        if plate in self.plates:
            self.plates.remove(plate)
        else:
            raise(ValueError)
        self.update_displays()
        self._log_car_activity(plate, "exited")

    def update_displays(self):
        current_datetime = datetime.now()
        data = {"Available Bays": self.available_bays, "Current Temperature": 41, "Current Time": current_datetime}
        for display in self.displays:
            display.update(data)

    def _log_car_activity(self, plate, action):
        with self.log_file.open("a") as f:
            f.write(f"{plate} {action} at {datetime.now()}\n")

    def write_config(self):
        with self.config_file.open("w") as f:
            json.dump({"location": self.location,
                       "capacity": self.capacity,
                       "log_file": str(self.log_file)}, f)

    def __str__(self):
        return f"{self.location} Car Park - {self.capacity - len(self.plates)} bays available"