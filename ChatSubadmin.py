import time

import ChatAllfind
import ChatLearning
import ChatReply
import simuse
from ChatClass import My_Thread


def getconfig():
    try:
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = file.read()
        config = eval(config)
        file.close()
        Subadmindict = config['subadmin']
    except:
        return None
    return Subadmindict


def Subreply(data, group):
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    config = eval(config)
    file.close()
    replygrouplist = config['replygrouplist']
    if group in replygrouplist:
        replygrouplist.remove(group)
        simuse.Send_Message(data, group, 1, '已关闭本群回复', 1)
    else:
        replygrouplist.append(group)
        simuse.Send_Message(data, group, 1, '已开启本群回复', 1)
    config['replygrouplist'] = replygrouplist
    file = open('config.clc', 'w', encoding='utf-8-sig')
    file.write(str(config))
    file.close()


def Sublearning(data, group):
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    config = eval(config)
    file.close()
    learninggrouplist = config['learninggrouplist']
    if group in learninggrouplist:
        learninggrouplist.remove(group)
        simuse.Send_Message(data, group, 1, '已关闭本群记录', 1)
    else:
        learninggrouplist.append(group)
        simuse.Send_Message(data, group, 1, '已开启本群记录', 1)
    config['learninggrouplist'] = learninggrouplist
    file = open('config.clc', 'w', encoding='utf-8-sig')
    file.write(str(config))
    file.close()


def Subadmin(group, sender):
    print('群{}进入管理模式,操作者：{}'.format(group, sender))
    data = simuse.Get_data()
    data = simuse.Get_Session(data)
    learning_config = ChatLearning.getconfig()
    reply_config = [ChatReply.getconfig(3), ChatReply.getconfig(1)]
    learning_close_sign = 0
    reply_close_sign = 0
    if learning_config[1] == 1 and group in learning_config[2]:
        Sublearning(data, group)
        learning_close_sign = 1
    time.sleep(0.8)
    if reply_config[0] == 1 and group in reply_config[1]:
        Subreply(data, group)
        reply_close_sign = 1
    time.sleep(0.8)
    ChatAllfind.findallcontrol(data, sender, group=group)
    print('群{}退出管理模式,操作者：{}'.format(group, sender))
    simuse.Send_Message(data, group, 1, '退出管理模式', 1)
    if learning_close_sign == 1:
        time.sleep(0.8)
        Sublearning(data, group)
    if reply_close_sign == 1:
        time.sleep(0.8)
        Subreply(data, group)


def main():
    data = simuse.Get_data()
    data = simuse.Get_Session(data)
    while 1:
        time.sleep(1)
        subadmindict = getconfig()
        if subadmindict == None:
            continue
        message = simuse.Fetch_Message(data)  # 监听消息链
        if type(message) == type(0):
            time.sleep(0.5)
            continue
        command = ''
        for i in message:
            if i['type'] == 'GroupMessage':  # 判断监听到的消息是否为群消息
                if i['group'] in subadmindict.keys(
                ) and i['sender'] in subadmindict[i['group']]:
                    messagechain = i['messagechain']
                    messagedict = messagechain[1]
                    if messagedict['type'] == 'Plain':
                        command = messagedict['text']
                        group = i['group']
                        sender = i['sender']
        if command == '':
            continue
        elif command == '!learning' or command == '！learning':
            Sublearning(data, group)
        elif command == '!reply' or command == '！reply':
            Subreply(data, group)
        elif command == '!admin' or command == '！admin':
            subadmin = My_Thread(target=Subadmin, args=[group, sender])
            subadmin.start()
