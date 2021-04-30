
import os
from selenium import webdriver
import time
import os, shutil, errno, time, datetime #, sys, subprocess
import re
from bs4 import BeautifulSoup as bs
import sys
from test import single_info
from tqdm import tqdm


driver_path = '/Users/eason880913/Desktop/work/fb_crawler/Internet-Observation-Station/chromedriver'
FB_email = 'z3211021@yahoo.com.tw'
FB_password = 'EASON880913'
number = '4846743088701670'


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

url = f'https://www.facebook.com/story.php?story_fbid={number}&id=101615286547831'
driver.get(url)
time.sleep(10) 
# driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
soup = bs(driver.page_source,'lxml')
                          
driver.find_element_by_css_selector('[class="j83agx80 bkfpd7mw jb3vyjys hv4rvrfc qt6c0cv9 dati1w0a l9j0dhe7"] [class="h3fqq6jp hcukyx3x oygrvhab cxmmr5t8 kvgmc6g5 j83agx80 bp9cbjyn"] [class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l"]').click()
time.sleep(5)
soup = bs(driver.page_source,'lxml')
driver.find_elements_by_css_selector('[class="j83agx80 cbu4d94t buofh1pr l9j0dhe7"] [class="tojvnm2t a6sixzi8 k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y l9j0dhe7 iyyx5f41 a8s20v7p"] [class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 j83agx80 p7hjln8o kvgmc6g5 oi9244e8 oygrvhab h676nmdw pybr56ya dflh9lhu f10w8fjw scb9dxdr i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l bp9cbjyn dwo3fsh8 btwxx1t3 pfnyh3mw du4w35lb"]')[2].click()
time.sleep(5)
for i in range(60):
    try:                                                                                            
        time.sleep(0.5)                                                                                                  
        driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[4]/div/div/div[2]/div[4]/div[1]/div[2]').click()
    except:
        continue
for i in range(500):
    try:                                                                                                                                                                                          
        driver.find_element_by_xpath(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[4]/div/div/div[2]/ul/li[{i}]/div[2]/div/div/div[2]').click()
    except:
        continue
a = input('break')
with open (f'data/mc{number}.txt','w') as f:
    f.write(str(bs(driver.page_source,'lxml')))
driver.close()


def main_comment(soups,datetime_dt):
    ans1 = []
    if 'class="m9osqain j1meafb1 lrazzd5p b2s5l15y j1lvzwm4 kady6ibp"' in str(soups[i]):
        owner = '1'
    else:
        owner = '0'
    ans1.append(owner)

    #那個人的網址
    purl = soups[i].select('[class="oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 q9uorilb mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l"]')[0]['href']
    # print(len(purl))
    purl = re.sub('.comment_id.*','',purl)
    ans1.append(purl)

    #那個人的留言
    try:
        comtext = soups[i].select('[class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql"]')[0].text
        comtext = re.sub('\,','，',comtext)
    except:
        comtext = 'error'
    # print(len(comtext))
    ans1.append(comtext)

    #留言回應心情數
    try:
        comheart = soups[i].select('[class="m9osqain e9vueds3 knj5qynh j5wam9gi jb3vyjys n8tt0mok qt6c0cv9 hyh9befq g0qnabr5"]')[0].text
    except:
        comheart = '0'
    # print(len(comheart))
    ans1.append(comheart)

    #時間
    retime = soups[i].select('[class="_6coi oygrvhab ozuftl9m l66bhrea linoseic"] [class="tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41"]')[0].text
    if '天' in retime:
        retime = re.sub('天','',retime)
        delta = datetime.timedelta(days=int(retime))
        datetime_dt = datetime_dt - delta
        datetime_str = datetime_dt.strftime("%Y/%m/%d")
    elif '週' in retime:
        retime = re.sub('週','',retime)
        delta = datetime.timedelta(days=int(retime)*7)
        datetime_dt = datetime_dt - delta
        datetime_str = datetime_dt.strftime("%Y/%m/%d")
    else:
        datetime_str = 'error'
    ans1.append(datetime_str)
    return ','.join(ans1), purl

def sec_comment(j,datetime_dt):
    ans2 = []
    try:
        secpurl = j.select('[class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8"]')
        secpurl = re.sub('.comment_id.*|\/$','',secpurl[0]['href'])
        ans2.append(secpurl)
    except:
        secpurl=''
        ans2.append(secpurl)
    #留言
    try:
        seccomtext = j.select('[class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql"]')[0].text
    except:
        seccomtext = 'None'
    ans2.append(seccomtext)
    #心情
    try:
        seccomheart = j.select('[class="m9osqain e9vueds3 knj5qynh j5wam9gi jb3vyjys n8tt0mok qt6c0cv9 hyh9befq g0qnabr5"]')[0].text
    except:
        seccomheart = '0'
    ans2.append(seccomheart)
    #時間
    secretime = j.select('[class="tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41"]')[1].text
    if '天' in secretime:
        secretime = re.sub('天','',secretime)
        delta = datetime.timedelta(days=int(secretime))
        datetime_dt = datetime_dt - delta
        datetime_str = datetime_dt.strftime("%Y/%m/%d")
    elif '週' in secretime:
        secretime = re.sub('週','',secretime)
        delta = datetime.timedelta(days=int(secretime)*7)
        datetime_dt = datetime_dt - delta
        datetime_str = datetime_dt.strftime("%Y/%m/%d")
    else:
        datetime_str = 'error'
    ans2.append(datetime_str)
    return ','.join(ans2)

posturl = f'https://www.facebook.com/mcdonalds.tw/posts/{number}'
datetime_dt = datetime.datetime.today()# 獲得當地時間
# delta = datetime.timedelta(days=0)
# datetime_dt = datetime_dt - delta

with open (f'data/comments{number}.csv','a') as f:
    f.write(f"posturl,是不是作者,留言者連結,留言內容,留言獲得心情數,留言時間,留言者學歷,留言者現居地,留言者婚姻,留言者朋友數,留言者性別,留言者工作,迴響留言數,迴響留言者連結,迴響留言內容,迴響留言獲得心情數,迴響留言時間\n")

with open (f'data/mc{number}.txt','r') as f:
    driver = start_driver(driver_path)
    time.sleep(1)
    driver.refresh()
    time.sleep(1)

    raw_soup = bs(f.read(),'lxml')                                                                                  
    soups = raw_soup.select('[class="d2edcug0 oh7imozk tr9rh885 abvwweq7 ejjq64ki"] [class="j83agx80 cbu4d94t"] [class="l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl"]')
    soups1 = raw_soup.select('[class="d2edcug0 oh7imozk tr9rh885 abvwweq7 ejjq64ki"] [class="j83agx80 cbu4d94t"] [class="kvgmc6g5 jb3vyjys rz4wbd8a qt6c0cv9 d0szoon8"]')
    with tqdm(total=len(soups)) as pbar:
        for i in range(len(soups)):
            main, prul = main_comment(soups,datetime_dt)
            res_single = single_info(driver, prul)
            if len(soups1[i].select('[class="g3eujd1d ni8dbmo4 stjgntxs hv4rvrfc"]')) >0:
                #迴響人的網址和內容跟
                comcom = soups1[i].select('[class="g3eujd1d ni8dbmo4 stjgntxs hv4rvrfc"]')
                for j in comcom:
                    #網址                
                    sec = sec_comment(j,datetime_dt)
                    # print(f"{postid},{main},{len(comcom)},{sec},'\n")
                    with open (f'data/comments{number}.csv', 'a', encoding = 'utf_8_sig') as f:
                        f.write(f"{posturl},{main},{res_single},{len(comcom)},{sec}'\n")
                pbar.update(1)
            else:
                # print(f"{postid},{main}")
                with open (f'data/comments{number}.csv', 'a',encoding = 'utf_8_sig') as f:
                    f.write(f"{posturl},{main},{res_single},0\n")
                pbar.update(1)
                continue


    
    # res = soup.select('[]')
    # res = soup.select('[class="d2edcug0 oh7imozk tr9rh885 abvwweq7 ejjq64ki"] [class="j83agx80 cbu4d94t"] [class="l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl"] [class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]')
    # for ri in res:
    #     if 'class="m9osqain j1meafb1 lrazzd5p b2s5l15y j1lvzwm4 kady6ibp"' in str(ri):
    #         print('hi')
    # print(res[0])

    # res = soup.select('[class="d2edcug0 oh7imozk tr9rh885 abvwweq7 ejjq64ki"] [class="l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl"] [class="g3eujd1d ni8dbmo4 stjgntxs hv4rvrfc"] [class="q9uorilb bvz0fpym c1et5uql sf5mxxl7"] [class="_680y"] [class="_6cuy"] [class="b3i9ofy5 e72ty7fz qlfml3jp inkptoze qmr60zad rq0escxv oo9gr5id q9uorilb kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x d2edcug0 jm1wdb64 l9j0dhe7 l3itjdph qv66sw1b"] [class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]')
    # for i in range(len(res)):s
        # print(res[i]['href'])
