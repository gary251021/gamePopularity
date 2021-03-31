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

	@staticmethod
	def get_today_object(self):
		return datetime.now().date()


	@staticmethod
	def get_prev_day_string(deltadate):
		return str(Timer.get_prev_day_object(deltadate))
	@staticmethod
	def get_date_object(date):
		"""given the string of the date, return the date object"""
		d = date.split("-")
		return datetime(*(int(i) for i in d))

	@staticmethod
	def get_prev_day_object(deltadate):
		d = timedelta(days = deltadate)
		s = datetime.now() - d 
		return s.date()
		

t = Timer()
print(t.today)
print(Timer.get_prev_day_object(3))
print(Timer.get_prev_day_string(3))
print(Timer.get_date_object("2020-01-01"))

