class Rat:

    def __init__(self, sex, weight):
        self.sex = sex 
        self.weight = weight
        self.litters = 0

    def __str__(self):
        return f'This {self.sex} rat is {self.weight}g and has breeded {self.litters} times'

    def __repr__(self):
        return f'{self.weight}g'

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __ge__(self, other):
        return self.weight >= other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def getSex(self):
        return self.sex

    def getWeight(self):
        return self.weight

    def setWeight(self, wt):
        self.weight = wt

    def canBreed(self):
        return self.litters < 5
    