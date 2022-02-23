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


async def getnode(tempdict, answerlist, group, waittime):
    await asyncio.sleep(waittime)
    session2 = PromptSession()
    with patch_stdout():
        node = await session2.prompt_async('请输入需删除的答案标记(输入-1可取消)：')
    try:
        node = int(node)
    except:
        print('参数错误')
        return None
    if node == -1:
        print('取消删除')
        return None
    try:
        answerlist.pop(node)
        filename = str(group) + '.cl'  # 读取已缓存的词库
        file = open(filename, 'w', encoding='utf-8-sig')
        file.write(str(tempdict))
        file.close()
        print('删除成功！')
    except:
        print('删除失败，答案不存在')
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
    #answer=eval(answer)
    for i in answer:  # 去除答案中的imageId，不去除mirai api http会无法回复
        try:
            i.pop('imageId')
        except:
            continue
    print('找到', len(answer), '个答案', flush=True)
    for i in answer:
        time.sleep(1)
        index = {'type': 'Plain', 'text': ''}
        index['text'] = '\n标记:' + str(answer.index(i))
        messagechain = copy.deepcopy(eval(i['answertext']))
        messagechain.append(index.copy())
        #print(messagechain)
        print(i['answertext'], '标记:', answer.index(i), flush=True)
        messagesign = simuse.Send_Message_Chain(data, sender, 2, messagechain)
        #print(messagesign)
        if str(messagesign) == 'None':
            messagechain_0 = [{
                'type': 'Plain',
                'text': '该答案发送失败，请在ChatLearning控制台中查看'
            }]
            messagechain_0.append(index.copy())
            simuse.Send_Message_Chain(data, sender, 2, messagechain_0)
    time.sleep(0.7)
    simuse.Send_Message(data, sender, 2, '发送完毕，请在ChatLearning控制台中继续操作', 1)
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
            waittime = replyanswer(data, sender, answerlist)
            loop2 = asyncio.new_event_loop()
            asyncio.set_event_loop(loop2)
            try:
                loop2.run_until_complete(
                    getnode(tempdict, answerlist, group, waittime))
            except:
                loop2.close()
                return None
        else:
            print('该问题无答案')
            simuse.Send_Message(data, sender, 2, '该问题无答案', 1)
            return None
    else:
        print('未找到该问题')
        simuse.Send_Message(data, sender, 2, '未找到该问题', 1)
    return None


def listening(data, sender, group):
    while 1:
        if getconfig() == 0:
            return None
        message = simuse.Fetch_Message(data)  # 监听消息链
        if type(message) == type(0):
            time.sleep(0.5)
            continue
        for i in message:
            if i['type'] == 'FriendMessage' and i[
                    'sender'] == sender:  # 判断监听到的消息是否为群消息
                messagechain = i['messagechain']
                messagechain.pop(0)
                question = messagechain
                getanswer(data, sender, group, question)  # 获取答案
        time.sleep(0.5)


async def tui(data, sender, group):
    session = PromptSession()
    listen = threading.Thread(target=listening, args=(data, sender, group))
    listen.start()
    while 1:
        with patch_stdout():
            command = await session.prompt_async('\nChatLearning(管理模式) ->')
            command = command.lower()
        if command == 'admin':
            file = open('config.clc', 'r', encoding='utf-8-sig')
            config = file.read()
            file.close()
            config = eval(config)
            config['admin'] = 0
            file = open('config.clc', 'w', encoding='utf-8-sig')
            file.write(str(config))
            file.close()
            print('<-退出管理模式')
            break
        else:
            print('请先输入admin退出管理模式！')
    return None


def getfilelist():
    filelist = os.listdir()
    cllist = []
    for i in filelist:
        if i[-3:] == '.cl':
            #print(i)
            cllist.append(i)
    cllist.remove('Merge.cl')
    grouplist = []
    for i in cllist:
        grouplist.append(int(i[:-3]))
    return grouplist


def main(sender, group):
    #print(getfilelist())
    if not (group in getfilelist()):
        print('<-群定位失败，未找到群', group)
        print('<-退出管理模式')
        return None
    print('<-定位到群', group)
    print('请使用管理员QQ', getconfig(1), '向bot发送消息')
    data = simuse.Get_data()
    data = simuse.Get_Session(data)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tui(data, sender, group))
    return None
