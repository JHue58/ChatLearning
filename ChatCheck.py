import os
import time

import simuse


def getallconfig():
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    file.close()
    config = eval(config)
    return config


def clcheck(filename, data, fromchat):
    question_num = 0
    answer_num = 0
    allanswerlist = []
    file = open(filename, 'r', encoding='utf-8-sig')
    cldict = file.read()
    file.close()
    cldict = eval(cldict)
    for i in cldict:
        question_num += 1
        questioninfo = cldict[i]
        answerlist = questioninfo['answer']
        allanswerlist.extend(answerlist)
    try:
        for i in allanswerlist:
            answer_num += 1
    except:
        pass
    group = filename[:-3]
    print('群', group, '收集到问题', question_num, '个', ' 答案', answer_num, '个')
    if fromchat != 0:
        nodedict = {
            'senderId': data['qq'],
            'time': int(time.time()),
            'senderName': 'ChatLearning',
            'messageChain': [{
                'type': 'Plain',
                'text': ''
            }]
        }
        messagechain = nodedict['messageChain']
        messagedict = messagechain[0]
        messagedict['text'] = '群' + str(group) + '收集到问题' + str(
            question_num) + '个' + ' 答案' + str(answer_num) + '个'
        return nodedict
        #simuse.Send_Message(data, fromchat, 2, '群'+str(group)+'收集到问题'+str(question_num)+'个'+' 答案'+str(answer_num)+'个', 1)
        #time.sleep(1)


def main(data, fromchat):
    filelist = os.listdir()
    cllist = []
    nodelist = []
    for i in filelist:
        if i[-3:] == '.cl':
            #print(i)
            cllist.append(i)
    #print(cllist)
    for i in cllist:
        try:
            nodedict = clcheck(i, data, fromchat)
            nodelist.append(nodedict.copy())
        except:
            pass
    config = getallconfig()
    learningtip = '记录功能：{}'
    if config['learning'] == 1:
        learningtip = learningtip.format('开启')
    else:
        learningtip = learningtip.format('关闭')
    replytip = '回复功能：{}'
    if config['reply'] == 1:
        replytip = replytip.format('开启')
    else:
        replytip = replytip.format('关闭')
    golbetip = '全局模式：{}'
    if config['sendmode'] == 1:
        golbetip = golbetip.format('开启')
    else:
        golbetip = golbetip.format('关闭')
    replychancetip = '回复触发概率：{}%'.format(config['replychance'])
    mergetimetip = '总词库合成间隔：{}秒'.format(config['mergetime'])
    intervaltip = '词库链间隔：{}秒'.format(config['interval'])
    blackfreqtip = '黑名单容错次数：{}次'.format(config['blackfreq'])
    situation = learningtip + '\n' + replytip + '\n' + golbetip + '\n' + replychancetip + '\n' + mergetimetip + '\n' + intervaltip + '\n' + blackfreqtip
    situationchain = [{'type': 'Plain', 'text': situation}]
    situationnodedict = {
        'senderId': data['qq'],
        'time': int(time.time()),
        'senderName': 'ChatLearning',
        'messageChain': [{
            'type': 'Plain',
            'text': ''
        }]
    }
    situationnodedict['messageChain'] = situationchain
    nodelist.append(situationnodedict.copy())
    if fromchat != 0:
        sendmessagechain = [{'type': 'Forward', 'nodeList': ''}]
        sendmessagedict = sendmessagechain[0]
        sendmessagedict['nodeList'] = nodelist
        simuse.Send_Message_Chain(data, fromchat, 2, sendmessagechain)
    print(situation)

    #os.system('pause')
