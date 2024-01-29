# Demo阶段
import copy
import json
import pickle
import time
from datetime import datetime
from dateutil.tz import tzlocal
from re import I

import ChatAdmin
import ChatClass
import ChatFilter
import ChatMerge
import simuse
from ChatClass import json_dump, json_load, pickle_dump, pickle_load


def getconfig():

    config = json_load('config.clc')

    learning = config['learning']
    interval = config['interval']
    grouplist = config['learninggrouplist']
    interval = int(interval)
    learning = int(learning)
    return interval, learning, grouplist


def creatquestion(question, group):  # 记录问题
    #print("old")
    tempquestion = copy.deepcopy(
        question)  #作为问题，不需要“url”标签，所以对消息链(list)进行深拷贝备用
    for i in question:  # 去除作为问题中的变动因素“url”
        try:
            i.pop('url')
        except:
            continue

    question = str(question)
    filename = str(group) + ".cl"
    try:  # 读取已缓存的词库
        tempdict = pickle.load(open('WordStock/' + filename, 'rb'))
    except:
        tempdict = {}
    if not (question in tempdict.keys()):  # 判断词库中问题是否存在，若不存在则记录问题
        questiondict = {}
        questiontime = int(time.time())
        answerlist = []
        questiondict["freq"] = 1
        questiondict["time"] = questiontime
        questiondict["answer"] = answerlist
        questiondict['regular'] = False
        tempdict[question] = questiondict
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n问题已记录",
              filename)
    else:
        questiondict = tempdict[question]
        questiondict["freq"] += 1
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              "\n相同问题 已记录重复", filename)
    #print(tempdict)
    pickle_dump(tempdict, 'WordStock/' + filename)
    return tempquestion  # 返回未去除“url”的消息链，为记录答案做准备


def creatanswer(question, answer, group):  # 记录答案
    #print("new")
    #os.system("pause")
    for i in question:  # 去除作为问题中的变动因素“url”
        try:
            i.pop('url')
        except:
            continue
    question = str(question)
    answer = str(answer)
    filename = str(group) + ".cl"
    tempdict = pickle_load('WordStock/' + filename)  # 读取缓存的词库
    # answertime = int(time.time())
    local_tz = tzlocal()  # 获取系统本地时区
    answertime = datetime.now().astimezone(local_tz)
    answerdict = {"answertext": "", "time": ""}
    answerdict["answertext"] = answer
    answerdict["time"] = answertime
    tempanswerdict = copy.deepcopy(answerdict)
    tempanswerdict['answertext'] = eval(tempanswerdict['answertext'])
    questiondict = {}
    if question:
        questiondict = tempdict[question]# 找到问题，将答案添加进“answer”属性
        #print(questiondict["answer"])
        if str(questiondict.get("answer")) != '[]':  # 判断答案列表是否为空
            isbreak = 0
            for i in questiondict["answer"]:  # 答案列表不为空则寻找相同的答案，有相同则记录相同次数'same'，无相同则记录新答案
                tempi = copy.deepcopy(i)
                tempi['answertext'] = eval(tempi['answertext'])
                #print(tempi)
                for k in tempanswerdict['answertext']:  # 去除作为答案中的变动因素"url"
                    #print(k)
                    try:
                        k.pop('url')
                    except:
                        continue
                for k in tempi['answertext']:  # 去除作为答案中的变动因素"url"
                    #print(k)
                    try:
                        k.pop('url')
                    except:
                        continue
                #print(tempi['answertext'])
                #print(tempanswerdict['answertext'])
                if tempi['answertext'] == tempanswerdict['answertext']:  # 判断答案是否相同
                    i['time'] = answerdict['time']
                    if not ('same' in i.keys()):  # 检测是否记录过相同次数，有则+1，无则记录相同次数为1
                        i['same'] = 1
                    else:
                        i['same'] += 1
                    print('检测到答案重复，重复次数已记录', end='')  # 相同则记录相同，然后结束循环，将循环结束判断符置1
                    isbreak = 1
                    break
            if isbreak == 0:  # 只有遍历完整个答案list无相同，才会记录
                questiondict["answer"].append(answerdict.copy())
        else:  # 答案列表为空时一定是新答案，所以直接记录
            questiondict["answer"].append(answerdict.copy())
        tempdict[question] = questiondict
        pickle_dump(tempdict, 'WordStock/' + filename)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n答案已记录",
            filename)


def extractmessage(data, tempdict):  # 将消息链转化为字典格式（key为群号，value为消息链）
    message = simuse.Fetch_Message(data)  # 监听消息链
    if type(message) == type(0):
        return tempdict
    for i in message:
        if i['type'] == 'GroupMessage':  # 判断监听到的消息是否为群消息
            try:
                if not (i['group'] in getconfig()[2]):
                    continue
            except:
                pass
            checkmessage = copy.deepcopy(i['messagechain'])
            checkmessage.pop(0)
            if ChatFilter.sensitivecheck(checkmessage, i['sender'],
                                         i['group']) == 0:
                continue
            elif ChatFilter.filtercheck(checkmessage, i['sender'],
                                        i['group']) == 0:
                continue

            if i['group'] in tempdict.keys():
                #tempdict[i['group']]=[]
                messagechain = i['messagechain']
                #messagechain.pop(0)
                tempdict[i['group']].append(messagechain)
            else:
                tempdict[i['group']] = []
                messagechain = i['messagechain']
                #messagechain.pop(0)
                tempdict[i['group']].append(messagechain)
    return tempdict


def listening(data):
    textdict = {}
    sign = {}  # 创建一个字典，用来标记第一个记录的问题，即标记“1”
    while 1:
        config = getconfig()
        interval = config[0]
        if config[1] == 0 or ChatClass.stop_run():
            return None
        #print(sign)
        textdict = {}
        textdict = extractmessage(data, textdict)  # 不同群的消息链对应存储
        #print(textdict)
        #file=open('texttemp.cl','w',encoding='utf-8-sig')
        #file.write(str(textdict))
        #file.close()
        for i in textdict:  # 遍历群号
            if not (i in sign.keys()):  # 若有新的群号，将收集到的第一个消息标记“1”
                sign[i] = {"id": "", "signtime": 0, "befor": ""}
            for k in textdict[i]:  # 开始记录问题
                messagesign = sign[i]
                messagechain = k
                messageinfo = messagechain[0]  # 获取消息链的信息属性（消息id和时间戳）
                messagechain.pop(0)
                if messageinfo['time'] - messagesign[
                        "signtime"] > interval:  # 若相同群，收集到的两个消息的间隔大于900秒，则新的消息重新标记“1”
                    #print(messageinfo['time'])
                    #os.system("pause")
                    messagesign["id"] = messageinfo['id']  # 将该消息重新标记“1”
                if messageinfo['id'] == messagesign["id"]:  # 将标记“1”的消息，记录为问题
                    creatquestion(messagechain, i)  # 记录问题
                    #print('->',end='')
                    messagesign["signtime"] = messageinfo['time']
                    messagesign["befor"] = messagechain  # 将该消息标记为“上一个问题”
                else:  # 剩下的问题，记录为上一个问题的答案和新的问题
                    #print(messagechain)
                    messagechain = creatquestion(messagechain, i)  # 记录问题
                    #print(messagechain)
                    creatanswer(messagesign["befor"], messagechain, i)  # 记录答案
                    #print('->',end='')
                    messagesign["signtime"] = messageinfo['time']  # 更新消息的时间戳
                    messagesign["befor"] = messagechain  # 将该消息标记为“上一个问题”
                sign[i] = messagesign

        time.sleep(0.5)


def custom_answer(data, fromchat):
    cl_file_text = '拥有的词库:\n'
    cl_list = ChatAdmin.getfilelist()
    for i in cl_list:
        cl_file_text += i + '\n'
    simuse.Send_Message(data, fromchat, 2, cl_file_text, 1)
    time.sleep(0.5)
    simuse.Send_Message(data, fromchat, 2, "请输入需要新增回复的词库昵称(不存在将会新建词库)", 1)
    while True:
        filename = ChatAdmin.get_admin_command(data, sender=fromchat)
        if filename != None:
            break
        time.sleep(0.5)

    filename += '.cl'
    have_cl = True

    try:
        cldict = pickle.load(open('WordStock/' + filename, 'rb'))
    except:
        time.sleep(0.5)
        simuse.Send_Message(data, fromchat, 2, "词库不存在，将被创建", 1)
        have_cl = False
        cldict = {}

    while True:
        time.sleep(0.5)
        simuse.Send_Message(data, fromchat, 2, "请输入问题", 1)
        while True:
            question = ChatAdmin.get_admin_question(data, fromchat)
            if question != None:
                break
            time.sleep(0.5)

        for i in question:
            try:
                i.pop('url')
            except:
                pass

        have_question = True
        try:
            questiondict = cldict[str(question)]
            answerlist = questiondict['answer']
        except:
            if have_cl:
                time.sleep(0.5)
                simuse.Send_Message(data, fromchat, 2, "问题不存在，将被创建", 1)
            time.sleep(0.2)
            simuse.Send_Message(data, fromchat, 2,
                                "该问题是否为正则表达式?\n0.否\n1.是", 1)
            while True:
                command = ChatAdmin.get_admin_command(data, sender=fromchat)
                if command != None:
                    break            
            if command == '1':
                regular = True
                simuse.Send_Message(data, fromchat, 2, "问题将被判定为正则表达式", 1)
            else:
                regular = False
                simuse.Send_Message(data, fromchat, 2, "问题将被判定为非正则表达式", 1)
            answerlist = []
            questiondict = {
                'time': int(time.time()),
                'answer': answerlist,
                'freq': 9999,
                'regular':regular
            }
            have_question = False

        while True:
            time.sleep(0.5)
            simuse.Send_Message(data, fromchat, 2, "请输入答案", 1)
            while True:
                answer = ChatAdmin.get_admin_question(data, fromchat)
                if answer != None:
                    break
            time.sleep(0.5)
            simuse.Send_Message(data, fromchat, 2,
                                "请输入答案的权重(这是一个非负的整数,越大表明抽中该答案的概率越大)", 1)
            while True:
                while True:
                    weight = ChatAdmin.get_admin_command(data, sender=fromchat)
                    if weight != None:
                        break
                    time.sleep(0.5)
                try:
                    weight = int(weight)
                except:
                    simuse.Send_Message(data, fromchat, 2,
                                        "权重必须是一个非负的整数，请重新输入", 1)
                    continue
                if weight < 0:
                    simuse.Send_Message(data, fromchat, 2,
                                        "权重必须是一个非负的整数，请重新输入", 1)
                    continue
                break

            if have_question:
                for answerdict in answerlist:
                    if answerdict["answertext"] == str(answer):
                        answerdict['same'] = weight
                        time.sleep(0.5)
                        simuse.Send_Message(data, fromchat, 2,
                                            "问题中已存在该答案，已将权重修改为新值", 1)
                        break
                else:
                    answerdict = {
                        'answertext': str(answer),
                        'time': int(time.time()),
                        'same': weight
                    }
                    answerlist.append(answerdict)
                    time.sleep(0.5)
                    simuse.Send_Message(data, fromchat, 2, "添加完毕！", 1)
            else:
                answerdict = {
                    'answertext': str(answer),
                    'time': int(time.time()),
                    'same': weight
                }
                answerlist.append(answerdict)
                cldict[str(question)] = questiondict

                time.sleep(0.5)
                simuse.Send_Message(data, fromchat, 2, "添加完毕！", 1)

            pickle_dump(cldict, 'WordStock/' + filename)

            time.sleep(0.5)
            simuse.Send_Message(data, fromchat, 2,
                                "请选择：\n0.退出\n1.为该问题继续添加答案\n2.为该词库添加新的问答", 1)
            while True:
                command = ChatAdmin.get_admin_command(data, sender=fromchat)
                if command != None:
                    break

            if command == str(0):
                ChatMerge.getfile()
                return None
            elif command == str(1):
                continue
            elif command == str(2):
                break


def main():
    data = simuse.Get_data()
    if data["Key"] != "":
        data = simuse.Get_Session(data)
    listening(data)
    return None


#main()

#{
#    "question text":{"time":"","answer":[{"answer text":"","time":""},{"answer text":"","time":""}]}
#}

#词库的缓存格式
