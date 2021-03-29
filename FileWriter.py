from abc import abstractmethod


class FileWriter:
	def __init__(self,data):
		pass

	@abstractmethod
	def write_to_storage(self):
		pass


class JsonWriter(FileWriter):
	def __init__(self, data):
		super().__init__(data)


class DBWriter(FileWriter):
	def __init__(self, data):
		super().__init__(data)