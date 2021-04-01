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
	def get_today_object():
		return Timer.get_prev_day_object(0)


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
		if datetime.now().hour >= 12:
			d = timedelta(days = deltadate)
		else:
			d = timedelta(days = deltadate + 1)
		s = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) - d 
		return s
		


