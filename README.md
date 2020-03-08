# soldoutmask_telegram

   
this app is watching an specific urls that we should be watching for buying mask   

ssg, naver storefarm, welkeeps, ppomppu 등
사전정의한 품절 페이지들을 크롤링해 품절이 아닌상태가 발견되면, 
특정 텔레그램 채널로 발송 하는 코드 입니다. 

pip install beautifulsoup4

pip install python-telegram-bot --upgrade

pip install requests  
 
    
    #config.py 
    
    'bot_token': '텔레그램봇 토큰',   
    'channel_id': '수신 채널id',    
    'bot_admin_receiver_chatid': '봇생성자 chat id' 

#python application.py
