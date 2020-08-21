from selenium import webdriver
import bs4
import json
import urllib.request as r
import traceback
import time
from datetime import date, datetime, timedelta
import re
import unicodedata
#please, open this program everyday
class population:
    

    onlineLink = "https://forum.gamer.com.tw/index.php?c=400"
    mobileLink = "https://forum.gamer.com.tw/index.php?c=94"
    webGameLink = "https://forum.gamer.com.tw/index.php?c=80"
    PCGameLink = "https://forum.gamer.com.tw/index.php?c=40"
    consoleLink = "https://forum.gamer.com.tw/index.php?c=52"
    #initialization
    def __init__(self):
        pass
    
    def usingDriver(self,url):
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(url)
        time.sleep(1)
        return driver

    #extraction of data
    def getSoup(self,url):
        #return bs4 object of this website
        #using selenium
        try:
            d = self.usingDriver(url)
            soup = bs4.BeautifulSoup(d.page_source,"html.parser")
            return soup
        except Exception:
            print("some error is occured in getSoup function")
            #tb = traceback.format_exc()
            #print(f"\n{tb}")
            print(Exception)
            return 0
    def getFormDiv(self,url):
        #get <div id=data-container>
        soup = self.getSoup(url)
        form = soup.find(id="data-container")
        return form
    def getNameIDRank(self,iter):
        tmpStorage = []
        li = iter.find(class_="forum_list_title").find_all("span") #rank,gameId,gameName
        tmpStorage.append(int(li[0].getText()))

        title = re.split("\s$",li[1].getText())[0]
        tmpStorage.append(title)

        gameId = li[1].find("a").get("href")
        gameId = re.findall("\d+",gameId)[0]
        tmpStorage.append(int(gameId))
        return tmpStorage
    def getPopulationAndThread(self,iter):
        numRegex = "[\s]\d+[\s]"
        txt = re.findall(numRegex,iter.getText())
        txt = self.strtoInt(txt)
        return txt
    def strtoInt(self,li):
        li = [unicodedata.normalize("NFKC",line) for line in li] #change \u3000 to std space
        for i in range(len(li)):
            li[i] = int(li[i])
        return li
    def getData(self,url):
        #return list of dictionary
        #{"gameName":str,"gameId":int,"rank":int,"population":int,"newThread":int}
        #grap data every ? minutes
        storage = []
        form = self.getFormDiv(url)
        for i in form.find_all(class_="forum_list"):
            data = {}

            li = self.getNameIDRank(i)
            txt = self.getPopulationAndThread(i)
            data["name"] = li[1]
            data["gameID"] = li[2]
            data["rank"] = li[0]
            data["population"] = txt[len(txt)-2]
            data["newThread"] = txt[len(txt)-1]
            storage.append(data)   
        return storage

    def getDataDate(self):
        #since the website is updated at 1200nn
        #the date should be adjusted
        #e.g. if the program is run at next day, it should return yesterday date5
        time = datetime.now()
        if time.hour < 12:
            d = timedelta(days = 1)
            time = time - d
        return str(time.date())

    def isIdentical(self,fileName,towrite):
        #check whether the json file should be updated
        #no need to update if time is equal to system time
        #also, the first 2 set of data (id, population and new thread) should be equal
        #return boolean value
        time = self.getDataDate()
        with open(f"data/{fileName}","r",encoding="utf-8") as f:
            j = json.load(f)
            if len(j["content"]) == 0:
                print("the file is newly created(isIdentical function)")
                return False
            if j["content"][len(j["content"]) - 1]["date"] == towrite["date"]:
                print("already exist(isIdentical function), no need to update")
                return True
        return False

    def writetoJson(self,url,typeName,fileName):
        #write to json only if there's new change to the file itself
        #call the checkIdentical function
        towrite = {}
        dic = self.getData(url)
        towrite["date"] = self.getDataDate()
        towrite["data"] = dic
        try:
            with open(f"data/{fileName}","r+",encoding="utf-8") as f:
                data = json.load(f)
        except: #if the file is newly created
            with open(f"data/{fileName}","w",encoding="utf-8") as f:
                data = {"type":typeName,"content":[]}
                json.dump(data,f)
        data["content"].append(towrite)
        if not self.isIdentical(fileName,towrite):
            try:
                with open(f"data/{fileName}","w",encoding="utf-8") as f:
                    json.dump(data,f,ensure_ascii=False)
                    print(f"Successfully updated {fileName}")
            except Exception:
                print(Exception)

    #debug
    def printJsonInfo(self,fileName,dateObj,numberToPrint = 0):
        d = str(dateObj)
        try:
            with open(f"data/{fileName}","r+",encoding="utf-8") as f:
                data = json.load(f)
            print(f"{fileName}:")
            for i in data["content"]:
                if(d == i["date"]):
                    if numberToPrint == 0 or numberToPrint > 30:
                        for j in i["data"]:
                            print(j)
                    else:
                        for ctr in range(numberToPrint):
                            print (i["data"][ctr])
        except Exception:
            traceback.format_exc()
            print("There's some error in the json file")
        



    def mainLoop(self):
        self.writetoJson(self.mobileLink,"mobile-game","mobile.json")
        self.writetoJson(self.onlineLink,"online-game","online.json")
        self.writetoJson(self.consoleLink,"console-game","console.json")
        self.writetoJson(self.webGameLink,"web-game","web.json")
        self.writetoJson(self.PCGameLink,"pc-game","pc.json")

    def checkJsonForEach(self,dateObj,numberToPrint = 0):
        li = ["mobile.json","online.json","console.json","web.json","pc.json"]
        for i in li:
            self.printJsonInfo(i,dateObj,numberToPrint)
        

tStart = time.time()
d = date.today()
p = population()
p.mainLoop()
p.checkJsonForEach(d,3)
p.getData(p.consoleLink)
tEnd = time.time()
print(f"Total running time: {tEnd-tStart:.3f}")