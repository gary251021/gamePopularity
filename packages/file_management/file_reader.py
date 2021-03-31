from abc import abstractmethod
from packages.helper.string_modifier import StringModifier
from packages.helper.timer import Timer
import json
class FileReader:
	'''
	This class corespond to any operation on reading the specific data in the database/json file, 
	calling any function will not modify any data stored
	'''
	def __init__(self,file_name):
		self.file = StringModifier.remove_extension_name(file_name)

	@abstractmethod
	def check_duplicate(self):
		pass

	@abstractmethod
	def read_today_data(self):
		pass

	@abstractmethod
	def read_certain_date_data(self):
		pass

class JsonReader(FileReader):
	def __init__(self,file_name):
		self.file = file_name
		self.fp =  open(f"data/{self.file_name}","r",encoding="utf-8")
		self.loaded = json.load(self.fp)
		self.fp.close


	def check_duplicate(self):
		pass

	def read_today_data(self):
		pass

	def read_certain_date_data(self):
		pass

class DBReader(FileReader):
	def __init__(self,file_name):
		super().__init__(file_name)

	def check_duplicate(self):
		pass

	def read_today_data(self):
		pass

	def read_certain_date_data(self):
		pass