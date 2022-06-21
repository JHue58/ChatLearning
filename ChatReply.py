# Demo阶段
import copy
import json
import pickle
import random
import time
import traceback

import requests

import ChatAllfind
import ChatFilter
import simuse

nowtime = time.time()


def RandomStop():
    replywait = getconfig(15)
    StopTime=replywait[0]
    RandomArea=random.uniform(-replywait[1],replywait[1])
    print('WaitTime:{}'.format(StopTime+RandomArea))
    time.sleep(StopTime+RandomArea)





def DelType(tempdict, answerlist):
    freqdict = getconfig(10)
    num = 0
    deltype = ''
    new_answerlist = copy.deepcopy(answerlist)
    for answerdict in answerlist:
        answertext = eval(answerdict['answertext'])
        for i in answertext:
            try:
                i.pop('url')
            except:
                pass

            try:
                weight=answerdict['same']+1
            except:
                weight=1
            
            try:
                if weight < freqdict[i['type']]:
                    try:
                        questiondict = tempdict[str(answertext)]
                        if questiondict['freq'] < freqdict[i['type']]:
                            new_answerlist.remove(answerdict)
                            num += 1
                            deltype = deltype + i['type'] + ' '
                            continue
                    except:
                        new_answerlist.remove(answerdict)
                        num +=1
                        deltype = deltype + i['type'] + ' '
                        continue
                    else:
                        continue
            except:
                pass


    if num != 0:
        print('已过滤{}个不符合发送要求的{}'.format(num, ','.join(set(deltype.split()))))
    return new_answerlist


def Judge_Fast_Delete(data, TempMessage, group, messagechain, sender,messageId):
    try:
        First_index = messagechain[0]
    except:
        return 1
    IS_ME = 0
    if First_index['type'] == 'Quote':
        SourceId = First_index['id']
        for i in messagechain:
            if i['type'] == 'At':
                if str(i['target']) == data['qq']:
                    IS_ME = 1
            if i['type'] == 'Plain' and IS_ME == 1:
                if i['text'].lower() == ' !delete' or i['text'].lower(
                ) == ' ！delete' or i['text'].lower()==' !d' or i['text'].lower()==' ！d':
                    if getconfig(13) == 0:
                            if not (sender in getconfig(14)):
                                return 1                    
                    Delete_Sign = Fast_Delete(TempMessage, group, SourceId)
                    break
        else:
            return 0
        if Delete_Sign == 1:
            global RecallList
            simuse.Recall_Message(data, SourceId)
            time.sleep(1)
            RecallList.append(simuse.Send_Message(data, group, 1, getconfig(16)['deletesuccess'], 1))
        elif Delete_Sign == 0:
            RecallList.append(
                simuse.Send_Message(data, group, 1, getconfig(16)['deletetemperror'], 1))
        elif Delete_Sign == -1:
            RecallList.append(
                simuse.Send_Message(data, group, 1, getconfig(16)['deletefinderror'], 1))
        RecallList.append(messageId)
        return 1
    else:
        return 0


def Fast_Delete(TempMessage, group, SourceId):
    try:
        IDdict = TempMessage[group]
        IDlist = IDdict[SourceId]
    except:
        return 0
    filelist = ChatAllfind.getcllist()
    IS_FIND = 0
    for filename in filelist:
        THIS_IS_FIND = 0
        cldict = pickle.load(open('WordStock/' + filename, 'rb'))
        try:
            questiondict = cldict[IDlist[0]]
        except:
            continue
        answerlist = questiondict['answer']
        for answerdict in answerlist:
            if answerdict['answertext'] == IDlist[1]:
                answerlist.remove(answerdict)
                IS_FIND = 1
                THIS_IS_FIND = 1
                if answerlist == []:
                    cldict.pop(IDlist[0])
                break
        if THIS_IS_FIND == 1:
            pickle.dump(cldict, open('WordStock/' + filename, 'wb'))
    if IS_FIND == 1:
        IDdict.pop(SourceId)
        return 1
    else:
        return -1


def talkvoice(data, group, messagechain):
    global nowtime
    try:
        atmessage = messagechain[0]
    except:
        print('转换语音失败')
        return None
    if atmessage['type'] == 'At' and str(atmessage['target']) == data['qq']:
        try:
            textmessage = messagechain[1]
            text = textmessage['text']
            try:
                text = text.strip(' ')
            except:
                pass
            if text[:3] == '快说 ':
                text = text[3:]
                if len(text) > 50:
                    print('长度超过限制')
                    simuse.Send_Message(data, group, 1, getconfig(16)['voicelengtherror'], 1)
                    return None
                if canToVoice(text):
                    try:
                        if CanSendTask(nowtime, 10):
                            answer_message = Plain_Voice(data, text)
                            if answer_message == None:
                                print('转换语音失败')
                                return None
                            simuse.Send_Message_Chain(data, group, 1,
                                                      answer_message)
                            nowtime = time.time()
                            return 1
                        else:
                            print('转换冷却中')
                            simuse.Send_Message(data, group, 1,
                                                getconfig(16)['voicecderror'], 1)
                            return 1
                    except:
                        print('转换语音失败')
                        return None
                else:
                    print('存在违规字符，转换失败')
                    simuse.Send_Message(data, group, 1, getconfig(16)['voicecharerror'], 1)
                    return None
        except:
            return None


def canToVoice(text):
    usualchar = [',', '，', '.', '。', '!', '！', '?', '？', ' ']
    chinesehave = 0
    anotherchar = 0
    for i in text:
        if '\u4e00' <= i <= '\u9fa5':
            chinesehave = 1
        else:
            if not (i in usualchar):
                anotherchar = 1
    if chinesehave == 1 and anotherchar == 0:
        cansign = 1
    else:
        cansign = 0
    return cansign


def CanSendTask(nowtime, cd):
    if time.time() - nowtime >= cd:
        return 1
    else:
        return 0


def Plain_Voice(data, text):
    # 检查训练集是否在服务器中
    pturl="http://124.222.165.166:19630/Ptlist"
    try:
        ptres = requests.request('get', pturl, timeout=20)
        ptres = json.loads(ptres.text)
    except:
        return None
    ptlist = ptres['ptlist']
    if not (getconfig(7) in ptlist):
        return None

    url = 'http://124.222.165.166:19630/ToVoice'
    data_in = {'text': text, 'QQ': data['qq'], 'synthesizer': getconfig(7)}
    try:
        res = requests.request('post', url, json=data_in)
        res = json.loads(res.text)
    except:
        return None
    if res['code'] == 0:
        return None
    base64_data = res['base64']
    messagechain = [{'type': 'Voice', 'base64': base64_data}]
    return messagechain


def runchance(replychance):
    ranom_num = random.uniform(0, 1)
    replychance = replychance * 0.01
    if ranom_num <= replychance:
        chance = 1
    else:
        chance = 0
    return chance


def getconfig(choice):
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    if choice == 1:
        grouplist = config['replygrouplist']
        grouptuple = tuple(grouplist)
        return grouptuple
    elif choice == 2:
        sendmode = config['sendmode']
        return sendmode
    elif choice == 3:
        reply = config['reply']
        return reply
    elif choice == 4:
        replychance = config['replychance']
        return replychance
    elif choice == 5:
        voicereply = config['voicereply']
        return voicereply
    elif choice == 6:
        voicereplychance = config['voicereplychance']
        return voicereplychance
    elif choice == 7:
        synthesizer_name = config['synthesizer']
        return synthesizer_name
    elif choice == 8:
        Tagdict = config['tag']
        return Tagdict
    elif choice == 9:
        replydict = config['singlereplychance']
        return replydict
    elif choice == 10:
        imagefreq = config['typefreq']
        return imagefreq
    elif choice == 11:
        voicereplydict = config['singlevoicereplychance']
        return voicereplydict
    elif choice == 12:
        TempMessageNum = config['tempmessagenum']
        return TempMessageNum
    elif choice == 13:
        FastDelete = config['fastdelete']
        return FastDelete
    elif choice == 14:
        Adminlist = config['Administrator']
        return Adminlist
    elif choice == 15:
        replywait = config['replywait']
        return replywait
    elif choice == 16:
        return config


def getanswer(group, question):  # 从词库中获取答案
    for i in question:  # 去除作为问题中的变动因素“url”
        try:
            i.pop('url')
        except:
            continue
    if getconfig(2) == 1:
        Tagdict = getconfig(8)
        if str(group) in Tagdict.keys():
            group = Tagdict[str(group)]
        else:
            group = 'Merge'
    question = str(question)
    if type(group) == type([]):
        answerlist = []
        for i in group:
            filename = str(i) + '.cl'  # 读取已缓存的词库
            try:
                tempdict = pickle.load(open('WordStock/' + filename, 'rb'))
            except:
                return None
            try:  # 检索问题，若词库中无该问题，则函数返回-1，若有，则返回所有答案（答案列表）
                #print(question)
                questiondict = tempdict[question]
                answerlist.extend(
                    copy.deepcopy(DelType(tempdict, questiondict['answer'])))
            except:
                continue

    else:
        filename = str(group) + '.cl'  # 读取已缓存的词库
        try:
            tempdict = pickle.load(open('WordStock/' + filename, 'rb'))
        except:
            return None
        try:  # 检索问题，若词库中无该问题，则函数返回-1，若有，则返回所有答案（答案列表）
            #print(question)
            questiondict = tempdict[question]
            answerlist = DelType(tempdict, questiondict['answer'])
        except:
            return -1

    #print(answerlist)
    if answerlist == []:
        return -1
    return answerlist


def replyanswer(data, group, answer):  # 发送答案
    global nowtime
    replydict = getconfig(9)
    if str(group) in replydict.keys():
        if runchance(replydict[str(group)]) == 0:
            print('已获取答案，但不发送')
            return None
    elif runchance(getconfig(4)) == 0:
        print('已获取答案，但不发送')
        return None

    try:
        answer = random_weight(answer)  # 尝试从答案列表中随机抽取一个答案，若答案列表为空，则不回复
        answer = answer['answertext']
    except:
        print('无答案，不给予回复')
        #print('->',end='')
        return None
    try:
        answer = eval(answer)
    except:
        pass
    origin_answer = copy.deepcopy(answer)
    for i in answer:  # 去除答案中的imageId，不去除mirai api http会无法回复
        #print(i)
        try:
            i.pop('imageId')
        except:
            continue
    #print(answer)
    #Voice Test
    voicereplysign = 0
    chance_True = 0
    if ChatFilter.filtercheck(copy.deepcopy(answer)) == 0:
        return None
    print(answer, end='')

    if getconfig(5) == 1:
        voicereplydict = getconfig(11)
        if str(group) in voicereplydict.keys():
            if runchance(voicereplydict[str(group)]) == 1:
                chance_True = 1
        elif runchance(getconfig(6)) == 1:
            chance_True = 1
    if chance_True == 1:
        for i in answer:
            if i['type'] == 'Plain':
                if canToVoice(i['text']):
                    if len(i['text']) > 55:
                        break
                    try:
                        if CanSendTask(nowtime, 10):
                            answer_new_message = Plain_Voice(data, i['text'])
                            if answer_new_message == None:
                                print('转换语音失败')
                                break
                            answer = answer_new_message
                            voicereplysign = 1
                            nowtime = time.time()
                        else:
                            break
                    except:
                        print('转换语音失败')
                    break

    # 添加随机阻塞，增加真实感
    if voicereplysign==0:
        RandomStop()

    number = simuse.Send_Message_Chain(data, group, 1,
                                       answer)  # 让bot发送随机抽取中的答案
    if number != None:
        if voicereplysign == 0:
            print('答案已发送', number)
            return origin_answer, number
        else:
            print('答案已发送(语音)', number)
            return origin_answer, number
        #print('->',end='')
    else:
        print('答案发送失败')


# 以same作为权重选择
def random_weight(answerlist):

    same_weight_multiple = 1 # 权重乘值
    same_weight_plus = 1 # 权重加值

    same_list=[]
    for answerdict in answerlist:
        try:
            same_list.append((answerdict["same"]+same_weight_plus)*same_weight_multiple)
        except:
            same_list.append((0+same_weight_plus)*same_weight_multiple)
    answer = random.choices(answerlist,weights=same_list,k=1)[0]
    # print("权重选择器选择：",answer)
    if answer!=None:
        return answer
    else:
        return random.choice(answerlist)


def listening(data):
    global RecallList
    RecallList = []
    AfterSecond = 0
    TempMessage = {}
    while 1:
        if RecallList != []:
            AfterSecond += 1
        if RecallList != [] and AfterSecond >= 10:
            for messageid in RecallList:
                simuse.Recall_Message(data, messageid)
            AfterSecond = 0
            RecallList = []
        if getconfig(3) == 0:
            return None
        message = simuse.Fetch_Message(data)  # 监听消息链
        if type(message) == type(0):
            time.sleep(0.5)
            continue
        for i in message:
            if i['type'] == 'GroupMessage':  # 判断监听到的消息是否为群消息
                group = i['group']  # 记录群号
                try:
                    getconfig(1).index(group)
                except:
                    continue
                messagechain = i['messagechain']
                messageSource = messagechain[0]
                messageId = messageSource['id']
                messagechain.pop(0)
                if talkvoice(data, group, messagechain) == 1:
                    continue
                if Judge_Fast_Delete(data, TempMessage, group, messagechain,
                                     i['sender'],messageId) == 1:
                    continue
                question = messagechain
                answer = getanswer(group, question)  # 获取答案
                if answer != -1 and answer != None:
                    reply_answer_info = replyanswer(data, group,
                                                    answer)  # 让bot回复
                    if reply_answer_info != None:
                        reply_answer = reply_answer_info[0]
                        SourceId = reply_answer_info[1]
                        if reply_answer != None:
                            try:
                                IDdict = TempMessage[group]
                                # TempMessage:{group:{id:[question,answer],id:[question,answer]}}
                            except:
                                IDlist = [str(question), str(reply_answer)]
                                IDdict = {}
                                IDdict[SourceId] = IDlist
                                TempMessage[group] = IDdict
                            else:
                                IDlist = [str(question), str(reply_answer)]
                                IDdict[SourceId] = IDlist
                                if len(IDdict) > getconfig(12):
                                    IDdict.pop(list(IDdict.keys())[0])
        time.sleep(0.5)


def main():
    data = simuse.Get_data()
    if data["Key"] != "":
        data = simuse.Get_Session(data)
    listening(data)
    return None


#main()
