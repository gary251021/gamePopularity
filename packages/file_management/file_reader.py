from abc import abstractmethod
from packages.helper.string_modifier import StringModifier
from packages.helper.timer import Timer

from pymongo import MongoClient
import json
class FileReader:
	'''
	This class corespond to any operation on reading the specific data in the database/json file, 
	calling any function will not modify any data stored
	'''
	def __init__(self,category_name):
		self.category = category_name

	@abstractmethod
	def check_duplicate(self,date_obj):
		pass

	@abstractmethod
	def read_today_data(self,rank):
		pass

	@abstractmethod
	def read_certain_date_data(self,date_obj,rank):
		pass
	
	@abstractmethod
	def read_game_data(self,gameid):
		pass

class JsonReader(FileReader):
	def __init__(self,file_name):
		super().__init__(file_name)
		#load the data in the file
		self.fp =  open(f"data/{self.file_name}","r",encoding="utf-8")
		self.loaded = json.load(self.fp)
		self.fp.close


	def check_duplicate(self,date_obj):
		pass

	def read_today_data(self):
		pass

	def read_certain_date_data(self):
		pass

	def read_game_data(self,gameid):
		pass

class DBReader(FileReader):
	def __init__(self,category_name,uri):
		super().__init__(category_name)
		try:
			self.client = MongoClient(uri)
			self.db = self.client.gamePopularityDB
			self.collection = self.db[self.category]
		except Exception as e:
			print(e)

	def check_duplicate(self,date_obj):
		"""check the data of the coresponding date is inserted or not"""
		result = self.db[self.category].find_one({"date":date_obj})
		if result != None:
			return True #already have inserted data
		return False

	def read_today_data(self,rank = 0):
		
		return self.read_certain_date_data(Timer.get_today_object(),rank)

	def read_certain_date_data(self,date_obj,rank = 0):
		if not isinstance(rank,int):
			raise TypeError("The rank must be an integer")
		elif rank < 0:
			raise ValueError("The rank must be positive")
		


		query = {"date":date_obj}
		projection = {
			"data":1 if rank == 0 else {"$slice":rank},
			"_id":0
		}
		return list(self.collection.find(query,projection))

	def read_game_data(self,gameid):
		#return the game data at come pate, excluding the gameID itself
		query = {"data.gameID":gameid}
		projection = {
			"date":1,
			"data":{"$elemMatch":{"gameID":gameid}},
			"_id":0
			}
		return list(self.collection.find(query,projection))
			
		