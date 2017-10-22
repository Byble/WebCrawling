# -*- coding: cp949 -*-

import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import xlrd
import xlwt
import pymysql

conn = pymysql.connect(host='localhost', user='UserID', password='UserPW', db='UserDB', charset='utf8')

curs = conn.cursor()

sql = "INSERT INTO recommend(name, address, contents) VALUES(%s,%s,%s)"

#for save with xls
"""
workbook = xlwt.Workbook(encoding='utf-8')
workbook.default_style.font.height = 20*11

worksheet = workbook.add_sheet(u'seat')

font_style = xlwt.easyxf('font:height 280;')
worksheet.row(0).set_style(font_style)

worksheet.write_merge(0,0,0,1,u"name")
worksheet.write_merge(0,0,2,3,u"address")
worksheet.write_merge(0,0,4,5,u"description")

sheetxNum = 1
sheetyNum = 1
"""

pageNumber = 3

broswer = webdriver.Chrome('/Users/kimmingug/Desktop/StudyRecommend/chromedriver') #Your chromedriver location

searching = "C language"
url = "https://www.youtube.com"
broswer.get(url)


search = broswer.find_element_by_id("search")
search.send_keys(searching)

searchB = broswer.find_element_by_xpath("//*[@id='search-icon-legacy']")
searchB.click()

broswer.get(broswer.current_url+'&sp=EgIQAVAU')

no_of_loadmore = 1

try:
    while no_of_loadmore:
        broswer.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(2)
        no_of_loadmore-=1
        # print(no_of_loadmore)
except:
    pass


soup = BeautifulSoup(broswer.page_source, 'lxml')

ContentsDiv = soup.find('div',{'id':'contents'})

VideoList = ContentsDiv.findAll('div',{'class':'text-wrapper style-scope ytd-video-renderer'})

for i in VideoList:
    title = str(i.find('a'))

    titleName = title[title.find('title="') + 7:title.find('">')]
    print(titleName)

    # worksheet.write_merge(sheetxNum, sheetyNum, 0, 1, titleName)

    link = url + title[title.find('href="') + 6:title.find('" id')]
    print(link)

    # worksheet.write_merge(sheetxNum, sheetyNum, 2, 3, link)
    broswer.get(link)

    linkSoup = BeautifulSoup(broswer.page_source,'lxml')
    linkContents = linkSoup.find('yt-formatted-string',{'id':'description'})
    strBody = str(linkContents)
    ContentBody = strBody[strBody.find('"">') + 3:strBody.find('</')]

    if linkContents is None:
        while linkContents is None:
            linkSoup = BeautifulSoup(broswer.page_source, 'lxml')
            linkContents = linkSoup.find('yt-formatted-string', {'id': 'description'})
            strBody = str(linkContents)
            ContentBody = strBody[strBody.find('"">') + 3:strBody.find('</')]


    try:
        print(ContentBody)
        # worksheet.write_merge(sheetxNum,sheetyNum, 4, 5, ContentBody)
    except AttributeError:
        print("No Description.")
    print('----------------------------------------------')
    curs.execute(sql, (titleName, link, ContentBody))
    # sheetxNum = sheetxNum + 1
    # sheetyNum = sheetyNum + 1
    #time.sleep(2)

# workbook.save('example.xls')

conn.commit()
conn.close()

broswer.quit()
