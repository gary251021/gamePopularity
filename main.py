import bs4
import json
import urllib.request as r
import traceback
class population:
    onlineLink = "https://forum.gamer.com.tw/index.php?c=400"
    mobileLink = "https://forum.gamer.com.tw/index.php?c=94"
    webGameLink = "https://forum.gamer.com.tw/index.php?c=80"
    PCGameLink = "https://forum.gamer.com.tw/index.php?c=40"
    consoleLink = "https://forum.gamer.com.tw/index.php?c=52"
    def __init__(self):
        pass
    def mainLoop(self):
        pass

    def getData(self,url):
        #return python dictionary
        #grap data every 240 minutes
        pass

    def checkIdentical(self,fileName,dict):
        #check whether the json file should be updated
        #return boolean value
        pass

    def writetoJson(self,dict,fileName):
        #write to json only if there's new change to the file itself
        #call the checkIdentical function
        pass
    def printInfo(self,link):
        try:
            req = r.Request(link,headers={"User-Agent":"Mozilla/5.0"})
            page = r.urlopen(req).read() 
            soup = bs4.BeautifulSoup(page,'html.parser')
            print(soup.title)
        except:
            print("some error is occured")
            tb = traceback.format_exc()
            print(f"\n{tb}")
        else:
            print("Finished")

p = population()
p.printInfo(p.onlineLink)