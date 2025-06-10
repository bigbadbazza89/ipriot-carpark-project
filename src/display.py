class Display():
    def __init__(self, id, message, is_on):
        self.id = id
        self.message = "Welcome to the City of Moondalup!"
        self.is_on = True

    def __str__(self):
        return f"{self.id}: {self.message}"
