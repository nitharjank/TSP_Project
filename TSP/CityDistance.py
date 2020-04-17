import math
class CityDistance:
    def __init__(self):
        self.distance = {}
    def append(self, city1, city2):
        #city1_xy = city1[1]
        #city2_xy = city2[1]
        self.distance[(city1[0], city2[0])] = self.computeDistance(city1[1], city2[1])

    def get(self, city1, city2):
        if (city1, city2) in self.distance:
            return self.distance[(city1, city2)]
        if (city2, city1) in self.distance:
            return self.distance[(city2, city1)]

    def computeDistance(self, xCoor, yCoor):
        return int(round(math.sqrt((xCoor[0] - yCoor[0]) ** 2 + (xCoor[1] - yCoor[1]) ** 2)))
    def __str__(self):
        return str(self.distance)  