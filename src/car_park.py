class CarPark():
    def __init__(self, location, capacity, plates=None, displays=None):
        self.location = location
        self.displays = displays or []
        self.capacity = capacity
        self.plates = plates or []

    def __str__(self):
        return f"{self.location} Car Park - {self.capacity - len(self.plates)} bays available"

cp = CarPark("Moondalup NMT", 100)
print(cp)