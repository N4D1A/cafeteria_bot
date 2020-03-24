# !/usr/bin/env pythona
# encoding=utf-8

import telegram
import requests
import time
from bs4 import BeautifulSoup
import telegram
from IPython.display import Image
import os
from apscheduler.schedulers.blocking import BlockingScheduler

###########################
##### 텔레그램 봇 생성 #####
###########################

###########################
###########################
## 봇 및 채널 생성해 봇 토큰과 채널 ID 얻은 후에는 아래 코드 진행 필요 없음

#bot = telegram.Bot(token='911941490:AAFmFEInh1DCYwZK8A5iFk1r2-U6UIcXls8')

# 생성한 텔레그램 봇 정보
#me = bot.getMe()
#print(me)

# 텔레그램에서 생성한 텔레그램 봇 /start 시작하기
# 그런 다음, 사용자 id 받아오기

#chat_id = bot.getUpdates()[-1].message.chat.id
#print('user id:', chat_id)

# 사용자 id로 메시지 보내기
#bot.sendMessage(chat_id, 'Hello!')

# 텔레그램에서 채널 생성하고, 위에서 생성한 봇을 관리자로 등록하기
# 채널에서 메시지 보내보기
# 그런 다음, 채널 id 받아오기
# https://api.telegram.org/bot봇토큰대체/getUpdates 에서 확인

#channel_id = -1001385432319
#bot.sendMessage(channel_id, 'bot의 메시지: Hello!')

###########################
###########################


#########################
##### 웹 크롤러 구현 #####
#########################

bot = telegram.Bot(token='911941490:AAFmFEInh1DCYwZK8A5iFk1r2-U6UIcXls8')
channel_id = -1001385432319

# 스케줄러 생성
scheduler = BlockingScheduler()

# 기존 url 저장 리스트
oldUrl = [1,2]

# 학생식당 메뉴페이지 기본 주소
base_1 = 'https://www.gist.ac.kr/kr/html/sub05/050601.html'
base_2 = 'https://www.gist.ac.kr/kr/html/sub05/050602.html'

def send_links():
    send_menu1(base_1) # 1학생식당
    send_menu2(base_2) # 2학생식당


def send_menu1(base):
    url = base
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    post = soup.find('div', {'class':'bd_item_box'})
    subQuary = post.find('a').attrs['href']
    subUrl = url + subQuary

    if oldUrl[0] == subUrl: # 기존 링크와 같은지 비교
        bot.sendMessage(channel_id, '아직 제 1 학생식당의 신규 주간 메뉴가 등록되지 않았습니다. 한 시간 뒤 다시 확인합니다.')
        #scheduler.resume_job(job_id='alarm_resend_1') # 재전송 스케줄러 등록
        scheduler.resume_job(job_id='test1') # 재전송 스케줄러 등록
        return

    oldUrl[0] = subUrl # 새 링크를 기존 링크 리스트에 할당
    title = post.find('h2').text
    subRes = requests.get(subUrl)
    subHtml = subRes.text
    subSoup = BeautifulSoup(subHtml, 'html.parser')
    subPost = subSoup.find('div', {'class':'bd_detail_content'})
    subImage = subPost.find('img').attrs['src']

    with open('./menu.png','wb') as file: # 이미지링크를 이미지로 저장
        resp = requests.get(subImage)
        file.write(resp.content)

    bot.sendPhoto(chat_id = channel_id, photo = open('./menu.png','rb'), caption = title) # 메뉴이미지 송부

    os.remove('./menu.png') # 저장이미지 삭제

    #scheduler.pause_job(job_id='alarm_resend_1') # 재전송 스케줄러 실행 정지
    scheduler.pause_job(job_id='test1') # 재전송 스케줄러 실행 정지


def send_menu2(base):
    url = base
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    post = soup.find('div', {'class':'bd_item_box'})
    subQuary = post.find('a').attrs['href']
    subUrl = url + subQuary

    if oldUrl[1] == subUrl: # 기존 링크와 같은지 비교
        bot.sendMessage(channel_id, '아직 제 2 학생식당의 신규 주간 메뉴가 등록되지 않았습니다. 한 시간 뒤 다시 확인합니다.')
        #scheduler.resume_job(job_id='alarm_resend_2')
        scheduler.resume_job(job_id='test2') # 재전송 스케줄러 등록
        return

    oldUrl[1] = subUrl # 새 링크를 기존 링크 리스트에 할당
    title = '제2학생식당 주간식단표:' + post.find('h2').text
    subRes = requests.get(subUrl)
    subHtml = subRes.text
    subSoup = BeautifulSoup(subHtml, 'html.parser')
    subPost = subSoup.find('div', {'class':'bd_detail_content'})
    subImage = subPost.find('img').attrs['src']

    with open('./menu.png','wb') as file: # 이미지링크는 이미지로 저장
        resp = requests.get(subImage)
        file.write(resp.content)

    bot.sendPhoto(chat_id = channel_id, photo = open('./menu.png','rb'), caption = title) # 메뉴이미지 송부

    os.remove('./menu.png') # 저장이미지 삭제

    #scheduler.pause_job(job_id='alarm_resend_2') # 재전송 스케줄러 실행 정지
    scheduler.pause_job(job_id='test2') # 재전송 스케줄러 실행 정지


def test(base):
    bot.sendMessage(channel_id, '다시보내기 테스트: ' + base)

# 스케줄러 세팅 및 적용

get_jobs = scheduler.get_jobs()
print_jobs = scheduler.print_jobs()
bot.sendMessage(channel_id, str(get_jobs))
bot.sendMessage(channel_id, str(print_jobs))

#scheduler.add_job(send_links, 'cron', day_of_week=0, hour=9, minute=30, second=0, id='alarm_basic')
# scheduler.add_job(send_menu1, "cron", args=[base_1], hour='*/1', id='alarm_resend_1')
# scheduler.add_job(send_menu2, "cron", args=[base_2], hour='*/1', id='alarm_resend_2')
# scheduler.pause_job(job_id='alarm_resend_1')
# scheduler.pause_job(job_id='alarm_resend_2')
scheduler.add_job(send_links, 'cron', day_of_week=1, minute='*/5', second=0, id='alarm_basic')
scheduler.add_job(test, "cron", args=[base_1], minute='*/1', id='test1')
scheduler.add_job(test, "cron", args=[base_2], minute='*/1', id='test2')
scheduler.pause_job(job_id='test1')
scheduler.pause_job(job_id='test2')

scheduler.start()
