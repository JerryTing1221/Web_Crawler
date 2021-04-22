from selenium import webdriver
import requests
import pandas as pd
from lxml import etree
import time
import ssl
from selenium.webdriver import Chrome 
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from lxml import etree
from lxml import etree
import os




ssl._create_default_https_context = ssl._create_unverified_context



page = 1

res = []

#對api requests，獲取json
for i in range(0,62):
    url = 'https://travel.yahoo.com.tw/ajax/LoadMore.php'

    userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'

    headers = {
        'user-aghent':userAgent
    }

    data = {
        'P' : page,    #總共61頁
        'T' : '台南',
        'type': 'tag',
        'GATitle': '台南'
    }

    resq = requests.post(url=url, headers=headers, data=data)
    
    res.append(resq.text) #把抓下的原始碼都存成一個list   (res = [])
    
    page+=1
    



Link = []
Title = []

#拆解每一頁，抓出每一頁的所有連結跟標題
for i in res:
    soup = BeautifulSoup(i)
    pageLinkList = soup.select('a[href]')
    pageTitleList = soup.select('div[class="item_topic dotdotdot"]')
    
    for title in pageTitleList:
        pageTitle = title.text
        Title.append(pageTitle)  #把每一頁的標題append到同一個list裡（Title= []）
        #print(pageTitle)


    for link in pageLinkList:
        pageLink = 'https://travel.yahoo.com.tw/' + link['href']
        Link.append(pageLink)   #把每一頁的連結append到同一個list裡（Link= []）
        #print(pageLink)
 
 
 


#新增一個資料夾
folderName = './YahooBlog/'

if not os.path.exists(folderName):
        os.mkdir(folderName)



#抓出所有的內容（從Link這個list有沒一篇文章連結）       
index = 0                

for i in Link:
    url_page = i
    resq_page = requests.get(url_page) 
    soup_page = etree.HTML(resq_page.text)
    content = soup_page.xpath('//*[@id="LeftCol"]/article/div[2]/p/text()')
    
    
    str1 = ''
    #print(str1.join(content))
    
    pagePath = folderName + Title[index]

    try:
        with open(pagePath, 'w') as f:  #把文章分篇存入資料夾
            f.write(str1.join(content))    #因為每一篇文章的內容被拆成一句一句字串，所有用.join()把字串合起來
    except:
        pass


    index+=1
