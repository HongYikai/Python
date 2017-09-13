# -*- coding: utf-8 -*-
#===================================================
#               www.hongyikai.com
#===================================================

from selenium import webdriver
import time
import random
import itchat
from PIL import Image
import pytesseract
#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'




#目标价位：元，低于此价位的手机专享价才会被收集
targetPrice= 30


itchat.auto_login(enableCmdQR=2,hotReload=True) #用命令行显示二维码
#itchat.auto_login() #登陆一次就可以了



testCount=0
#定时的死循环
while True:
#你的selenium的驱动地址：
    driver = webdriver.PhantomJS(executable_path='/root/anaconda3/selenium/webdriver/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    #你的网址（先按规则搜索，copy第一个结果页面到这里）：
    webUrl='http://xm.meituan.com/dianying/cinemalist/zhongshanlulundu' 
    #webUrl='http://xm.meituan.com/shop/115078857?mtt=1.movie%2Fcinemalist.0.0.j7c6icyx'#华谊兄弟影院
    #符合要求的电影将放在这个变量里，输出到微信
    output=[] #每次循环前清空列表
    driver.implicitly_wait(30) #智能等待
    driver.get(webUrl)
#    driver.maximize_window() #屏幕最大化
#    
#    #从中山路页面进入，然后切换为目标影院
#    #关闭下面的下载链接，挡视野
#    time.sleep(1)
#    driver.find_element_by_xpath("//span[@class='close-it']").click()
#    #下拉滚动条
#    js = "var q=document.body.scrollTop=300"  
#    driver.execute_script(js)
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="cinema-info__list"]//a[text()="中华电影院"]').click()
    time.sleep(0.3)
    now_handle = driver.window_handles[1] #获取目标窗口句柄
    print(now_handle)  #输出目标窗口句柄
    driver.close() #关闭当前窗口
    time.sleep(0.2)
    driver.switch_to_window(now_handle) #切换目标窗口为当前窗口
    
    
    
#    #下拉滚动条,后面截图的时候要减去
#    js = "var q=document.body.scrollTop=600"  
#    driver.execute_script(js)
#    #关闭下面的下载链接，挡视野
#    time.sleep(1)
#    driver.find_element_by_xpath("//span[@class='close-it']").click()
#    driver.maximize_window() #屏幕最大化
#    driver.set_window_size(1440, 900)
    time.sleep(5)
    dateNow=time.localtime()
    print('当地日期为：%s'%time.strftime("%Y-%m-%d", time.localtime()))
    #得到影片列表数movieN（每个列表里还有影片）
    movieLists=driver.find_elements_by_xpath("//li[@class='mt-slider-sheet mt-slider-current-sheet' or @class='mt-slider-sheet']")
    movieN=len(movieLists)
    print('总共有%d个电影列表。'%(movieN))
    
    
    for i in range(movieN):
        #获取活动状态列表下的电影
        movies=driver.find_elements_by_xpath("//li[@class='mt-slider-sheet mt-slider-current-sheet' or @class='mt-slider-sheet']")[i]
    #    print(i,":  ",movies.is_displayed())
        movies=movies.find_elements_by_tag_name('a')
        movieCount=1
        for movie in movies: #遍历当前列表里的每1部影片
            movie.click()
            time.sleep(1)
            #首映日期
            premiere=driver.find_element_by_xpath("//div[@class='movie-info movie-info--current']//dd").text 
            #电影名称
            movieName=driver.find_element_by_xpath("//div[@class='movie-info movie-info--current']//h3").text
    
            if time.strptime(premiere, "%Y-%m-%d") < dateNow: #跳过非预售的影片，预售才有优惠
                if movieCount ==4: #超过4部就切换列表
                    break
                movieCount+=1
                continue 
    
    
            
            print(" ")
            print(" ")
            print('%s(%s首映)'%(movieName,premiere))
            print('-'*30)
            #电影开放售卖的日期
            movie_dates=driver.find_elements_by_xpath("//div[@class='movie-info movie-info--current']/div[@class='show-time']//a")
            driver.implicitly_wait(2) #设置等待超时，以免try命令等太久
            for movie_date in movie_dates:
                movie_date.click()
                time.sleep(0.1)
                try:
                    triggerPrice =driver.find_element_by_xpath("//div[@class='movie-info movie-info--current']/table[@class='time-table time-table--current']//span[@class='trigger__price']")
                    triggerPriceShow=triggerPrice.text[:-2]
                    
                    #对手机专享优惠的价格截图，然后截图 
                    driver.get_screenshot_as_file('triggerPrice.png') 
                    left = int(triggerPrice.location['x'])+24 # 去掉文字
                    top = int(triggerPrice.location['y']) #减去滚动条的值
                    right = int(triggerPrice.location['x'] + triggerPrice.size['width'])-19 #去掉右边的下拉箭头
                    bottom = int(triggerPrice.location['y'] + triggerPrice.size['height']) #减去滚动条的值
#                    print(left, top, right, bottom)
#                    
                    im = Image.open('triggerPrice.png')
#                    print('open')

                    im = im.crop((left, top, right, bottom)) #截取价格 
#                    print('crop')
                    w,h = im.size #获得图片尺寸
#                    print('im.size')
                    im=im.resize((w*3,h*3)) #长宽各放大10倍
#                    print('resize')
                    im=im.convert('L') #灰阶
#                    print('convert')
                    im=im.point(lambda x:0 if x<195 else 255) #二值化
#                    print(left, top, right, bottom)
#                    print('point')
                    im.save('price.png') #储存处理后的图片
#                    print('save')

                    thePrice = pytesseract.image_to_string(im) #识别数值
#                    print(left, top, right, bottom)
#                    print(thePrice)
                    thePrice=float(thePrice.replace(' ','')) #把字符串价格里的空格去掉,并转换为数值
                    

                    print(movie_date.text,': ',triggerPriceShow,thePrice,'元')
                    if thePrice <= targetPrice:
                        output.append(movieName+'('+movie_date.text+':'+str(thePrice)+'元)')
                except:
                    print(movie_date.text,': 没有优惠')
            driver.implicitly_wait(30) #恢复为30秒
            
    
            if movieCount ==4: #超过4部就切换列表
                break 
            movieCount+=1
        
        
        driver.find_elements_by_xpath('//a[@style="opacity: 0.6;" or @style="opacity: 0;"]')[1].click()
        time.sleep(3)
    
    
    #获取网络时间
    
    driver.get('http://www.114time.com')
    time.sleep(5)
    hour=driver.find_element_by_xpath('//b[@class="hour"]').text
    hour=int(hour)
    time.sleep(1)
    driver.quit() 
    
    print('='*30+'\n'+'\n'+'\n'+'\n'+'-'*30)
    #发送信息给指定好友
    
#    print(output)
    author = itchat.search_friends(remarkName='kai')[0] #用 备注名 搜索指定好友比较好
    testCount+=1
    if testCount == 1 :
        haha='尊敬的主人：'+'\n'+'\n'+'第一次运行基本正常，等待10分钟左右进入第二次运行。'+'\n'+'\n'+'你家的小虫'
        author.send(haha)
    elif testCount == 2 :
        haha='尊敬的主人：'+'\n'+'\n'+'第二次运行正常，现在。待检索到价格<'+str(targetPrice)+'元的电影票再通知您。'+'\n'+'\n'+'你家的小虫'
        author.send(haha)
    
    
    
    itchat.send(' ', toUserName='filehelper')#空消息，好像可以减少微信掉线？
    if len(output) != 0 :
        #微信只能发字符，把列表转换成字符把
        movieMsgSend='第'+str(testCount)+'次检索'+'\n'+'美团优惠电影票如下：'+'\n'+'\n' #清空上次可能的输出信息
        for outP in output:
            movieMsgSend=movieMsgSend+outP+'\n'
            
        movieMsgSend=movieMsgSend+'\n'+'由Kai的服务器监控与筛选'+'\n'+'你家的小虫'
        author.send(movieMsgSend) 
        print(movieMsgSend)
        print('-'*30+'\n'+'\n'+'\n') 
       
        
    #等待一定时间后重启遍历影片
    timeRandom=random.randint(100, 300) #不要太规律了，搞点随机数
    print('正在等待：%d minutes'%int((600+timeRandom)/60))
    time.sleep(600+timeRandom)
#    time.sleep(5)    

    if 1<hour<6: #晚上就不要爬了，吵人。注意不要让if一个晚上可以运行两次，后果很严重。。。
        haha='第'+str(testCount)+'运行已完成，进入睡眠模式。'+'\n'+'\n'+'明早见'+'\n'+'你家的小虫'
        author.send(haha)
        print(haha)
        time.sleep(21600)
        haha='早上好，开始自动执行今天的第一次运行。'+'\n'+'\n'+'你家的小虫'
        author.send(haha)
        print(haha)
        
        
    print('下一个循环继续执行：')

