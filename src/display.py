import time

class Display:
    def __init__(self, display_id: int, message: str, is_on=True):
        self.id = display_id
        self.message = message
        self.is_on = is_on

    def slow_print(self, text, delay=0.1):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
            self.slow_print(f"{key}: {value}")
            time.sleep(1)

    def __str__(self):
        return f"{self.id}: {self.message}"
