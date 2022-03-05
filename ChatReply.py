# Demo阶段
import random
import time
import simuse
import requests
import json
nowtime=time.time()

def talkvoice(data,group,messagechain):
    global nowtime
    atmessage=messagechain[0]
    if atmessage['type']=='At' and str(atmessage['target'])==data['qq']:
        try:
            textmessage=messagechain[1]
            text=textmessage['text']
            try:
                text=text.strip(' ')
            except:
                pass
            if text[:3]=='快说 ':
                text=text[3:]
                if len(text)>100:
                    print('超过长度限制')
                    simuse.Send_Message(data,group,1,'超过长度限制',1)
                    return None                 
                if canToVoice(text):
                    try:
                        if CanSendTask(nowtime,10):
                            answer_message=Plain_Voice(data,text)
                            if answer_message==None:
                                print('转换语音失败')
                                return None
                            simuse.Send_Message_Chain(data,group,1,answer_message)
                            nowtime=time.time()
                            return 1
                        else:
                            print('转换冷却中')
                            simuse.Send_Message(data,group,1,'能不能让我休息下喝口水再说啊？',1)
                            return 1
                    except:
                        print('转换语音失败')
                        return None
                else:
                    print('存在违规字符，转换失败')
                    simuse.Send_Message(data,group,1,'存在违规字符，转换失败',1)
                    return None
        except:
            return None
        






def canToVoice(text):
    usualchar=[',','，','.','。','!','！','?','？',' ']
    chinesehave=0
    anotherchar=0
    for i in text:
        if '\u4e00'<=i<='\u9fa5':
            chinesehave=1
        else:
            if not(i in usualchar):
                anotherchar=1
    if chinesehave==1 and anotherchar==0:
        cansign=1
    else:
        cansign=0
    return cansign

def CanSendTask(nowtime,cd):
    if time.time()-nowtime>=cd:
        return 1
    else:
        return 0


def Plain_Voice(data,text):
    url='http://124.222.165.166:19630/ToVoice'
    data_in={'text':text,'QQ':data['qq'],'synthesizer':getconfig(7)}
    try:
        res=requests.request('post',url,json=data_in)
        res=json.loads(res.text)
    except:
        return None
    if res['code']==0:
        return None
    base64_data=res['base64']
    messagechain=[{'type':'Voice','base64':base64_data}]
    return messagechain


def runchance(replychance):
    list = []
    for i in range(replychance):
        list.append(1)
    for i in range(100 - replychance):
        list.append(0)
    chance = random.choice(list)
    return chance


def getconfig(choice):
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    file.close()
    config = eval(config)
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
    elif choice==5:
        voicereply=config['voicereply']
        return voicereply
    elif choice==6:
        voicereplychance=config['voicereplychance']
        return voicereplychance
    elif choice==7:
        synthesizer_name=config['synthesizer']
        return synthesizer_name


def getanswer(group, question):  # 从词库中获取答案
    for i in question:  # 去除作为问题中的变动因素“url”
        try:
            i.pop('url')
        except:
            continue
    if getconfig(2) == 1:
        group = 'Merge'
    question = str(question)
    filename = str(group) + '.cl'  # 读取已缓存的词库
    try:
        file = open(filename, 'r', encoding='utf-8-sig')
    except:
        return None
    tempdict = file.read()
    tempdict = eval(tempdict)
    try:  # 检索问题，若词库中无该问题，则函数返回-1，若有，则返回所有答案（答案列表）
        #print(question)
        questiondict = tempdict[question]
        answerlist = questiondict['answer']
    except:
        return -1
    #print(answerlist)
    return answerlist


def replyanswer(data, group, answer):  # 发送答案
    global nowtime
    if runchance(getconfig(4)) == 0:
        print('已获取答案，但不发送')
        return None
    try:
        answer = random.choice(answer)  # 尝试从答案列表中随机抽取一个答案，若答案列表为空，则不回复
        answer = answer['answertext']
    except:
        print('无答案，不给予回复')
        #print('->',end='')
        return None
    print(answer, end='')
    try:
        answer = eval(answer)
    except:
        pass
    for i in answer:  # 去除答案中的imageId，不去除mirai api http会无法回复
        #print(i)
        try:
            i.pop('imageId')
        except:
            continue
    #print(answer)
    #Voice Test
    voicereplysign=0
    if getconfig(5)==1 and runchance(getconfig(6))==1:
        for i in answer:
            if i['type']=='Plain':
                if canToVoice(i['text']):
                    if len(i['text'])>55:
                        break
                    try:
                        if CanSendTask(nowtime,10):
                            answer_new_message=Plain_Voice(data,i['text'])
                            if answer_new_message==None:
                                print('转换语音失败')
                                break
                            answer=answer_new_message
                            voicereplysign=1
                            nowtime=time.time()
                        else:
                            break
                    except:
                        print('转换语音失败')
                    break

    
    number = simuse.Send_Message_Chain(data, group, 1,
                                       answer)  # 让bot发送随机抽取中的答案
    if number != None:
        if voicereplysign==0:
            print('答案已发送', number)
        else:
            print('答案已发送(语音)',number)
        #print('->',end='')
    else:
        print('答案发送失败')


def listening(data):
    while 1:
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
                messagechain.pop(0)
                if talkvoice(data,group,messagechain)==1:
                    continue
                question = messagechain
                answer = getanswer(group, question)  # 获取答案
                if answer != -1 and answer!=None:
                    replyanswer(data, group, answer)  # 让bot回复
        time.sleep(0.5)


def main():
    data = simuse.Get_data()
    data = simuse.Get_Session(data)
    listening(data)


#main()
