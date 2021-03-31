from abc import abstractmethod
from packages.file_management.file_reader import DBReader
from packages.helper.timer import Timer
from packages.helper.string_modifier import StringModifier

from pymongo import MongoClient
import json

class FileWriter:
	"""
	This class corespond to any action that will write data into the database/json file
	"""
	def __init__(self,category_name):
		self.today = Timer().today
		self.category_name = category_name

	@abstractmethod
	def write_to_storage(self,data):
		pass

	@abstractmethod
	def remove_from_storage(self,date):
		pass
	@abstractmethod
	def pop_from_storage(self):
		pass


class JsonWriter(FileWriter):
	def __init__(self,file_name):
		super().__init__(file_name)
		
		try:
			self.current_data = self.open_and_load()			
		except: #if the file is newly created
			self.fp =  open(f"data/{self.category_name}","w",encoding="utf-8")
			self.current_data = {"type":StringModifier.remove_extension_name(self.category_name),"content":[]}
			self.fp.close
			
	def open_and_load(self):
		self.fp = open(f"data/{self.category_name}","r+",encoding="utf-8")
		loaded =  json.load(self.fp)
		self.fp.close
		return loaded

	def write_to_storage(self,data):
		self.fp = open(f"data/{self.category_name}","w",encoding="utf-8")
		toappend = {"date": self.today,"data":data}
		self.current_data["content"].append(toappend)		
		json.dump(self.current_data,self.fp,ensure_ascii=False)

		self.fp.close


	def remove_from_storage(self,date):
		pass

	def pop_from_storage(self):
		'''
		remove and return the last entry
		'''
		self.current_data = self.open_and_load()
		last = self.current_data["content"].pop()
		#write back to the json
		self.fp = open(f"data/{self.category_name}","w",encoding="utf-8")
		json.dump(self.current_data,self.fp,ensure_ascii=False)
		self.fp.close
		return last
		


class DBWriter(FileWriter):
	def __init__(self, category_name,uri):
		super().__init__(category_name)
		self.uri = uri
		self.client = MongoClient(uri)
		self.db = self.client.gamePopularityDB    #the thing after self.client is the name of the database

	def copy_from_json(self):
		"""
		if there some document exist in the json one but not in mongodb, get the data from json and write to it
		"""
		j = JsonWriter(self.category_name + ".json")
		j = j.open_and_load()
		dr = DBReader(self.category_name,self.uri)
		for one_day_data in j["content"]:
			#if some of them are inserted, ignore it
			date_obj = Timer.get_date_object(one_day_data["date"])
			
			if dr.check_duplicate(date_obj):
				print(f"The data in {str(date_obj)} is already in the database")
			else:
				self.write_to_storage(date_obj,one_day_data["data"])


	def write_to_storage(self,date,data):
		toappend = {"date": date,"data":data}
		result = self.db[self.category_name].insert_one(toappend)      #insert one into the collection name
		#print("result id: "+ str(result.inserted_id))

