import json
import os
import pickle
import time
from wsgiref.simple_server import server_version

import requests

import simuse
from ChatClass import Version, json_dump, json_load, pickle_dump, pickle_load


def getallconfig():
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json_load(file)
    file.close()
    return config


def checkversion():
    url = 'http://124.222.165.166:19630/Update'
    try:
        res = requests.request('get', url=url, timeout=20)
        res = json.loads(res.text)
    except:
        return None
    now_version = int(Version().replace('.', ''))
    server_version = int(res['version'].replace('.', ''))
    if server_version > now_version:
        return 1, res['version'], Version()
    else:
        return 0, Version()


def clcheck(filename, data, fromchat):
    question_num = 0
    answer_num = 0
    allanswerlist = []
    cldict = pickle_load(open('WordStock/' + filename, 'rb'))
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
    config = getallconfig()
    Tagdict = config['tag']
    group = filename[:-3]
    try:
        print('词库', group, '收集到问题', question_num, '个', ' 答案', answer_num, '个',
              'Tag:{}'.format(' '.join(Tagdict[group])))
    except:
        print('词库', group, '收集到问题', question_num, '个', ' 答案', answer_num, '个')
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
        try:
            messagedict['text'] = '词库' + str(group) + '收集到问题' + str(
                question_num) + '个' + ' 答案' + str(
                    answer_num) + '个' + '\nTag:{}'.format(' '.join(
                        Tagdict[group]))
        except:
            messagedict['text'] = '词库' + str(group) + '收集到问题' + str(
                question_num) + '个' + ' 答案' + str(answer_num) + '个'
        return nodedict
        #simuse.Send_Message(data, fromchat, 2, '群'+str(group)+'收集到问题'+str(question_num)+'个'+' 答案'+str(answer_num)+'个', 1)
        #time.sleep(1)


def main(data, fromchat):
    filelist = os.listdir('WordStock')
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
    voicereplytip = '文字转语音回复功能：{}'
    if config['voicereply'] == 1:
        voicereplytip = voicereplytip.format('开启')
    else:
        voicereplytip = voicereplytip.format('关闭')
    golbetip = '全局模式：{}'
    if config['sendmode'] == 1:
        golbetip = golbetip.format('开启')
    else:
        golbetip = golbetip.format('关闭')
    replychancetip = '回复触发概率：{}%'.format(config['replychance'])
    replywaittip = '回复等待时间：{:g}±{:g}秒'.format(config['replywait'][0],
                                              config['replywait'][1])
    replycdtip = '回复冷却时间：{}秒'.format(config['replycd'])
    voicereplychancetip = '语音回复触发概率：{}%'.format(config['voicereplychance'])
    try:
        synthesizertip = '训练集：{}'.format(config['synthesizer'])
    except:
        synthesizertip = '训练集：无'
    mergetimetip = '总词库合成间隔：{}秒'.format(config['mergetime'])
    intervaltip = '词库链间隔：{}秒'.format(config['interval'])
    blackfreqtip = '黑名单容错次数：{}次'.format(config['blackfreq'])
    tempmessagenumtip = '单个群最大消息缓存数：{}条'.format(config['tempmessagenum'])
    typefreqtip = '回复阈值设定：\n'
    singlereplytip = '指定群回复触发概率：\n'
    singlevoicereplytip = '指定群回复概率（语音）：\n'
    typefreqdict = config['typefreq']
    replydict = config['singlereplychance']
    voicereplydict = config['singlevoicereplychance']
    if replydict == {}:
        singlereplytip = ''
    if voicereplydict == {}:
        singlevoicereplytip = ''
    if typefreqdict == {}:
        typefreqtip = ''
    for i in typefreqdict:
        typefreqtip = typefreqtip + '{}:{}次\n'.format(i, typefreqdict[i])
    for i in replydict:
        singlereplytip = singlereplytip + '群{}：{}%\n'.format(i, replydict[i])
    for i in voicereplydict:
        singlevoicereplytip = singlevoicereplytip + '群{}：{}%\n'.format(
            i, voicereplydict[i])
    check_version = checkversion()
    if check_version[0] == 1:
        versiontip = "已连接至ChatLearning服务器\n检测到有新版本：{}\n当前版本：{}".format(
            check_version[1], check_version[2])
    elif check_version[0] == 0:
        versiontip = "已连接至ChatLearning服务器\n当前已是最新版本：{}".format(
            check_version[1])
    else:
        versiontip = "未连接至ChatLearning服务器"
    situation = learningtip + '\n' + replytip + '\n' + voicereplytip + '\n' + golbetip + '\n' + replychancetip + '\n' + replywaittip + '\n' + replycdtip + '\n' + voicereplychancetip + '\n' + synthesizertip + '\n' + mergetimetip + '\n' + intervaltip + '\n' + blackfreqtip + '\n' + tempmessagenumtip
    situationchain = [{'type': 'Plain', 'text': situation}]
    typefreq_message = [{'type': 'Plain', 'text': typefreqtip}]
    siglereply_message = [{'type': 'Plain', 'text': singlereplytip}]
    singlevoicereply_message = [{'type': 'Plain', 'text': singlevoicereplytip}]
    version_message = [{'type': 'Plain', 'text': versiontip}]
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
    situationnodedict['messageChain'] = typefreq_message
    nodelist.append(situationnodedict.copy())
    situationnodedict['messageChain'] = siglereply_message
    nodelist.append(situationnodedict.copy())
    situationnodedict['messageChain'] = singlevoicereply_message
    nodelist.append(situationnodedict.copy())
    situationnodedict['messageChain'] = version_message
    nodelist.append(situationnodedict.copy())
    if fromchat != 0:
        sendmessagechain = [{'type': 'Forward', 'nodeList': ''}]
        sendmessagedict = sendmessagechain[0]
        sendmessagedict['nodeList'] = nodelist
        simuse.Send_Message_Chain(data, fromchat, 2, sendmessagechain)
    print(
        situation, '\n' + typefreqtip + '\n' + singlereplytip + '\n' +
        singlevoicereplytip + '\n' + versiontip)
    return None

    #os.system('pause')
