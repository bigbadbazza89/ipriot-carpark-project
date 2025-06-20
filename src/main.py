"""This program simulates a car parking system by which cars are detected entering and exiting.
It provides real-time updates to drivers on how many bays are available and other features such as the temperature and time."""
from car_park import CarPark
from sensor import EntrySensor, ExitSensor
from display import Display
from pathlib import Path
import json

def main():
    """Program creates the necessary Display, Sensor and CarPark instances and simulates
     cars entering and exiting.

     Writes CarPark config to a file in json format.
     """
    car_park = CarPark("moondalup", 100, config_file=Path("moondalup_config.json"))

    car_park.write_config()

    car_park.from_config("moondalup_config.json")

    entry_sensor = EntrySensor(1, car_park=car_park, is_active=True)
    exit_sensor = ExitSensor(2, car_park=car_park, is_active=True)
    display = Display(1, "Welcome to Moondalup!", is_on=True)

    car_park.register(display)

    for car in range(10): # simulates 10 vehicles entering car park.
        entry_sensor.detect_vehicle()

    for car in range(2): # simulates 2 vehicles leaving car park.
        exit_sensor.detect_vehicle()

if __name__ == "__main__":
   main()





