import requests
import time
from packages.helper.string_modifier import StringModifier
from packages.helper.timer import Timer
from fake_useragent import UserAgent
class DataReader:
	timeout_time = 0.5
	
	def __init__(self,type,category,req_page):
		self.category = category
		self.ua = UserAgent()
		self.headers = {'User-Agent': self.ua.chrome}
		self.type = type
		self.page = 0
		self._link = f"https://forum.gamer.com.tw/ajax/rank.php?c={type}&page={self.page}"
		self.req_page = req_page
		self._datas = []

	def start_request(self):
		'''
		perform req_page times HTTP request, and store the result in datas variable,
		it will check any data exist to avoid duplicate
		'''
		for current_page in range(1,self.req_page+1):
			self.link = current_page
			response = requests.get(self.link,headers=self.headers).json() #get the list
			print(f"{self.category} in page {current_page}")
			try:
				for game in response:
					self.datas.append(self.get_data_to_write(game))
			except Exception as e:
				#some page return [] as there no any more subpages, or the format returned is different
				print(e)
				raise
			
			time.sleep(self.timeout_time)
			
	def get_data_to_write(self,game):
		'''
		the start_request method will invoke this method to get the dictonary object to write
		'''
		to_write = {} 
		try:			
			to_write["name"] = StringModifier.remove_end_space(game["title"])
			to_write["gameID"] = game["bsn"]
			to_write["rank"] = game["ranking"]
			to_write["population"] = int(game["hot"])
			to_write["newThread"] = int(game["article"])
		except Exception:
			raise KeyError("No valid key found in the json file")
		return to_write

		

	@property
	def datas(self):
		return self._datas

	@property
	def link(self):
		return self._link
	
	@link.setter
	def link(self,page):
		self._link = f"https://forum.gamer.com.tw/ajax/rank.php?c={self.type}&page={page}"


class SyncDataReader(DataReader):
	def __init__(self,type,category,req_page):
		super().__init__(type,category,req_page)

	def get_data_to_write(self, game):
		pass


