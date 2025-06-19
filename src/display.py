import time
import sys

class Display:
    def __init__(self, display_id: int, message: str, is_on=True):
        self.id = display_id
        self.message = message
        self.is_on = is_on

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
            print(f"{key}: {value}", end='', flush=True)
            time.sleep(2)
            sys.stdout.write('\r' + ' ' * 50 + '\r')

    def __str__(self):
        return f"{self.id}: {self.message}"
