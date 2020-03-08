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
    
##네이버 스마트 스토어
def fetch_smartstore(url):

    bot_token =  config.TELEGRAM_CONFIG['bot_token']  
    bot_channelid = config.TELEGRAM_CONFIG['channel_id']
    bot = telegram.Bot(token=bot_token)  
    arr = [] 
    try:
        start = time.time()
        isSoldout = False
        context = ssl._create_unverified_context()
        soup = BeautifulSoup(urlopen(url,timeout=10, context=context), "html.parser")
        contents = soup.find('form')
        
        children = contents.find_all('p')  
        p = [a.get_text() for a in children]
        for val in p: 
            if val == "이 상품은 현재 구매하실 수 없는 상품입니다.":
                isSoldout = True      
                if(arr.count(val)>0):
                    arr.remove(val)
        if (isSoldout == False):   
            if(arr.count(url) == 0):
                arr.append(url)
                bot.send_message(chat_id=bot_channelid, text="**재 고 풀 림**\n "+url).chat_id
                print(p)
    except Exception as e:
        print ('naver error '+e)
 

def run_naver(): 
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        while(True):
            executor.map(fetch_smartstore,crawl.urls_smartstore_list) 
            time.sleep(10)
            if(_FINISH):
                break