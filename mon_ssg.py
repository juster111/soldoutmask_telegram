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
##SSG 계열사
def fetch_ssg(url): 
    
    bot_token =  config.TELEGRAM_CONFIG['bot_token']  
    bot_channelid = config.TELEGRAM_CONFIG['channel_id']
    bot = telegram.Bot(token=bot_token)  
    arr = [] 
    try:
        start = time.time()
        isSoldout = False 
        context = ssl._create_unverified_context()
        soup = BeautifulSoup(urlopen(url,timeout=10, context=context), "html.parser")
        contents = soup.find("div",{"class":"cdtl_row_top"})
        children = contents.find_all('span')  

        p = [a.get_text() for a in children]    
        for val in p: 
            if "품절" in val:
                isSoldout = True      
                if(arr.count(val)>0):
                    arr.remove(val)
        if (isSoldout == False):       
            if(arr.count(url) == 0):
                arr.append(url)    
                bot.send_message(chat_id=bot_channelid, text="**재 고 풀 림**\n "+url).chat_id
                print(p)
        
    except Exception as e:
        print ('ssg error ' + e)
     

 


def run_ssg():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        while(True):
            for val in crawl.urls_ssg_list: 
                executor.submit(fetch_ssg,val)
                time.sleep(0.1) 
            if(_FINISH):
                break