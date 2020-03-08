from urllib.request import urlopen
from bs4 import BeautifulSoup
import threading
import crawl 
import time
import telegram 
import concurrent.futures
import datetime
import ssl
import config
from requests import get

_FINISH = False
def stop():
    global _FINISH
    _FINISH = True

## 웰킵스 
def fetch_welkeeps(url): 
    bot_token =  config.TELEGRAM_CONFIG['bot_token']  
    bot_channelid = config.TELEGRAM_CONFIG['channel_id']  
    bot = telegram.Bot(token=bot_token)  
    arr = [] 
    try: 
        start = time.time()
        isSoldout = False   
        
        context = ssl._create_unverified_context()
        soup = BeautifulSoup(urlopen(url,timeout=10, context=context), "html.parser")
        contents = soup.find("div",{"class":"prd-btns"})
        children = contents.find_all('div')    
        p = [a.get_text() for a in children]        
        for val in p:  
            if "SOLD OUT" in val:  
                isSoldout = True      
                if(arr.count(val)>0):
                    arr.remove(val) 
        if (isSoldout == False):     
            if(arr.count(url) == 0):  
                arr.append(url)
                bot.send_message(chat_id=bot_channelid, text="**재 고 풀 림**\n "+url).chat_id
                print(p)
        #print ("'%s\' fetched in %ss" % (url, (time.time() - start)))
    except Exception as e :
        print ('welkeeps error'+ e) 

def run_welkeeps():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        while(True):
            for val in crawl.urls_welkeepsmall: 
                executor.submit(fetch_welkeeps,val)
                time.sleep(0.3)
            time.sleep(10)
            
            if(_FINISH):
                break
        