###############################################################

##################################
### EXPONENTIAL MOVING AVERAGE ###
##################################


class exponentially_weighted_moving_average:
    def __init__(self, updateWeight=0.7, prevWeight=0.3, length=20):
        self.updateWeight = updateWeight
        self.prevWeight = prevWeight
        self.keepLength = length
        self.history = []
        if self.updateWeight + self.prevWeight != 1:
            raise RuntimeError("Total weight greater than 1")

    def setLength(self, length):
        self.keepLength = length

    def setUpdateWeight(self, weight):
        self.updateWeight = weight
        self.prevWeight = 1 - weight

    def setPrevWeight(self, weight):
        self.prevWeight = prevWeight
        self.updateWeight = 1 - weight

    def clear(self):
        self.history = []

    def update(self, reading):
        value = (reading * self.updateWeight) + ((sum(self.history) / len(self.history)) * self.prevWeight)
        while len(self.history) >= self.keepLength:
            self.history.pop(0)
        self.history.append(reading)
        return value

    def getHistory(self):
        return self.history


###############################################################
