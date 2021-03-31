import re
class StringModifier:
	def __init__(self):
		pass

	@staticmethod
	def remove_end_space(str):
		if str[-1] == " ":
			return str[:-1]
		return str

	@staticmethod
	def remove_extension_name(str):
		'''
		can be called only if the things after the dot is the extension name
		e.g. cars.model.json, return cars
		'''
		try:
			return str[:re.search("\..*$",str).span()[0]]
		except AttributeError:
			print(f"no extension name in {str}")
			return str
			





