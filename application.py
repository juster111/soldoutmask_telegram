 
import threading 
import mon_etc
import mon_ppomppu
import mon_ssg
import mon_naver
import json
import time
from datetime import datetime 
from requests import get
import telegram  
import config
bot_token = config.TELEGRAM_CONFIG['bot_token']  
bot = telegram.Bot(token=bot_token)  


naver = threading.Thread(target=mon_naver.run_naver)
ssg = threading.Thread(target=mon_ssg.run_ssg)
welkeeps = threading.Thread(target=mon_etc.run_welkeeps)
ppomppu = threading.Thread(target=mon_ppomppu.run_ppomppu) 

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
bot.sendMessage(chat_id = "658472331", text="시작 합니다.") 
ppomppu.start() 
naver.start()
welkeeps.start()
ssg.start()
while(True):
    bot.sendMessage(chat_id = "658472331", text=("%s 현재 재고 상태 상품 %s 개 동시 확인 처리 하고 있습니다" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),threading.active_count())) )
    time.sleep(1*60 * 5)
    
def stop():
    mon_ppomppu.stop()
    mon_naver.stop()
    mon_etc.stop()
    mon_ssg.stop()
    bot.sendMessage(chat_id = "658472331", text="종료 합니다.") 

# 아래 코드는 봇으로 채팅이 전달 오면 상태값/시작/종료를 핸들링하려 했으나 
# getupdates가 어느순간 갱신되지 않은 상태가 보여 우선 주석 처리 합니다. 
#    
# updates = bot.getUpdates()
# latest = bot.getUpdates()[-1].message.message_id
# for u in updates: 
#     print(u.message)
# while(True): 
#     for u in updates: 
#         try: 
#             print ("latest = %s , id= %s" %(latest, u.message.message_id) )
#             if(latest < u.message.message_id): 
#                 print('?????????????')
#                 print(latest)
#                 latest = u.message.message_id    
#                 if('시작' in u.message.text and '658472331' == str(u.message.chat.id)):
#                     bot.sendMessage(chat_id = "658472331", text="시작 합니다.")
#                     run()
#                 if('상태조회' in u.message.text):
#                     bot.sendMessage(chat_id = str(u.message.chat.id), text=("현재 재고 상태 상품 %s 개 동시 확인 처리 하고 있습니다" % (threading.active_count())) )
#                 if('종료' in u.message.text and '658472331' == str(u.message.chat.id)):
#                     bot.sendMessage(chat_id = str(u.message.chat.id), text="시작 합니다.\n [상태조회] 입력시 상태 확인 가능 합니다.")
#                     stop()
#         except Exception as e:
#             print(e)
#             print(latest)
#             # continue
#     time.sleep(2)
 
