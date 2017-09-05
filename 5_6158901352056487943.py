#coding:utf-8
#===================================================
#               www.hongyikai.com
#===================================================

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re 
import csv




#你的selenium的驱动地址：
driverUrl='D:\pymodules\chromedriver.exe'
#你的pubmed网址（先按规则搜索，copy第一个结果页面到这里）：
webUrl='http://xm.meituan.com/dianying/cinemalist/zhongshanlulundu'
driver = webdriver.Chrome(executable_path= driverUrl)
driver.implicitly_wait(60) #智能等待
driver.get(webUrl)
time.sleep(3)
driver.find_element_by_xpath('//a[text()="思明电影院"]').click()
now_handle = driver.window_handles[1] #获取目标窗口句柄
print(now_handle)  #输出目标窗口句柄
driver.close() #关闭当前窗口
driver.switch_to_window(now_handle) #切换目标窗口为当前窗口
i=1
#得到所有影片
movies=driver.find_elements_by_xpath("//div[@class='movie-info' or @class='movie-info movie-info--current']")
for movie in movies: # 遍历每部影片
    premiere=movie.find_element_by_xpath('//dd[1]').text #获取当前影片的首映日期
    print(premiere)
#    if movie not    



time.sleep(10) 
driver.quit()       
#for movie in 影片库:  #所有影片遍历一遍
#    if movie not 预售: #跳过非预售的影片，一般非预售的影片没有优惠
#        continue
#    for date in 影片观影日期: #遍历目标影片的所有观影日期
#        for time in 观影时间: #遍历观影时间
#            if 18:00<=time<=21:30 or date ==星期六 or 星期日: #筛选观影时间条件
#            if 手机专享价: #筛选有 手机专享价 的影片
#                #下载价格图片
#                #识别图片
#                if price <= 目标价位:
#                    价位池.append=影片简要信息
#print(价位池)
#if 价位池 非空:
#    #发送价位池到微信
#    价位池=[]  #清空
##8±3min后重新遍历一遍

                
                
            












