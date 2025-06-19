import unittest
import json
from pathlib import Path
from car_park import CarPark
from sensor import EntrySensor
from display import Display

class TestCarPark(unittest.TestCase):
      def setUp(self):
          self.test_log_file = Path("new_log.txt")
          self.car_park = CarPark("123 Example Street", 100, log_file=self.test_log_file)

      def test_car_park_initialized_with_all_attributes(self):
         self.assertIsInstance(self.car_park, CarPark)
         self.assertEqual(self.car_park.location, "123 Example Street")
         self.assertEqual(self.car_park.capacity, 100)
         self.assertEqual(self.car_park.plates, [])
         self.assertEqual(self.car_park.displays, [])
         self.assertEqual(self.car_park.available_bays, 100)
         self.assertEqual(self.car_park.log_file, Path("new_log.txt"))

      def test_add_car(self):
         self.car_park.add_car("FAKE-001")
         self.assertEqual(self.car_park.plates, ["FAKE-001"])
         self.assertEqual(self.car_park.available_bays, 99)

      def test_remove_car(self):
         self.car_park.add_car("FAKE-001")
         self.car_park.remove_car("FAKE-001")
         self.assertEqual(self.car_park.plates, [])
         self.assertEqual(self.car_park.available_bays, 100)

      def test_overfill_the_car_park(self):
         for i in range(100):
            self.car_park.add_car(f"FAKE-{i}")
         self.assertEqual(self.car_park.available_bays, 0)
         self.car_park.add_car("FAKE-100")
         # Overfilling the car park should not change the number of available bays
         self.assertEqual(self.car_park.available_bays, 0)

         # Removing a car from an overfilled car park should not change the number of available bays
         self.car_park.remove_car("FAKE-100")
         self.assertEqual(self.car_park.available_bays, 0)

      def test_removing_a_car_that_does_not_exist(self):
         with self.assertRaises(ValueError):
            self.car_park.remove_car("NO-1")

      def test_register_raises_type_error(self):
          with self.assertRaises(TypeError):
              self.car_park.register("Not a Sensor or Display")

      def test_register_display_succeeds(self):
          self.car_park.register(Display(12, "Have a great day!"))
          self.assertTrue(self.car_park.displays)

      def test_register_sensor_fails(self):
          with self.assertRaises(TypeError):
              self.car_park.register(EntrySensor(15, self.car_park, True))

      def test_log_file_created(self):
          self.assertTrue(Path("new_log.txt").exists())

      def tearDown(self):
          Path("new_log.txt").unlink(missing_ok=True)

      def test_car_logged_when_entering(self):
          self.car_park.add_car("NEW-001")
          with self.car_park.log_file.open() as f:
              last_line = f.readlines()[-1]
          self.assertIn("NEW-001", last_line)  # check plate entered
          self.assertIn("entered", last_line)  # check description
          self.assertIn("\n", last_line)  # check entry has a new line

      def test_car_logged_when_exiting(self):
          self.car_park.add_car("NEW-001")
          self.car_park.remove_car("NEW-001")
          with self.car_park.log_file.open() as f:
              last_line = f.readlines()[-1]
          self.assertIn("NEW-001", last_line)  # check plate entered
          self.assertIn("exited", last_line)  # check description
          self.assertIn("\n", last_line)  # check entry has a new line

      def test_write_config_in_json(self):
          config_path = Path("testing_config.json")
          self.car_park.config_file = config_path
          self.car_park.write_config()
          self.assertTrue(config_path.exists())

          with config_path.open() as f:
              config_data = json.load(f)

          self.assertEqual(config_data["location"], "123 Example Street")
          self.assertEqual(config_data["capacity"], 100)
          self.assertEqual(config_data["log_file"], str(self.test_log_file))

          config_path.unlink(missing_ok=True)


if __name__ == "__main__":
   unittest.main()