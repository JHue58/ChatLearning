# Demo阶段
import copy
import json
import pickle
import random
import time
import traceback
from jieba import setLogLevel,cut,logging,set_dictionary
setLogLevel(logging.INFO)
set_dictionary('dict.txt')
from numpy import linalg , zeros ,dot 
import re

import requests

import ChatAllfind
import ChatClass
import ChatFilter
import simuse
from ChatClass import json_dump, json_load, pickle_dump, pickle_load
from functools import wraps

nowtime = time.time()
max_cosmath_length = 50


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        print('-----Cosmatch INFO Start-----')
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("%s: %.5f seconds" %('消耗用时', t1-t0))
        print('-----Cosmatch INFO End-----')
        return result
    return function_timer


def RandomStop():
    replywait = getconfig(15)
    StopTime = replywait[0]
    RandomArea = random.uniform(-replywait[1], replywait[1])
    print('WaitTime:{}'.format(StopTime + RandomArea))
    time.sleep(StopTime + RandomArea)


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
                weight = answerdict['same'] + 1
            except:
                weight = 1

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
                        num += 1
                        deltype = deltype + i['type'] + ' '
                        continue
                    else:
                        continue
            except:
                pass

    if num != 0:
        print('已过滤{}个不符合发送要求的{}'.format(num, ','.join(set(deltype.split()))))
    return new_answerlist


def Judge_Fast_Delete(data, TempMessage, group, messagechain, sender,
                      messageId):
    global RecallList
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
                ) == ' ！delete' or i['text'].lower(
                ) == ' !d' or i['text'].lower() == ' ！d':
                    if getconfig(13) == 0:
                        if not (sender in getconfig(14)):
                            return 1
                    Delete_Sign = Fast_Delete(TempMessage, group, SourceId)
                    break
        else:
            return 0
        if Delete_Sign == 1:
            simuse.Recall_Message(data, SourceId)
            time.sleep(1)
            RecallList.append(
                simuse.Send_Message(data, group, 1,
                                    getconfig(16)['deletesuccess'], 1))
        elif Delete_Sign == 0:
            RecallList.append(
                simuse.Send_Message(data, group, 1,
                                    getconfig(16)['deletetemperror'], 1))
        elif Delete_Sign == -1:
            RecallList.append(
                simuse.Send_Message(data, group, 1,
                                    getconfig(16)['deletefinderror'], 1))
        RecallList.append(messageId)
        return 1

    elif First_index['type'] == 'Plain':
        for i in messagechain:
            if i['type'] == 'Plain':
                if i['text'][:2].lower() == '!d' or i['text'][:2].lower(
                ) == '！d':
                    if getconfig(13) == 0:
                        if not (sender in getconfig(14)):
                            return 1

                    try:
                        MessageNum = int(i['text'][3:])
                        IDdict = TempMessage[group]
                    except:
                        return 0

                    try:
                        SourceId = list(IDdict.keys())[-MessageNum]
                        Delete_Sign = Fast_Delete(TempMessage, group, SourceId)
                    except:
                        Delete_Sign = 0

                    break
        else:
            return 0
        if Delete_Sign == 1:
            simuse.Recall_Message(data, SourceId)
            time.sleep(1)
            RecallList.append(
                simuse.Send_Message(data, group, 1,
                                    getconfig(16)['deletesuccess'], 1))
        elif Delete_Sign == 0:
            RecallList.append(
                simuse.Send_Message(data, group, 1,
                                    getconfig(16)['deletetemperror'], 1))
        elif Delete_Sign == -1:
            RecallList.append(
                simuse.Send_Message(data, group, 1,
                                    getconfig(16)['deletefinderror'], 1))
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
        cldict = pickle_load(open('WordStock/' + filename, 'rb'))
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
            pickle_dump(cldict, open('WordStock/' + filename, 'wb'))
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

            voiceCommand = getconfig(16)['voicecommand']
            if text[:len(voiceCommand)] == voiceCommand:
                text = text[len(voiceCommand):]
                if len(text) > 50:
                    print('长度超过限制')
                    simuse.Send_Message(data, group, 1,
                                        getconfig(16)['voicelengtherror'], 1)
                    return None
                try:
                    text = textChange(text)
                except Exception as e:
                    print(e)
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
                                                getconfig(16)['voicecderror'],
                                                1)
                            return 1
                    except:
                        print('转换语音失败')
                        return None
                else:
                    print('存在违规字符，转换失败')
                    simuse.Send_Message(data, group, 1,
                                        getconfig(16)['voicecharerror'], 1)
                    return None
        except:
            return None


def textChange(text: str):

    usualchar = list('，？！~·.?!-')
    usualchar_2 = list('（）()《》<>“”‘’' + "'" + '"')
    num = {
        '0': '零',
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六',
        '7': '七',
        '8': '八',
        '9': '九'
    }

    for i in usualchar:
        text = text.replace(i, ',')
    for i in usualchar_2:
        text = text.replace(i, '')
    for i in num.keys():
        text = text.replace(i, num[i])

    return text


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
    pturl = "http://124.222.165.166:19630/Ptlist"
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


def getconfig(choice=16):
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json_load(file)
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
    #是否为文字标志
    IS_Plain = False
    question_text = None
    question_str = None
    for i in question:  # 去除作为问题中的变动因素“url”
        if i['type']=='Plain':
            IS_Plain = True
        try:
            i.pop('url')
        except:
            continue
    if IS_Plain == True:
        for i in question:
            if i['type'] == 'Plain':
                question_text = i['text']
                break

    
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
                return None,question_str
            try:  # 检索问题，若词库中无该问题，则函数返回-1，若有，则返回所有答案（答案列表）
                #print(question)
                questiondict = tempdict[question]
                answerlist.extend(
                    copy.deepcopy(DelType(tempdict, questiondict['answer'])))
            except KeyError:
                if IS_Plain == True:
                    question_str = regular_mate(tempdict,question_text)
                    if question_str == None and getconfig()['cosmatch']==1 and len(question_text)<=max_cosmath_length:
                        question_str = get_answer_vector(tempdict,question_text)
                    if question_str!=None:
                        questiondict = tempdict[question_str]
                        answerlist.extend(copy.deepcopy(DelType(tempdict, questiondict['answer'])))
                continue
            except Exception as e:
                print(e)
                continue

    else:
        filename = str(group) + '.cl'  # 读取已缓存的词库
        try:
            tempdict = pickle.load(open('WordStock/' + filename, 'rb'))
        except:
            return None,question_str
        try:  # 检索问题，若词库中无该问题，则函数返回-1，若有，则返回所有答案（答案列表）
            #print(question)
            questiondict = tempdict[question]
            answerlist = DelType(tempdict, questiondict['answer'])
        except KeyError:
            if IS_Plain == True:
                question_str = regular_mate(tempdict,question_text)
                if question_str == None and getconfig()['cosmatch']==1 and len(question_text)<=max_cosmath_length:
                    question_str = get_answer_vector(tempdict,question_text)
                if question_str!=None:
                    questiondict = tempdict[question_str]
                    answerlist=DelType(tempdict, questiondict['answer'])
                else:
                    return -1,question_str
            else:
                return -1,question_str
        
        except Exception as e:
            print(e)
            return -1,question_str

    #print(answerlist)
    if answerlist == []:
        return -1,question_str
    return answerlist,question_str


def replyanswer(data, group, answer,Atme_Config,sender):  # 发送答案
    global nowtime
    sender_name = simuse.Get_memberinfo(data,group,sender)['memberName']
    replydict = getconfig(9)
    if str(group) in replydict.keys():
        if runchance(replydict[str(group)]) == 0 and Atme_Config[0]!=1:
            print('已获取答案，但不发送')
            return None
    elif runchance(getconfig(4)) == 0 and Atme_Config[0]!=1:
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

    for i in answer:
        if i['type'] == 'Plain':
            i['text'] = i['text'].format(me=random.choice(getconfig(16)['botname']),name=sender_name,segment='\n')
            if len(i['text'])>getconfig(16)['replylength']:
                print('答案字数超过所设定字数,取消发送')
                return None
    
    


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
    if voicereplysign == 0:
        RandomStop()

    if Atme_Config[0] == 1:
        answer.insert(0,{'type':'At','target':Atme_Config[2]})
        answer.insert(1,{'type':'Plain','text':'\n'})
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

    same_weight_multiple = 1  # 权重乘值
    same_weight_plus = 1  # 权重加值

    same_list = []
    for answerdict in answerlist:
        try:
            same_list.append(
                (answerdict["same"] + same_weight_plus) * same_weight_multiple)
        except:
            same_list.append((0 + same_weight_plus) * same_weight_multiple)
    answer = random.choices(answerlist, weights=same_list, k=1)[0]
    # print("权重选择器选择：",answer)
    if answer != None:
        return answer
    else:
        return random.choice(answerlist)


def regular_mate(cldict,question_text):

    regular_dict={}
    question = None
    regular_flag = False

    try:
        for i in cldict:
            question_dict = cldict[i]
            if question_dict['regular'] == True:
                regular_dict[i] = copy.deepcopy(question_dict)
    except KeyError:
        print('词库版本不匹配')
        return question
    
    if regular_dict == {}:
        return question
    
    for i in regular_dict:
        if regular_flag == True:
            break
        eval_i = eval(i)
        for k in eval_i:
            if k['type']=='Plain':
                if re.search(k['text'],question_text)!=None:
                    question = i
                    print('正则匹配的问题',question)
                    regular_flag = True
                    break

    return question




@fn_timer
def get_answer_vector(cldict,question_text):

    cos_dict={}
    set_cosmatching = getconfig()['cosmatching']

    for i in cldict:
        eval_i = eval(i)
        for k in eval_i:
            if k['type'] == 'Plain' and cldict[i]['regular'] == False:
                if len(k['text'])>max_cosmath_length:
                    continue
                matching = get_word_vector(k['text'],question_text)
                if matching >= set_cosmatching:
                    cos_dict[i] = matching
                continue

    if cos_dict == {}:
        print('相似度计算引擎未找到相关问题(小于设定阈值{})'.format(set_cosmatching))
        return None

    question = max(cos_dict,key=cos_dict.get)

    cosmatching = max(cos_dict.values())
    

    if cosmatching==0:
        print('相似度计算引擎未找到相关问题')
        return None
    else:
        print('匹配的问题：',question)
        print('句子相似度：',cosmatching)
        return question


    






def get_word_vector(s1,s2):
    s1 = s1.strip()
    s2 = s2.strip()
    #print(s1,s2)
    pun_list = ['。', '，', '、', '？','?', '！','!', '；', '：', '“', '”', '‘', '’', '「', '」', '『', '』', '（', '）', '[', ']',
                        '〔', '〕', '【', '】', '——', '—', '……', '…', '—', '-', '～', '·', '《', '》', '〈', '〉', '﹏﹏', '___',
                        '.']
    cut1 = [w for w in list(cut(s1, cut_all=False)) if w not in pun_list]
    cut2 = [w for w in list(cut(s2, cut_all=False)) if w not in pun_list]


    # 分词
    #cut1 = cut(s1)
    #cut2 = cut(s2)
    list_word1 = (','.join(cut1)).split(',')
    list_word2 = (','.join(cut2)).split(',')
 
    # 列出所有的词,取并集
    key_word = list(set(list_word1 + list_word2))
    # 给定形状和类型的用0填充的矩阵存储向量
    word_vector1 = zeros(len(key_word))
    word_vector2 = zeros(len(key_word))
 
    # 计算词频
    # 依次确定向量的每个位置的值
    for i in range(len(key_word)):
        # 遍历key_word中每个词在句子中的出现次数
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1
 
    # 输出向量
    #print(word_vector1)
    #print(word_vector2)
    return cos_dist(word_vector1, word_vector2)
 
 
 
def cos_dist(vec1,vec2):
    dist1=float(dot(vec1,vec2)/(linalg.norm(vec1)*linalg.norm(vec2)))
    return dist1
 
def filter_html(html):
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub('',html).strip()
    return dd

def AtMe(data,messagechain,sender):

    atmessage = {}
    for i in messagechain:
        if i['type'] == 'At' and str(i['target']) == data['qq']:
            atmessage = i
        if i['type'] == 'Plain':
            i['text'] = i['text'].strip()
        if i['type'] == 'Quote':
            i = {'type':'Plain','text':''}
    if atmessage == {}:
        return None,messagechain,sender
    messagechain.remove(atmessage)
    return 1,messagechain,sender



def listening(data):
    global RecallList
    ReplyCd = {}
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
        if getconfig(3) == 0 or ChatClass.stop_run():
            return None
        message = simuse.Fetch_Message(data)  # 监听消息链
        if type(message) == type(0):
            time.sleep(0.5)
            continue
        for i in message:
            if i['type'] == 'GroupMessage':  # 判断监听到的消息是否为群消息
                group = i['group']  # 记录群号
                sender = i['sender']
                try:
                    getconfig(1).index(group)
                except:
                    continue

                # Cd检测
                try:
                    GroupTime = ReplyCd[group]
                    now_time = int(time.time())
                    cd = getconfig(16)['replycd']
                    if now_time - GroupTime < cd:
                        print('群{}处于回复冷却中,剩余{}秒'.format(
                            group, cd - now_time + GroupTime))
                        continue
                except:
                    pass

                

                messagechain = i['messagechain']
                messageSource = messagechain[0]
                messageId = messageSource['id']
                messagechain.pop(0)
                if talkvoice(data, group, messagechain) == 1:
                    continue
                if Judge_Fast_Delete(data, TempMessage, group, messagechain,
                                     i['sender'], messageId) == 1:
                    continue

                Atme_Config = AtMe(data,messagechain,sender)

                if Atme_Config[0] == 1:
                    messagechain = Atme_Config[1]
                    
                question = messagechain
                answer_info = getanswer(group, question)  # 获取答案

                answer = answer_info[0]
                if answer_info[1]!=None:
                    question = answer_info[1]

                if answer != -1 and answer != None:
                    reply_answer_info = replyanswer(data, group,
                                                    answer,Atme_Config,sender)  # 让bot回复
                    if reply_answer_info != None:
                        # 发送成功后开始计算Cd
                        ReplyCd[group] = int(time.time())
                        
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
