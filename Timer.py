from datetime import date, datetime, timedelta
class Timer:
	def __init__(self):
		self._today = datetime.now()
		

	@property
	def today(self):
		if self._today.hour < 12:
			d = timedelta(days = 1)
			self._today = self._today - d
		return str(self._today.date())



d = Timer()
print(d.today)