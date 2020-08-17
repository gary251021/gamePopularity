from selenium import webdriver
import bs4
import json
import urllib.request as r
import traceback
import time
from datetime import date
import re
import unicodedata
#please, open this program everydayu
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
        time.sleep(0.5)
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

        link = li[1].find("a").get("href")
        link = re.findall("\d+",link)[0]
        tmpStorage.append(link)

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
            data["population"] = txt[0]
            data["newThread"] = txt[1]
            storage.append(data)          
        return storage

    def checkIdentical(self,fileName,dict):
        #check whether the json file should be updated
        #return boolean value
        pass

    def writetoJson(self,url,typeName,fileName):
        #write to json only if there's new change to the file itself
        #call the checkIdentical function
        towrite = {}
        dic = self.getData(url)
        towrite["date"] = str(date.today())
        towrite["type"] = typeName
        towrite["data"] = dic
        with open(fileName,"a") as f:
            try:
                x = json.dump(towrite,f,ensure_ascii=False)
            except:
                pass

    #debug
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
    def mainLoop(self):
        self.writetoJson(self.mobileLink,"mobile-game","mobile.json")
        self.writetoJson(self.onlineLink,"online-game","online.json")
        self.writetoJson(self.consoleLink,"console-game","console.json")
        self.writetoJson(self.webGameLink,"web-game","web.json")
        self.writetoJson(self.PCGameLink,"pc-game","pc.json")
        

"""url = "https://worstit9.github.io/index.html"
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
time.sleep(1)
soup = bs4.BeautifulSoup(driver.page_source)"""
p = population()
p.mainLoop()
#print(p.getData(p.onlineLink))
