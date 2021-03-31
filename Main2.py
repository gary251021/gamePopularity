'''
use datareader object to read the http response's json data
write to json/ database by the filewriter object

when initializing the program, also allow check game's data (FileReader)

'''
from packages.file_management.file_writer import *
from data_reader import DataReader

ONLINE = 400
MOBILE = 94
WEBGAME = 80
PC = 48
CONSOLE = 52

list_to_read = {"online":400,"mobile":94,"web":80,"pc":48,"console":52}
additional_list = {"acg":22,"themes":61,"others":95}
'''
for category in additional_list:
	d = DataReader(additional_list[category],category,2)
	d.start_request()
	JsonWriter(str(category+".json")).write_to_storage(d.datas)
'''
for category in list_to_read:
	d = DataReader(list_to_read[category],category,2)
	d.start_request()
	JsonWriter(str(category+".json")).write_to_storage(d.datas)



