from abc import abstractmethod
from packages.helper.timer import Timer
import json

class FileWriter:
	def __init__(self,file_name):
		self.today = Timer().today

	@abstractmethod
	def write_to_storage(self):
		pass


class JsonWriter(FileWriter):
	def __init__(self,file_name):
		super().__init__(file_name)
		self.file_name = file_name
		try:
			self.current_data = self.open_and_load()			
		except: #if the file is newly created
			self.fp =  open(f"data/{self.file_name}","w",encoding="utf-8")
			self.current_data = {"type":file_name,"content":[]}
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

