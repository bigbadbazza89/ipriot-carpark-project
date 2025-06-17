from time import sleep

class Display:
    def __init__(self, display_id=int, message="Welcome and Thanks For Choosing Us!", is_on=True):
        self.id = display_id
        self.message = message
        self.is_on = is_on

    def update(self, data: dict, delay=0.2):
        for key, value in data.items():
            for c in f"{key}: {value}":
                print(c, end="")
                sleep(delay)
            sleep(delay * 2)
            print(end="\r")



    def __str__(self):
        return f"{self.id}: {self.message}"
