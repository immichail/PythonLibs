from bs4 import BeautifulSoup as bs
import requests as req
from threading import Thread
import re

class ProxySearcher:
    
    def __init__(self, url = "http://spys.one/proxies/", type = "http", destination = "http://www.google.com", timeout = 2, MIN_IN_POOL = 2):
        self.url = url
        self.type = type
        self.poolRaw = []
        self.poolVal = []
        self.mask = r"\d+\.\d+\.\d+\.\d+"
        self.destination = destination
        self.timeout = timeout
        self.current_proxy = -1
        self.MIN_IN_POOL = MIN_IN_POOL
        self.repooler = None
        return

    def getValue(self, s, d):
        l = s.split('^')[0]
        r = s.split("^")[1]

        return int(l) ^ d[r]

    def getPortValue(self, v):

        l = v.split("^")[0]
        r = v.split("^")[1]

        return self.table[l] ^ self.table[r]

    def getCodeTable(self, sp):
        queries = sp.body.select("script")[2].text.split(";")
        self.table = { s.split("=")[0]: s.split("=")[1] for s in queries if s != ""}
        for k, v in self.table.items():
            if (v.find("^") == -1):
                self.table[k] = int(v)
        
        for k, v in self.table.items():
            if (type(v) is str):
                if (v.find("^") > -1):
                    self.table[k] = self.getValue(v, self.table)
        
        return

    def checkProxy(self, proxy):

        try:
            proxies = {
                "http": proxy,
                "https": proxy
            }
            req.get(self.destination, timeout = self.timeout, proxies = proxies)
            print("ProxySearcher::checkProxy - proxy ", proxy, " working")
            return True
        except:
            print("ProxySearcher::checkProxy - proxy ", proxy, " is unavailable")
            return False

        return False

    def getProxiesFromURL(self, url = None):
        if (url == None):
            url = self.url
        page = req.get(url)
        page_bs = bs(page.content)
        self.getCodeTable(page_bs)
        #proxies = page_bs.find_all("tr")
        proxy_list = page_bs.select("tr.spy1xx")
        for proxy in proxy_list:
            cols = proxy.select("td")
            address_col = cols[0]
            address = cols[0].text
            address_match = re.findall(self.mask, address)
            if (address_match):
                address = address_match[0]
            else:
                address = None
            port = ""
            if (len(address_col.select("script")) > 0):
                port_string = address_col.select("script")[0].text.split("+")[1:]
                port_string = [p.replace("(", "").replace(")", "") for p in port_string]
                port_string = [str(self.getPortValue(p)) for p in port_string]
                port_string = "".join(port_string)
                port = port_string
            
            if (address):
                address = ":".join([address, port])
                if (not(address in self.pool))and(not(address in self.poolVal)):
                    self.pool.append(address)

        return

    def createPool(self):
        print("ProxySearch::createPool - Creating new proxy pool")
        self.pool = []
        #self.poolVal = []
        #print(self.getProxiesFromURL(self.url + "1/"))
        self.getProxiesFromURL(self.url)
        for i in range(5):
            self.getProxiesFromURL(self.url + str(i) + "/")

        for proxy in self.pool:
            if (self.checkProxy(proxy)):
                self.poolVal.append(proxy)
            self.pool.remove(proxy)
        return

    def next(self):
        if (self.current_proxy == -1):
            self.current_proxy = 0
            return self.poolVal[self.current_proxy]
        else:
            self.current_proxy += 1
            
            print("Currently available ", len(self.poolVal) - self.current_proxy)
            #check how many proxies left
            if (self.current_proxy >= len(self.poolVal) - self.MIN_IN_POOL):
                #self.createPool()
                self.repooler = Thread(target = self.createPool)
                self.repooler.start()

            if (self.current_proxy >= len(self.poolVal)):
                print("Waiting for repooler...")
                self.repooler.join()
                return self.next()
            else:
                return self.poolVal[self.current_proxy]
        return None



ps = ProxySearcher(timeout = 1, destination="http://api.telegram.org/bot986035515:AAGbQkEbgoYO8Nbpj_Nkc3HreH8uIDUgY8c/getMe")
ps.createPool()

print(ps.next())
print(ps.next())
print(ps.next())