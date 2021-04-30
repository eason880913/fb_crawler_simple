#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on  Oct 14 19:53:20 2020

@author: eason880913
"""
import os
from selenium import webdriver
import time
import os, shutil, errno, time, datetime #, sys, subprocess
import re
from bs4 import BeautifulSoup as bs
import sys
from test import single_info

driver_path = '/Users/eason880913/Desktop/work/fb_crawler/Internet-Observation-Station/chromedriver'
FB_email = 'z3211021@yahoo.com.tw'
FB_password = 'EASON880913'

with open ('Mc.csv','a') as f:
    f.write(f"postid,post_time,main_text,pic_url,pic_num,vide_url,讚,愛心,加油,哈,哇,嗚,怒,comment_num,share_num\n")

def start_driver(driver_path):
    '''
    Open Chrome, turn off notification window, and log in FB
    
    Parameter:
        driver_path = the path of chromedriver
    '''
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--max_old_space_size')    
    chrome_options.add_experimental_option("prefs",prefs) # turn of notification window\
    driver = webdriver.Chrome(driver_path, options=chrome_options)#用chrome開啟

    #進到ＦＢ登入頁面
    driver.get('https://www.facebook.com')
    driver.find_element_by_id('email').send_keys(FB_email)#找到元素 輸入帳號
    driver.find_element_by_id('pass').send_keys(FB_password)#找到元素 輸入密碼
    driver.find_element_by_name('login').click()#按下登入按鈕
    return driver

driver = start_driver(driver_path)
time.sleep(1)
driver.refresh()
time.sleep(1)

#mbasic crawler urls
driver.get('https://m.facebook.com/asusclub.tw/?ref=page_intern')
time.sleep(1)
for i in range(30):
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(2)
soup=bs(driver.page_source,'lxml')
url = soup.select('[class="_52jc _5qc4 _78cz _24u0 _36xo"] a')

for i in url:        
    # print('https://mbasic.facebook.com/'+i['href'])
    url = 'https://mbasic.facebook.com/'+i['href']

    # video mode
    # url = 'https://mbasic.facebook.com/story.php?story_fbid=5219552801420695&id=101615286547831&__tn__=-R'
    postid = re.sub('https.*story_fbid=|\&id=.*','',url)
    try:
        driver.get(url)
        time.sleep(2)
        soup1 = bs(driver.page_source,'lxml')
        post_time = re.sub('·.*','',soup1.select('[class="be bf"]')[1].text)
        main_text = soup1.select('[class="bp"]')[0].text
        main_text = re.sub(',','，',main_text)
        pic_raw = soup1.select('[style="width:205px; height:205px;"] a')
        pic_urls = {}
    
        for picu in pic_raw:
            purl = 'https://mbasic.facebook.com/'+picu['href']
            driver.get(purl)
            time.sleep(1)
            soup11 = bs(driver.page_source,'lxml')
            pic_urls[purl] = soup11.select('[class="_1g06"]')[0].text
        pic_num = len(pic_urls)
        pic_url = ''
        for j in pic_urls:
            pic_url = pic_url + str(j)
        vide_url =' '
        if len(pic_url) == 0:
            vide_url = soup1.select('[target="_blank"]')[len(soup1.select('[target="_blank"]'))-1]['href']
            pic_url = ' '
            pic_num = '0'
    except:
        try:
            vide_url = 'https://mbasic.facebook.com/' + soup1.select('[target="_blank"]')[len(soup1.select('[target="_blank"]'))-1]['href']
        except:
            vide_url = 'error'
        pic_url = ' '
        pic_num = '0'

    emotion_url = f"https://mbasic.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier={postid}&refid=52"
    driver.get(emotion_url)
    soup2 = bs(driver.page_source,'lxml')
    emotions = soup2.select('[class="y"] a')
    emo_list = ['0' for i in range(7)]
    for i in range(1,len(emotions)):
        emo_type = re.findall('alt="\w*"',str(emotions[i]))[0]
        if emo_type == 'alt="讚"':
            emo_list[0] = emotions[i].text.replace(',','')
        elif emo_type == 'alt="大心"':
            emo_list[1] = emotions[i].text.replace(',','')
        elif emo_type == 'alt="加油"':
            emo_list[2] = emotions[i].text.replace(',','')
        elif emo_type == 'alt="哈"':
            emo_list[3] = emotions[i].text.replace(',','')
        elif emo_type == 'alt="哇"':
            emo_list[4] = emotions[i].text.replace(',','')
        elif emo_type == 'alt="嗚"':
            emo_list[5] = emotions[i].text.replace(',','')
        elif emo_type == 'alt="怒"':
            emo_list[6] = emotions[i].text.replace(',','')

    new_url = f'https://www.facebook.com/asusclub.tw/posts/{postid}'
    driver.get(new_url)
    time.sleep(5)
    soup3 = bs(driver.page_source,'lxml')
    try:
        comment_num = soup3.select('[class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v knj5qynh m9osqain"]')[0].text.replace(',','')
    except:
        continue
    share_num = soup3.select('[class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v knj5qynh m9osqain"]')[1].text.replace(',','')


    with open ('asus.csv','a') as f:
        f.write(f"{postid},{post_time},{main_text},{pic_url},{pic_num},{vide_url},{','.join(emo_list)},{comment_num},{share_num},{new_url}\n")

# print(share_num,comment_num)
# print(','.join(emo_list))
# print(post_time)
# print(main_text)
# print(vide_url)


driver.close()
