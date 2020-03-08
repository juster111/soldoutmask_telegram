
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
 
## 뽐뿌 
def run_ppomppu():
    
    bot_token =  config.TELEGRAM_CONFIG['bot_token']  
    bot_channelid = config.TELEGRAM_CONFIG['channel_id']
    bot = telegram.Bot(token=bot_token)  
    arr = [] 
    while(True):
        time.sleep(8) 
        url = "http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"
        r= get(url)
        soup = BeautifulSoup(r.content.decode('euc-kr','replace'),"html.parser") 
        contents = soup.find_all('font',{"class":"list_title"})    
        p = [a.get_text() for a in contents] 
        # 한페이지에 20개 출력하므로 최신 세개빼고 삭제.
        del p[3:19] 
        for val in p:        
            if "마스크" in val or "kf94" in val or "kf80" in val:   
                if val not in arr:  
                    arr.append(val) 
                    bot.send_message(chat_id=bot_channelid, text="**확 인 필 요**\n "+val+"\n"+url).chat_id  
                    print(val)
        if(_FINISH):
            break

