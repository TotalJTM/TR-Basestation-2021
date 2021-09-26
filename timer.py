import time
#class that acts as a timer
#timer object should be created, then the timer can be started with start func
#check_timer will return False until timer has expired, where it will return True
class Timer:
	#takes an interval in seconds
	def __init__(self, interval):
		self.interval = interval
		self.start_time = 0

	def start(self):
		self.start_time = time.perf_counter()

	def check_timer(self):
		if (self.start_time+self.interval) <= time.perf_counter():
			return True
		else:
			return False