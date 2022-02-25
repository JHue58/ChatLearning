import copy
import time

import ChatAdmin
import simuse


def getconfig():
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    config = eval(config)
    file.close()
    return config['blackfreq']


def replyanswer(data, sender, filterlist):  # 发送答案
    nodelist = []
    #answer=eval(answer)
    for i in filterlist:  # 去除答案中的imageId，不去除mirai api http会无法回复
        try:
            i.pop('imageId')
        except:
            continue
    print('条目共有', len(filterlist), '个', flush=True)
    tips = '若显示不完整，或未成功发送，则可在ChatLearning控制台中查看'
    simuse.Send_Message(data, sender, 2,
                        '条目共有' + str(len(filterlist)) + '个' + '\n' + tips, 1)
    nodedict = {
        'senderId': data['qq'],
        'time': int(time.time()),
        'senderName': 'ChatLearning',
        'messageChain': []
    }
    tipmessageChain = [{
        'type':
        'Plain',
        'text':
        '请输入需删除的标记' + '\n' + '(输入-1可取消,all清空所有,多个用空格隔开)：'
    }]
    nodedict['messageChain'] = tipmessageChain
    nodelist.append(nodedict.copy())
    #messagechain_c=nodedict['messageChain']
    for i in filterlist:
        changelist = []
        #time.sleep(1)
        #print(i)
        #num = answer.index(i)
        #temp = answer[num]
        templist = eval(i)
        for k in templist:
            #print(type(templist),type(tempdict))
            #print(templist)
            #print(tempdict)
            #print(tempdict)
            try:
                if k['type'] == 'At':
                    changelist = [{
                        'type': 'Plain',
                        'text': '该条目为@消息，要显示完整请在ChatLearning控制台查看'
                    }]
                    #print(k)
                    #print('-',changelist)
                elif k['type'] == 'Quote':
                    changelist = [{
                        'type': 'Plain',
                        'text': '该条目为回复类消息，要显示完整请在ChatLearning控制台查看'
                    }]
                    #print(k)
                    #print('-',changelist)
                elif k['type'] == 'AtAll':
                    changelist = [{
                        'type': 'Plain',
                        'text': '该条目为@全员消息，要显示完整请在ChatLearning控制台查看'
                    }]
                    #print(k)
                    #print('-',changelist)
                elif k['type'] == 'Poke':
                    changelist = [{
                        'type': 'Plain',
                        'text': '该条目为戳一戳类消息，要显示完整请在ChatLearning控制台查看'
                    }]
            except:
                #print('error')
                pass
            #print(i)
        index = {'type': 'Plain', 'text': ''}
        index['text'] = '\n标记:' + str(filterlist.index(i))
        if changelist != []:
            #print(changelist)
            messagechain = copy.deepcopy(changelist)
            #print(messagechain)
        else:
            messagechain = copy.deepcopy(eval(i))
        #print(messagechain)
        messagechain.append(index.copy())
        print(i, '标记:', filterlist.index(i), flush=True)
        #messagesign = simuse.Send_Message_Chain(data, sender, 2, messagechain)
        nodedict['messageChain'] = messagechain
        #nodedict['time']=i['time']
        nodelist.append(nodedict.copy())
        #print(messagesign)
    sendmessagechain = [{'type': 'Forward', 'nodeList': ''}]
    sendmessagedict = sendmessagechain[0]
    sendmessagedict['nodeList'] = nodelist
    simuse.Send_Message_Chain(data, sender, 2, sendmessagechain)
    time.sleep(0.7)
    #simuse.Send_Message(data, sender, 2, '发送完毕，请在ChatLearning控制台中继续操作', 1)
    print('请稍等，程序正在处理……')
    return len(filterlist)


def getnode(data, Filterconfig, filterlist, sender):
    #await asyncio.sleep(waittime)
    #simuse.Send_Message(data, sender, 2, '请输入需删除的答案标记'+'\n'+'(输入-1可取消,all清空所有,多个用空格隔开)：', 1)
    print('请在聊天窗口发送需删除的标记(发送-1可取消，多个用空格隔开)')
    while 1:
        node = ChatAdmin.get_admin_command(data, sender=sender)
        if node != None:
            break
    if node == 'all':
        filterlist.clear()
        file = open('Filter.clc', 'w', encoding='utf-8-sig')
        file.write(str(Filterconfig))
        file.close()
        time.sleep(0.5)
        simuse.Send_Message(data, sender, 2, '已清空', 1)
        return None
    if node == str(-1) or node == '–1':
        time.sleep(0.5)
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
            time.sleep(0.5)
            print('参数错误')
            simuse.Send_Message(data, sender, 2, '参数错误', 1)
            return None
    except:
        time.sleep(0.5)
        print('参数错误')
        simuse.Send_Message(data, sender, 2, '参数错误', 1)
        return None
    simuse.Send_Message(data, sender, 2, '正在执行操作，请稍等', 1)
    time.sleep(0.5)
    templist = []
    sendtext = ''
    for i in nodelist:
        time.sleep(1)
        try:
            templist.append(filterlist[i])
        except:
            print('标记为', i, '的条目不存在')
            sendtext = sendtext + str(i) + ' '
    #simuse.Send_Message(data, sender, 2, '标记为'+sendtext+'的答案不存在', 1)
    for i in templist:
        #print(i)
        filterlist.remove(i)
    #print(filterlist)
    file = open('Filter.clc', 'w', encoding='utf-8-sig')
    file.write(str(Filterconfig))
    file.close()
    if templist != []:
        if sendtext != '':
            simuse.Send_Message(
                data, sender, 2, '标记为' + sendtext + '的条目不存在' + '\n' + '删除' +
                str(len(templist)) + '个条目成功！', 1)
        else:
            simuse.Send_Message(data, sender, 2,
                                '删除' + str(len(templist)) + '个条目成功！', 1)
        print('删除', str(len(templist)), '个条目成功！')
        return None
    else:
        simuse.Send_Message(data, sender, 2,
                            '标记为' + sendtext + '的条目不存在' + '\n' + '删除失败', 1)
        print('删除失败')
        return None


def replyblack(data, Filterconfig, sender, blackdict):
    blackfreq = getconfig()
    nodelist = []
    nodedict = {
        'senderId': data['qq'],
        'time': int(time.time()),
        'senderName': 'ChatLearning',
        'messageChain': []
    }
    tipmessageChain = [{
        'type':
        'Plain',
        'text':
        '请输入需删除的账号' + '\n' +
        '(输入-1可取消,all清空所有,多个用空格隔开)\n触发次数大于{}次会被屏蔽：'.format(blackfreq)
    }]
    nodedict['messageChain'] = tipmessageChain
    nodelist.append(nodedict.copy())
    for i in blackdict:
        messagechain = []
        blackindex = {'type': 'Plain', 'text': ''}
        blackindex['text'] = str(i) + '\n已触发敏感词次数:' + str(blackdict[i])
        messagechain.append(blackindex.copy())
        nodedict['messageChain'] = messagechain
        nodelist.append(nodedict.copy())
    sendmessagechain = [{'type': 'Forward', 'nodeList': ''}]
    sendmessagedict = sendmessagechain[0]
    sendmessagedict['nodeList'] = nodelist
    simuse.Send_Message_Chain(data, sender, 2, sendmessagechain)
    while 1:
        node = ChatAdmin.get_admin_command(data, sender=sender)
        if node != None:
            break
    if node == 'all':
        blackdict.clear()
        file = open('Filter.clc', 'w', encoding='utf-8-sig')
        file.write(str(Filterconfig))
        file.close()
        time.sleep(0.5)
        simuse.Send_Message(data, sender, 2, '已清空', 1)
        return None
    if node == str(-1) or node == '–1':
        time.sleep(0.5)
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
            time.sleep(0.5)
            print('参数错误')
            simuse.Send_Message(data, sender, 2, '参数错误', 1)
            return None
    except:
        time.sleep(0.5)
        print('参数错误')
        simuse.Send_Message(data, sender, 2, '参数错误', 1)
        return None
    poperror = ''
    for i in nodelist:
        try:
            blackdict.pop(i)
        except:
            poperror = poperror + str(i) + ' '
    file = open('Filter.clc', 'w', encoding='utf-8-sig')
    file.write(str(Filterconfig))
    file.close()
    time.sleep(0.5)
    if poperror == '':
        time.sleep(0.5)
        simuse.Send_Message(data, sender, 2, '删除成功！', 1)
    else:
        time.sleep(0.5)
        simuse.Send_Message(data, sender, 2, '删除完毕！\n账号{}不存在'.format(poperror),
                            1)


def blackcheck():
    try:
        file = open('Filter.clc', 'r', encoding='utf-8-sig')
        Filterconfig = file.read()
        Filterconfig = eval(Filterconfig)
        file.close()
        return Filterconfig
    except:
        file = open('Filter.clc', 'w', encoding='utf-8-sig')
        Filterconfig = {
            'filter': [],
            'sensitive': [],
            'blackdict': {},
            'type': ['At', 'AtAll', 'Quote', 'Poke']
        }
        file.write(str(Filterconfig))
        file.close()
        return Filterconfig


def sensitivecheck(question, sender):
    for i in question:
        try:
            i.pop('url')
        except:
            pass
    Filterconfig = blackcheck()

    if str(question) in Filterconfig['sensitive']:
        creatblack(sender)
        print('已过滤，原因：与敏感问题匹配，已将发送者加入黑名单')
        return 0
    else:
        for i in question:
            if i['type'] == 'Plain':
                for k in Filterconfig['sensitive']:
                    k = eval(k)
                    for j in k:
                        if j['type'] == 'Plain':
                            if i['text'].find(j['text']) != -1:
                                creatblack(sender)
                                print('已过滤，原因：与敏感问题匹配，已将发送者加入黑名单')
                                return 0
    if sender in Filterconfig['blackdict'].keys():
        num = Filterconfig['blackdict']
        if num[sender] >= getconfig():
            print('该用户在黑名单中超出最大次数，已屏蔽')
            return 0
    return 1


def filtercheck(question):
    for i in question:  # 去除作为问题中的变动因素“url”
        try:
            i.pop('url')
        except:
            continue
    Filterconfig = blackcheck()
    #print(question)
    if str(question) in Filterconfig['filter']:
        print('已过滤，原因：与过滤名单匹配')
        return 0
    else:
        for i in question:
            if i['type'] in Filterconfig['type']:
                print('已过滤，原因：与过滤名单中消息类型匹配')
                return 0
        return 1


def creatfilter(question, addfilterlist=0):
    if addfilterlist == 0:
        for i in question:  # 去除作为问题中的变动因素“url”
            try:
                i.pop('url')
            except:
                continue
        question = str(question)
        Filterconfig = blackcheck()
        filterlist = Filterconfig['filter']
        #print(filterlist)
        filterlist.append(question)
        filterlist = list(set(filterlist))
        file = open('Filter.clc', 'w', encoding='utf-8-sig')
        file.write(str(Filterconfig))
        file.close()
    else:
        Filterconfig = blackcheck()
        filterlist = Filterconfig['filter']
        for i in question:
            for k in i:
                try:
                    k.pop('url')
                except:
                    continue
            filterlist.append(i['answertext'])
        filterlist = list(set(filterlist))
        file = open('Filter.clc', 'w', encoding='utf-8-sig')
        file.write(str(Filterconfig))
        file.close()
        #print(filterlist)


def creatsensitive(question):
    for i in question:  # 去除作为问题中的变动因素“url”
        try:
            i.pop('url')
        except:
            continue
    question = str(question)
    Filterconfig = blackcheck()
    sensitivelist = Filterconfig['sensitive']
    sensitivelist.append(question)
    sensitivelist = list(set(sensitivelist))
    filterlist = Filterconfig['filter']
    filterlist.append(question)
    filterlist = list(set(filterlist))
    file = open('Filter.clc', 'w', encoding='utf-8-sig')
    file.write(str(Filterconfig))
    file.close()


def creatblack(sender, list=0):
    Filterconfig = blackcheck()
    blackdict = Filterconfig['blackdict']
    if list != 0:
        for i in sender:
            blackdict[i] = 999
    elif sender in blackdict.keys():
        blackdict[sender] += 1
    else:
        blackdict[sender] = 1
    file = open('Filter.clc', 'w', encoding='utf-8-sig')
    file.write(str(Filterconfig))
    file.close()
    if list == 0:
        return blackdict[sender]


def filtercontrol(data, sender):
    while 1:
        time.sleep(1)
        tips = '请选择你的操作\n1.添加需过滤的问题\n2.添加敏感关键字\n3.添加黑名单账号\n4.查看\n5.退出管理模式'
        simuse.Send_Message(data, sender, 2, tips, 1)
        while 1:
            command = ChatAdmin.get_admin_command(data, sender=sender)
            if command != None:
                break
        #print(command)
        if command == str(1):
            simuse.Send_Message(data, sender, 2, '请发送需要过滤的问题', 1)
            while 1:
                question = ChatAdmin.get_admin_question(data, sender)
                if question != None:
                    break
            try:
                creatfilter(question)
            except:
                simuse.Send_Message(data, sender, 2, '添加失败', 1)
            else:
                simuse.Send_Message(data, sender, 2, '添加成功！', 1)
        elif command == str(2):
            simuse.Send_Message(data, sender, 2, '请发送敏感的关键字', 1)
            while 1:
                question = ChatAdmin.get_admin_question(data, sender)
                if question != None:
                    break
            try:
                creatsensitive(question)
            except:
                simuse.Send_Message(data, sender, 2, '添加失败', 1)
            else:
                simuse.Send_Message(data, sender, 2, '添加成功！', 1)
        elif command == str(3):
            simuse.Send_Message(data, sender, 2, '请输入需要添加黑名单的账号', 1)
            while 1:
                member = ChatAdmin.get_admin_command(data, sender=sender)
                if member != None:
                    break
            try:
                member = member.replace('，', ',')
                member = member.replace(' ', ',')
            except:
                pass
            memberlist = '[{}]'.format(member)
            try:
                memberlist = eval(memberlist)
                if type(memberlist) != type([]):
                    print('参数错误')
                    simuse.Send_Message(data, sender, 2, '参数错误', 1)
                    return None
            except:
                print('参数错误')
                simuse.Send_Message(data, sender, 2, '参数错误', 1)
                return None
            creatblack(memberlist, list=1)
            simuse.Send_Message(data, sender, 2, '添加完毕', 1)
        elif command == str(4):
            simuse.Send_Message(data, sender, 2,
                                '请输入需要查看的内容\n1.过滤的问题\n2.敏感的关键字\n3.黑名单\n4.返回',
                                1)
            while 1:
                Filterconfig = blackcheck()
                node = ChatAdmin.get_admin_command(data, sender=sender)
                if node != None:
                    break
            if node == str(1):
                filterlist = Filterconfig['filter']
                replyanswer(data, sender, filterlist)
                getnode(data, Filterconfig, filterlist, sender)
            elif node == str(2):
                sensitivelist = Filterconfig['sensitive']
                replyanswer(data, sender, sensitivelist)
                getnode(data, Filterconfig, sensitivelist, sender)
            elif node == str(3):
                blackdict = Filterconfig['blackdict']
                replyblack(data, Filterconfig, sender, blackdict)
            else:
                continue

        else:
            return None
