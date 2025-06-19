import unittest
import re
from sensor import EntrySensor, ExitSensor
from car_park import CarPark

class TestEntrySensor(unittest.TestCase):
    def setUp(self):
        self.entry_sensor = EntrySensor(sensor_id=12, car_park=CarPark("123 Example Street", 100), is_active=True)  # add assertion here

    def test_entry_sensor_initialized_with_all_attributes(self):
        self.assertIsInstance(self.entry_sensor, EntrySensor)
        self.assertEqual(self.entry_sensor.id, 12)
        self.assertEqual(self.entry_sensor.car_park.location,"123 Example Street")
        self.assertEqual(self.entry_sensor.car_park.capacity, 100)
        self.assertEqual(self.entry_sensor.is_active, True)

    def test_detect_vehicle(self):
        initial_bays = self.entry_sensor.car_park.available_bays
        self.entry_sensor.detect_vehicle()
        plate = self.entry_sensor.car_park.plates[-1]
        updated_bays = self.entry_sensor.car_park.available_bays
        self.assertEqual(updated_bays, initial_bays - 1)
        self.assertRegex(plate, r"^FAKE-\d{3}$")

class TestExitSensor(unittest.TestCase):
    def setUp(self):
        car_park = CarPark("123 Example Street", 100)
        self.plate_to_remove = "FAKE-042"
        car_park.add_car(self.plate_to_remove)
        self.exit_sensor = ExitSensor(sensor_id=12, car_park=car_park, is_active=True)  # add assertion here

    def test_exit_sensor_initialized_with_all_attributes(self):
        self.assertIsInstance(self.exit_sensor, ExitSensor)
        self.assertEqual(self.exit_sensor.id, 12)
        self.assertEqual(self.exit_sensor.car_park.location,"123 Example Street")
        self.assertEqual(self.exit_sensor.car_park.capacity, 100)
        self.assertEqual(self.exit_sensor.is_active, True)

    def test_detect_vehicle(self):
        initial_bays = self.exit_sensor.car_park.available_bays
        self.exit_sensor.detect_vehicle()
        updated_bays = self.exit_sensor.car_park.available_bays
        self.assertEqual(updated_bays, initial_bays + 1)
        self.assertNotIn(self.plate_to_remove, self.exit_sensor.car_park.plates)


if __name__ == '__main__':
    unittest.main()
