# -*- coding: utf-8 -*-
#用itchat调用网页版微信进行程序监控及远程执行一些命令，可扩展性很高

import itchat

#itchat.auto_login(enableCmdQR=True,hotReload=True) #用命令行显示二维码
itchat.auto_login() #登陆一次就可以了
#itchat.send('测试一下', toUserName='filehelper') #发送给文件助手
author = itchat.search_friends(remarkName='这里填写备注名')[0] #用 备注名 搜索指定好友比较好
author.send('测试一下，来自python') #发送信息给指定好友


@itchat.msg_register(itchat.content.TEXT) #消息注册
def text_reply(msg): #程序每收到一次消息都会调用一次函数
    print(msg['Text'])  #打印文本消息的内容  
    if msg['Text']=='退出':  #退出程序
        itchat.logout() 
    if msg['Text']=='回复我':
        return '回复你妹啊' #自动回复别人发给你的原消息

itchat.run() #开始执行自动回复
#itchat.logout() #记得退出 