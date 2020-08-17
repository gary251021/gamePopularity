from selenium import webdriver
import bs4
import json
import urllib.request as r
import traceback
import time

class population:
    

    onlineLink = "https://forum.gamer.com.tw/index.php?c=400"
    mobileLink = "https://forum.gamer.com.tw/index.php?c=94"
    webGameLink = "https://forum.gamer.com.tw/index.php?c=80"
    PCGameLink = "https://forum.gamer.com.tw/index.php?c=40"
    consoleLink = "https://forum.gamer.com.tw/index.php?c=52"
    def __init__(self):
        pass
    
    def usingDriver(self,url):
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(url)
        time.sleep(1)
        return driver
    def getSoup(self,url):
        #return bs4 object of this website
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
    def getData(self,url):
        #return python dictionary
        #grap data every ? minutes
        soup = self.getSoup(url)
        form = soup.find(id="data-container")
        print(form)

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
    def mainLoop(self):
        pass

"""url = "https://worstit9.github.io/index.html"
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
time.sleep(1)
soup = bs4.BeautifulSoup(driver.page_source)"""
p = population()
p.getData(p.onlineLink)