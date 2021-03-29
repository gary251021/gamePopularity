import requests
import time
from fake_useragent import UserAgent
class DataReader:
	timeout_time = 2
	
	def __init__(self,type,req_page):
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
			r = requests.get(self.link,headers=self.headers).json() #get the list
			print(f"game in page {self.page}")
			for game in r:
				print(game["title"] + " " + str(game["ranking"]))
			#r = requests.get("https://forum.gamer.com.tw/ajax/rank.php?c=400&page=1")
			time.sleep(self.timeout_time)# timeout 3 second
			

	@property
	def datas(self):
		return self._datas

	@property
	def link(self):
		return self._link
	
	@link.setter
	def link(self,page):
		self._link = f"https://forum.gamer.com.tw/ajax/rank.php?c={self.type}&page={page}"


d = DataReader(400,3)
d.start_request()
print(s)