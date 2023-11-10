# ECE 547 Group Project


class FieldSensor_class:
    x: float = 0
    y: float = 0
    z: float = 0
    signalRangeRadius: float = 0

    def __init__(self, coord_x, coord_y):
        self.x = coord_x
        self.y = coord_y
        self.z = 0
        self.signalRangeRadius = 0.5

    def position(self) -> tuple:
        return self.x, self.y

    def dispCoordinates(self):
        print(f'[{self.x}, {self.y}, {self.z}]')
