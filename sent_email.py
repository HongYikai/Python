#coding:utf-8   #强制使用utf-8编码格式
import smtplib  #加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
import time

my_sender='' #发件人邮箱账号

my_user= str(input("请输入对方邮箱：") )#收件人邮箱账号
def mail():
    try:
        msg=MIMEText("这是一封来自Python的邮件","plain","utf-8")
        msg['From']=formataddr([my_sender,my_sender])   #括号里的对应发件人邮箱昵称（str）、发件人邮箱账号
        msg['To']=formataddr([my_user,my_user])   #括号里的对应收件人邮箱昵称（str）、收件人邮箱账号
        msg['Subject']="python测试" #邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.xx.xx.com",25)  #发件人邮箱中的SMTP服务器，端口是25,SSL加密则根据各网站服务器定义的写
        server.login(my_sender,"")    #括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())   #括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()   #这句是关闭连接的意思
        print("邮件已经发给%s"%my_user)
    except Exception:   #如果try中的语句没有执行，则会执行下面
        print("邮件未发出")
mail()