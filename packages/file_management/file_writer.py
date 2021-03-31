from abc import abstractmethod
from packages.helper.timer import Timer
from packages.helper.string_modifier import StringModifier
import json

class FileWriter:
	"""
	This class corespond to any action that will write data into the database/json file
	"""
	def __init__(self,file_name):
		self.today = Timer().today
		self.file_name = file_name

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
			self.fp =  open(f"data/{self.file_name}","w",encoding="utf-8")
			self.current_data = {"type":StringModifier.remove_extension_name(file_name),"content":[]}
			self.fp.close
			
	def open_and_load(self):
		self.fp = open(f"data/{self.file_name}","r+",encoding="utf-8")
		loaded =  json.load(self.fp)
		self.fp.close
		return loaded

	def write_to_storage(self,data):
		self.fp = open(f"data/{self.file_name}","w",encoding="utf-8")
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
		self.fp = open(f"data/{self.file_name}","w",encoding="utf-8")
		json.dump(self.current_data,self.fp,ensure_ascii=False)
		self.fp.close
		return last
		


class DBWriter(FileWriter):
	def __init__(self, file_name):
		super().__init__(file_name)

	def copy_from_json(self):
		"""
		if there some document exist in the json one but not in mongodb, get the data from json and write to it
		"""
		j = JsonWriter(self.file_name)
		j = j.open_and_load()
		for one_day_data in j["content"]:
			self.write_to_storage(one_day_data)



	def write_to_storage(self,data):
		pass

