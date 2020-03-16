###############################################################

############################
### MOVING AVERAGE CLASS ###
############################

class simple_moving_average:
	def __init__(self, length=20):
		self.keepLength = length
		self.history = []

	def setLength(self, length):
		self.keepLength = length

	def clear(self):
		self.history = []

	def update(self, reading):
		while len(self.history) >= self.keepLength:
			self.history.pop(0)
		self.history.append(reading)
		return sum(self.history) / len(self.history)

	def getHistory(self):
		return self.history

###############################################################
