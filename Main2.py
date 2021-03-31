'''
use datareader object to read the http response's json data
write to json/ database by the filewriter object

when initializing the program, also allow check game's data (FileReader)

'''
from packages.file_management.file_writer import *
from packages.file_management.file_reader import *
from packages.helper.timer import Timer
from data_reader import DataReader

import config


ONLINE = 400
MOBILE = 94
WEBGAME = 80
PC = 48
CONSOLE = 52



list_to_read = {"online":400,"mobile":94,"web":80,"pc":48,"console":52}
additional_list = {"acg":22,"themes":61,"others":95}
def fetch_all(pages):	
	for category in additional_list:
		d = DataReader(additional_list[category],category,pages)
		d.start_request()
		JsonWriter(str(category+".json")).write_to_storage(d.datas)
		DBWriter(category,config.db_uri).write_to_storage(Timer().today,d.datas)
	
	for category in list_to_read:
		d = DataReader(list_to_read[category],category,pages)
		d.start_request()
		JsonWriter(str(category+".json")).write_to_storage(d.datas)
		DBWriter(category,config.db_uri).write_to_storage(Timer().today,d.datas)

def copy_all():
	for category in additional_list:
		w = DBWriter(category,config.db_uri)
		w.copy_from_json()
		print(f"{category} is sucessfully inserted")
	

	for category in list_to_read:
		w = DBWriter(category,config.db_uri)
		w.copy_from_json()
		print(f"{category} is sucessfully inserted")

if __name__ == "__main__":
	fetch_all(2)

	
	





