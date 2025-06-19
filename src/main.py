from car_park import CarPark
from sensor import EntrySensor, ExitSensor
from display import Display
from pathlib import Path
import json

def main():
    car_park = CarPark("moondalup", 100, config_file=Path("moondalup_config.json"))

    car_park.write_config()

    with Path("moondalup_config.json").open() as f:
        config = json.load(f)

    entry_sensor = EntrySensor(1, car_park=car_park, is_active=True)
    exit_sensor = ExitSensor(2, car_park=car_park, is_active=True)
    display = Display(1, "Welcome to Moondalup!", is_on=True)

    car_park.register(display)

    print(display)

    for car in range(10):
        entry_sensor.detect_vehicle()

    for car in range(2):
        exit_sensor.detect_vehicle()

if __name__ == "__main__":
   main()





