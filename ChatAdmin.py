import asyncio
import copy
import os
import threading
import time

import nest_asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

import simuse

nest_asyncio.apply()


def exitadmin(getadminsign=0):
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    file.close()
    config = eval(config)
    if getadminsign == 1:
        return config['admin']
    config['admin'] = 0
    file = open('config.clc', 'w', encoding='utf-8-sig')
    file.write(str(config))
    file.close()


def getnode(data, tempdict, answerlist, group, sender):
    #await asyncio.sleep(waittime)
    simuse.Send_Message(data, sender, 2, '请输入需删除的答案标记(输入-1可取消，多个用,隔开)：', 1)
    print('请在聊天窗口发送需删除的答案标记(发送-1可取消，多个用,隔开)')
    while 1:
        node = None
        message = simuse.Fetch_Message(data)
        if type(message) == type(0):
            time.sleep(0.5)
            continue
        for i in message:
            if i['type'] == 'FriendMessage' and i[
                    'sender'] == sender:  # 判断监听到的消息是否为群消息
                messagechain = i['messagechain']
                command = messagechain[1]
                if command['type'] == 'Plain':
                    node = command['text']
                    break
        if node != None:
            break
    if node == str(-1):
        simuse.Send_Message(data, sender, 2, '取消删除', 1)
        print('取消删除')
        return None
    try:
        node = node.replace('，', ',')
        node = node.replace(' ', ',')
    except:
        pass
    nodelist = '[{}]'.format(node)
    try:
        nodelist = eval(nodelist)
        if type(nodelist) != type([]):
            print('参数错误')
            simuse.Send_Message(data, sender, 2, '参数错误', 1)
            return None
    except:
        print('参数错误')
        simuse.Send_Message(data, sender, 2, '参数错误', 1)
        return None
    simuse.Send_Message(data, sender, 2, '正在执行操作，请稍等', 1)
    templist = []
    sendtext = ''
    for i in nodelist:
        time.sleep(1)
        try:
            templist.append(answerlist[i])
        except:
            print('标记为', i, '的答案不存在')
            sendtext = sendtext + str(i) + ' '
    #simuse.Send_Message(data, sender, 2, '标记为'+sendtext+'的答案不存在', 1)
    for i in templist:
        #print(i)
        answerlist.remove(i)
    filename = str(group) + '.cl'  # 读取已缓存的词库
    file = open(filename, 'w', encoding='utf-8-sig')
    file.write(str(tempdict))
    file.close()
    if templist != []:
        simuse.Send_Message(
            data, sender, 2, '标记为' + sendtext + '的答案不存在' + '\n' + '删除' +
            str(len(templist)) + '个答案成功！', 1)
        print('删除', str(len(templist)), '个答案成功！')
        return None
    else:
        simuse.Send_Message(data, sender, 2,
                            '标记为' + sendtext + '的答案不存在' + '\n' + '删除失败', 1)
        print('删除失败')
        return None


def getconfig(adminnum=0):
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    file.close()
    config = eval(config)
    if adminnum == 1:
        return config['Administrator']
    admin = config['admin']
    admin = int(admin)
    return admin


def replyanswer(data, sender, answer):  # 发送答案
    nodelist = []
    #answer=eval(answer)
    for i in answer:  # 去除答案中的imageId，不去除mirai api http会无法回复
        try:
            i.pop('imageId')
        except:
            continue
    print('找到', len(answer), '个答案', flush=True)
    tips = '若显示的答案不完整，或未成功发送，则可在ChatLearning控制台中查看'
    simuse.Send_Message(data, sender, 2,
                        '找到' + str(len(answer)) + '个答案' + '\n' + tips, 1)
    nodedict = {
        'senderId': data['qq'],
        'time': int(time.time()),
        'senderName': 'ChatLearning',
        'messageChain': []
    }
    #messagechain_c=nodedict['messageChain']
    for i in answer:
        changelist=[]
        #time.sleep(1)
        #print(i)
        num=answer.index(i)
        temp=answer[num]
        templist=eval(temp['answertext'])
        for k in templist:
        #print(type(templist),type(tempdict))
        #print(templist)
        #print(tempdict)
        #print(tempdict)
            try:
                if k['type']=='At':
                    changelist=[{'type':'Plain','text':'该答案为@消息，要显示完整请在ChatLearning控制台查看'}]
                    #print(k)
                    #print('-',changelist)
                elif k['type']=='Quote':
                    changelist=[{'type':'Plain','text':'该答案为回复类消息，要显示完整请在ChatLearning控制台查看'}]
                    #print(k)
                    #print('-',changelist)
                elif k['type']=='AtAll':
                    changelist=[{'type':'Plain','text':'该答案为@全员消息，要显示完整请在ChatLearning控制台查看'}]
                    #print(k)
                    #print('-',changelist)
            except:
                #print('error')
                pass
            #print(i)
        index = {'type': 'Plain', 'text': ''}
        index['text'] = '\n标记:' + str(answer.index(i))
        if changelist!=[]:
            #print(changelist)
            messagechain=copy.deepcopy(changelist)
            #print(messagechain)
        else:
            messagechain = copy.deepcopy(eval(i['answertext']))
        messagechain.append(index.copy())
        #print(messagechain)
        print(i['answertext'], '标记:', answer.index(i), flush=True)
        #messagesign = simuse.Send_Message_Chain(data, sender, 2, messagechain)
        nodedict['messageChain'] = messagechain
        nodelist.append(nodedict.copy())
        #print(messagesign)
    sendmessagechain = [{'type': 'Forward', 'nodeList': ''}]
    sendmessagedict = sendmessagechain[0]
    sendmessagedict['nodeList'] = nodelist
    simuse.Send_Message_Chain(data, sender, 2, sendmessagechain)
    time.sleep(0.7)
    #simuse.Send_Message(data, sender, 2, '发送完毕，请在ChatLearning控制台中继续操作', 1)
    print('请稍等，程序正在处理……')
    return len(answer)


def getanswer(data, sender, group, question):  # 从词库中获取答案
    for i in question:  # 去除作为问题中的变动因素“url”
        try:
            i.pop('url')
        except:
            continue
    question = str(question)
    filename = str(group) + '.cl'  # 读取已缓存的词库
    file = open(filename, 'r', encoding='utf-8-sig')
    tempdict = file.read()
    file.close()
    tempdict = eval(tempdict)
    try:  # 检索问题，若词库中无该问题，则函数返回-1，若有，则返回所有答案（答案列表）
        #print(question)
        questiondict = tempdict[question]
        answerlist = questiondict['answer']
    except:
        answerlist = -1
    if answerlist != -1:
        if answerlist != []:
            replyanswer(data, sender, answerlist)
            #loop2 = asyncio.new_event_loop()
            #asyncio.set_event_loop(loop2)

            getnode(data, tempdict, answerlist, group, sender)

        else:
            print('该问题无答案')
            simuse.Send_Message(data, sender, 2, '该问题无答案', 1)
            return None
    else:
        print('未找到该问题')
        simuse.Send_Message(data, sender, 2, '未找到该问题', 1)
    return None


def listening(data, adminlist, group):
    while 1:
        if getconfig() == 0:
            break
        message = simuse.Fetch_Message(data)  # 监听消息链
        if type(message) == type(0):
            time.sleep(0.5)
            continue
        for i in message:
            if i['type'] == 'FriendMessage' and (
                    i['sender'] in adminlist):  # 判断监听到的消息是否为群消息
                messagechain = i['messagechain']
                messagechain.pop(0)
                command = messagechain[0]
                if command['type'] == 'Plain' and command['text'] == 'admin':
                    exitadmin()
                    simuse.Send_Message(data, i['sender'], 2, '退出管理模式', 1)
                    break
                question = messagechain
                getanswer(data, i['sender'], group, question)  # 获取答案
        time.sleep(0.5)


def tui(data, adminlist, group):
    listen = threading.Thread(target=listening, args=(data, adminlist, group))
    listen.start()
    print('当前处于管理模式')
    while 1:
        time.sleep(1)
        if exitadmin(1) == 0:
            print('退出管理模式')
            return None
    #return None


def getfilelist():
    filelist = os.listdir()
    cllist = []
    for i in filelist:
        if i[-3:] == '.cl':
            #print(i)
            cllist.append(i)
    try:
        cllist.remove('Merge.cl')
    except:
        pass
    grouplist = []
    for i in cllist:
        grouplist.append(int(i[:-3]))
    return grouplist


def main(data, adminlist, group, fromchat):
    #print(getfilelist())
    if not (group in getfilelist()):
        print('<-群定位失败，未找到群', group)
        print('<-退出管理模式')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2,
                                '群定位失败，未找到群' + str(group) + '\n' + '退出管理模式', 1)
        return None
    print('<-定位到群', group)
    if fromchat != 0:
        tips = '定位到群' + str(group) + '\n' + '请发送“问题”，发送admin可退出管理模式'
        simuse.Send_Message(data, fromchat, 2, tips, 1)
    print('请使用管理员QQ', getconfig(1), '向bot发送消息')
    tui(data, adminlist, group)
    return None
