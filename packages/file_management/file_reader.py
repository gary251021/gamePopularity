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

	def read_certain_date_data(self,date_obj,rank = None):
		if not(rank is None):  #if rank is not none and not int
			if not isinstance(rank,int):
				raise TypeError("The rank must be an integer")
		elif rank < 0:
			raise ValueError("The rank must be positive")
		


		query = {"date":date_obj}
		projection = {
			"data":1 if rank is None else {"$slice":rank},
			"_id":0
		}
		
		return list(self.collection.find(query,projection))

	def read_game_data(self,gameid,return_doc = None):
		#return the game data at come pate
		if not(return_doc is None):
			if not isinstance(return_doc,int):
				raise TypeError("The return_doc must be an integer")
		elif return_doc < 0:
			raise ValueError("The return_doc must be positive")

		query = {"data.gameID":gameid}
		
		projection = {
			"date":1,
			"data":{
				"$filter":{
					"input":'$data',
					"as":"data",
					"cond":{"$eq":["$$data.gameID",gameid]}
				}
			},
			"_id":0
		}
		if return_doc != None:
			l = self.collection.aggregate([
				{"$match":query},
				{"$project":projection},
				{"$sort":{"date":-1}},
				{"$limit":return_doc},
				{"$unwind":"$data"}  #since the array only have 1 element
			])
			return list(l)
		else:
			l = self.collection.aggregate([
				{"$match":query},
				{"$project":projection},
				{"$sort":{"date":-1}},
				{"$unwind":"$data"}  #since the array only have 1 element
			])
			return list(l)
		

	def get_data_higher_than_rank(self,gameid,rank = 500):
		#given a game, see how much date the game have a rank higher than rank
		query = {"data.gameID":gameid}
		
		projection = {
			"date":1,
			"data":{
				"$filter":{
					"input":'$data',
					"as":"data",
					"cond":{"$and":[{"$eq":["$$data.gameID",gameid]},{"$lte":["$$data.rank",rank]}]}
				}
			},
			"_id":0
		}

		l = self.collection.aggregate([
			{"$match":query},
			{"$project":projection},
			{"$sort":{"date":-1}},
			{"$unwind":"$data"}  #since the array only have 1 element
		])
		return list(l)
			


		