import asyncio
import base64
import datetime
import pickle
import json
import os
import sys
import time
import wave
import copy
import traceback

import nest_asyncio
import requests
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

import ChatAdmin
import ChatAllfind
import ChatCheck
import ChatDelete
import ChatFilter
import ChatLearning
import ChatMerge
import ChatReply
import ChatSubadmin
import simuse
from ChatClass import My_Thread, Update, Version, commandclass, TimeTask

nest_asyncio.apply()


def hello():

    if not (os.path.exists('AutoTask')):
        os.makedirs('AutoTask')
        with open('AutoTask/看我看我.txt', 'wb') as file:
            str =b'\'\'\'\xe8\xbf\x99\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe5\xae\x9a\xe6\x97\xb6\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x9a\x84\xe6\xa8\xa1\xe6\x9d\xbf\xef\xbc\x8c\xe7\xa8\x8b\xe5\xba\x8f\xe4\xbc\x9a\xe8\x87\xaa\xe5\x8a\xa8\xe8\xa7\xa3\xe6\x9e\x90\xe5\xb8\xa6\xe6\xa0\x87\xe8\xae\xb0\xe7\x9a\x84\xe8\xa1\x8c\'\'\'\r\n\'\'\'\xe8\xaf\xb7\xe5\x88\x9b\xe5\xbb\xba\xe4\xb8\x80\xe4\xb8\xaa\xe6\x96\xb0\xe7\x9a\x84txt\xe6\x96\x87\xe4\xbb\xb6\xe6\x9d\xa5\xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe4\xbd\xa0\xe7\x9a\x84\xe4\xbb\xbb\xe5\x8a\xa1\xef\xbc\x8c\xe6\x96\x87\xe4\xbb\xb6\xe5\x90\x8d\xe5\x8d\xb3\xe6\x98\xaf\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x90\x8d\'\'\'\r\n\r\n\'\'\xe5\xbc\x80\xe5\xa4\xb4\xe4\xbd\xbf\xe7\x94\xa8"#"\xe6\x9d\xa5\xe6\xa0\x87\xe8\xae\xb0\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x9a\x84\xe6\x89\xa7\xe8\xa1\x8c\xe6\x97\xa5\xe6\x9c\x9f\'\'\r\n\xe5\xa6\x82"\xe6\xaf\x8f\xe6\x97\xa5"\xef\xbc\x9a\r\n#everyday\r\n\xe6\x88\x96\xe6\x98\xaf"\xe5\x91\xa8\xe4\xb8\x80 \xe5\x91\xa8\xe6\x97\xa5"\xef\xbc\x9a\r\n#w1 w7\r\n\xe4\xba\xa6\xe6\x88\x96\xe6\x98\xaf"\xe5\x85\xb7\xe4\xbd\x93\xe6\x97\xa5\xe6\x9c\x9f"(\xe4\xb8\x8d\xe8\xb6\xb3\xe5\x8d\x81\xe4\xbd\x8d\xe8\xaf\xb7\xe8\xa1\xa50\xef\xbc\x8c\xe5\xa6\x825\xe2\x86\x9205)\xef\xbc\x9a\r\n#2022-08-30\r\n\r\n\'\'\xe5\xbc\x80\xe5\xa4\xb4\xe4\xbd\xbf\xe7\x94\xa8"@"\xe6\x9d\xa5\xe6\xa0\x87\xe8\xae\xb0\xe6\x89\xa7\xe8\xa1\x8c\xe7\xbb\x93\xe6\x9e\x9c\xe5\x8f\x91\xe9\x80\x81\xe7\x9a\x84QQ\xe5\x8f\xb7\r\n\xe5\xa6\x82\xef\xbc\x9a\r\n@123456\r\n\r\n\'\'\xe5\xbc\x80\xe5\xa4\xb4\xe4\xbd\xbf\xe7\x94\xa8"*"\xe6\x9d\xa5\xe6\xa0\x87\xe8\xae\xb0\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x9a\x84\xe6\x89\xa7\xe8\xa1\x8c\xe6\x97\xb6\xe9\x97\xb4\r\n\xe5\xa6\x82(\xe8\xaf\xb7\xe4\xbd\xbf\xe7\x94\xa8\xe8\x8b\xb1\xe6\x96\x87\xe5\x86\x92\xe5\x8f\xb7\xe5\x93\xa6)\xef\xbc\x9a\r\n*05:05\r\n\r\n\'\'\xe5\xbc\x80\xe5\xa4\xb4\xe4\xbd\xbf\xe7\x94\xa8"/"\xe6\x9d\xa5\xe6\xa0\x87\xe8\xae\xb0\xe4\xbb\xbb\xe5\x8a\xa1\xe6\x89\x80\xe9\x9c\x80\xe6\x89\xa7\xe8\xa1\x8c\xe7\x9a\x84\xe6\x8c\x87\xe4\xbb\xa4\r\n\xe5\xa6\x82(\xe4\xb8\x80\xe4\xb8\xaa\xe6\x8c\x87\xe4\xbb\xa4\xe5\xaf\xb9\xe5\xba\x94\xe4\xb8\x80\xe8\xa1\x8c)\xef\xbc\x9a\r\n/check\r\n/autodelete\r\n\r\n\xe4\xbb\xa5\xe4\xb8\x8b\xe6\x98\xaf\xe7\xa4\xba\xe4\xbe\x8b\xef\xbc\x88\xe6\xaf\x8f\xe5\xa4\xa9\xe7\x9a\x8412\xe7\x82\xb9\xe5\x92\x8c23\xe7\x82\xb959\xe5\x88\x86\xef\xbc\x8c\xe6\x89\xa7\xe8\xa1\x8ccheck\xef\xbc\x8cgrouplist\xe6\x8c\x87\xe4\xbb\xa4\xef\xbc\x8c\xe5\xb9\xb6\xe5\xb0\x86\xe7\xbb\x93\xe6\x9e\x9c\xe5\x8f\x91\xe9\x80\x81\xe7\xbb\x99123456\xef\xbc\x89\xef\xbc\x9a\r\n#everyday\r\n@123456\r\n*12:00 23:59\r\n/check\r\n/grouplist\r\n\r\n\r\n-------------------\r\n\xe5\x9c\xa8\xe8\x87\xaa\xe5\x8a\xa8\xe4\xbb\xbb\xe5\x8a\xa1\xe4\xb8\xad\xe6\x9c\x89\xe4\xb8\x80\xe4\xba\x9b\xe7\x89\xb9\xe6\xae\x8a\xe6\x8c\x87\xe4\xbb\xa4\xef\xbc\x9a\r\n\xe8\x87\xaa\xe5\x8a\xa8\xe6\xb8\x85\xe7\x90\x86\xe8\xaf\x8d\xe5\xba\x93"autodelete"\r\n\xe5\x8f\x91\xe9\x80\x81\xe7\xbe\xa4\xe6\xb6\x88\xe6\x81\xaf"sendgroupmessage <\xe7\xbe\xa4\xe5\x8f\xb7> <\xe6\xb6\x88\xe6\x81\xaf>"\r\n\xe5\x8f\x91\xe9\x80\x81\xe7\xbe\xa4\xe5\x9b\xbe\xe7\x89\x87"sendgroupmessageimage <\xe7\xbe\xa4\xe5\x8f\xb7> <\xe5\x9b\xbe\xe7\x89\x87\xe6\x96\x87\xe4\xbb\xb6\xe7\x9a\x84\xe7\xbb\x9d\xe5\xaf\xb9\xe8\xb7\xaf\xe5\xbe\x84>"\r\n\xe5\x8f\x91\xe9\x80\x81\xe5\xa5\xbd\xe5\x8f\x8b\xe6\xb6\x88\xe6\x81\xaf"sendfriendmessage <\xe5\xa5\xbd\xe5\x8f\x8bQQ> <\xe6\xb6\x88\xe6\x81\xaf>"\r\n\xe5\x8f\x91\xe9\x80\x81\xe5\xa5\xbd\xe5\x8f\x8b\xe5\x9b\xbe\xe7\x89\x87"sendfriendmessageimage <\xe5\xa5\xbd\xe5\x8f\x8bQQ> <\xe5\x9b\xbe\xe7\x89\x87\xe6\x96\x87\xe4\xbb\xb6\xe7\x9a\x84\xe7\xbb\x9d\xe5\xaf\xb9\xe8\xb7\xaf\xe5\xbe\x84>"\r\n\xe5\x9c\xa8<\xe6\xb6\x88\xe6\x81\xaf>\xe8\xbf\x99\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xe4\xb8\xad\xef\xbc\x8c\xe5\x8f\xaf\xe4\xbb\xa5\xe9\x99\x84\xe5\xb8\xa6\xe4\xb8\x80\xe4\xba\x9b\xe6\x8c\x87\xe5\xae\x9a\xe7\x9a\x84\xe6\xa0\x87\xe8\xae\xb0\xef\xbc\x8c\xe7\xa8\x8b\xe5\xba\x8f\xe4\xbc\x9a\xe5\xb0\x86\xe8\xbf\x99\xe4\xba\x9b\xe6\xa0\x87\xe8\xae\xb0\xe6\x9b\xbf\xe6\x8d\xa2\xe6\x88\x90\xe7\x9b\xb8\xe5\xba\x94\xe7\x9a\x84\xe7\xbb\x93\xe6\x9e\x9c\xef\xbc\x9a\r\n\xe5\xbd\x93\xe5\x89\x8d\xe5\xb9\xb4\xef\xbc\x9a{year}\r\n\xe5\xbd\x93\xe5\x89\x8d\xe6\x9c\x88\xef\xbc\x9a{month}\r\n\xe5\xbd\x93\xe5\x89\x8d\xe6\x97\xa5\xef\xbc\x9a{day}\r\n\xe6\x8d\xa2\xe8\xa1\x8c\xef\xbc\x9a{n}\r\n\xe5\xa6\x82\xef\xbc\x9a\r\n/sendgroupmessage 123456 \xe4\xbb\x8a\xe5\xa4\xa9\xe6\x98\xaf{year}\xe5\xb9\xb4{month}\xe6\x9c\x88{day}\xe6\x97\xa5\xef\xbc\x81{n}\xe5\xa4\xa7\xe5\xae\xb6\xe5\xa5\xbd\xe5\x95\x8a\xef\xbc\x81\r\n-------------------\r\n\r\n'
            file.write(str)
        print('在目录下的AutoTask文件夹内看看定时任务的说明吧！')

    #os.system("title ChatLearning")
    file = open('config.clc', 'r', encoding='utf-8-sig')
    try:
        config = json.load(file)
    except json.decoder.JSONDecodeError:
        file.close()
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = eval(file.read())
    file.close()
    config['reply'] = 0
    config['merge'] = 0
    config['learning'] = 0
    config['admin'] = 0
    if ('version' in config.keys()) == False:
        update = Update('0.0.0')
        update.ClChange()
        config['version'] = '2.7.0'
    else:
        update = Update(config['version'])
    update.Cl_version()
    config = update.Config_version()
    config['version'] = Version()
    file = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file, indent=3, ensure_ascii=False)
    file.close()
    ChatFilter.Merge_Filter()
    print('欢迎使用ChatLearning应用 版本号：', Version())
    #print('遇到问题和bug请在mirai论坛回复我或发送至我的邮箱1121917292@qq.com')
    print('输入help来查看指令列表吧！')


def unknowcommand(command):
    print('<-未知指令"{}"   请输入help/?查看帮助'.format(command))
    pass


def exit():
    sys.exit(0)


def ReplyWait(args: str, fromchat=0):
    global data
    if args.find(' ') == -1:
        print('参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None
    try:
        BenchmarkTime = float(args[:args.find(' ')])
        RandomTime = float(args[args.find(' ') + 1:])
    except:
        print('参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None
    if BenchmarkTime < RandomTime:
        print("浮动时间范围不得大于基准时间！")
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, "浮动时间范围不得大于基准时间！", 1)
        return None
    elif BenchmarkTime > 4 or RandomTime > 2:
        print("基准时间不得大于4秒，浮动时间不得大于2秒！")
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, "基准时间不得大于4秒，浮动时间不得大于2秒！", 1)
        return None
    elif BenchmarkTime < 0 or RandomTime < 0:
        print("时间不得为负数！")
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, "时间不得为负数！", 1)
        return None
    replystoptime = [BenchmarkTime, RandomTime]
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    config['replywait'] = replystoptime
    file = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file, indent=3, ensure_ascii=False)
    print('已将回复等待时间设置为{:g}±{:g}秒'.format(BenchmarkTime, RandomTime))
    if fromchat != 0:
        simuse.Send_Message(
            data, fromchat, 2,
            '已将回复等待时间设置为{:g}±{:g}秒'.format(BenchmarkTime, RandomTime), 1)


def GetAutoTask():
    try:
        Taskdict = pickle.load(open('AutoTask/AutoTask.clc', 'rb'))
    except:
        Taskdict = {}
        pickle.dump(Taskdict, open('AutoTask/AutoTask.clc', 'wb'))
    return Taskdict


def GetAutoTaskInfo(fromchat=0):
    global TaskDict
    global data
    if TaskDict == {}:
        print('当前无定时任务')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '当前无定时任务', 1)
    else:
        nodelist = []
        situationnodedict = {
            'senderId': data['qq'],
            'time': int(time.time()),
            'senderName': 'ChatLearning',
            'messageChain': [{
                'type': 'Plain',
                'text': ''
            }]
        }
        for Task in TaskDict.values():
            print(Task.TaskInfo())
            InfoChain = [{'type': 'Plain', 'text': Task.TaskInfo()}]
            situationnodedict['messageChain'] = InfoChain
            nodelist.append(situationnodedict.copy())

        if fromchat != 0:
            sendmessagechain = [{'type': 'Forward', 'nodeList': ''}]
            sendmessagedict = sendmessagechain[0]
            sendmessagedict['nodeList'] = nodelist
            simuse.Send_Message_Chain(data, fromchat, 2, sendmessagechain)


def RunAutoTask():
    global TaskDict
    while 1:
        pickle.dump(TaskDict, open('AutoTask/AutoTask.clc', 'wb'))
        time.sleep(1)
        if TaskDict == {}:
            continue
        TaskValuesList = list(TaskDict.values())
        for Task in TaskValuesList:
            if Task.ISTaskTime() == 1:
                RunTaskCommand(Task)

def AutoTaskLog(function):
    def wrapper(Task):
        print('开始执行自动任务{}'.format(Task.TaskName))
        with open('AutoTask/Tasklog.log', 'a',
                    encoding='utf-8-sig') as file:
            nowtime = datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')
            file.write(nowtime + ' 开始执行自动任务{}'.format(Task.TaskName) +
                        '\n')
        try:
            function(Task)
        except:
            print('自动任务{}执行出错，异常已记录'.format(Task.TaskName))
            with open('AutoTask/Tasklog.log', 'a',
                        encoding='utf-8-sig') as file:
                nowtime = datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S')
                file.write(nowtime + ' 自动任务{}执行出错：\n'.format(Task.TaskName) +traceback.format_exc()+
                            '\n')
            raise
        else:
            print('自动任务{}执行完毕'.format(Task.TaskName))
            with open('AutoTask/Tasklog.log', 'a',
                        encoding='utf-8-sig') as file:
                nowtime = datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S')
                file.write(nowtime + ' 自动任务{}执行完毕'.format(Task.TaskName) +
                            '\n')
    return wrapper


@AutoTaskLog
def RunTaskCommand(Task):
    for TaskCommand in Task.TaskList:
        time.sleep(1)
        if TaskCommand == 'admin':
            continue
        if TaskCommand == 'autodelete':
            AutoDelete(Task.SendList)
            continue
        if TaskCommand[:18] == 'sendfriendmessage ':
            sendfriendmessage(TaskCommand[18:].split(' ', 1))
            continue
        if TaskCommand[:23] == 'sendfriendmessageimage ':
            sendfriendmessageimage(TaskCommand[23:].split(' ', 1))
            continue
        if TaskCommand[:17] == 'sendgroupmessage ':
            sendgroupmessage(TaskCommand[17:].split(' ', 1))
            continue
        if TaskCommand[:22] == 'sendgroupmessageimage ':
            sendgroupmessageimage(TaskCommand[22:].split(' ', 1))
            continue
        if Task.SendList != []:
            commandchoice(TaskCommand, fromchat=Task.SendList)
        else:
            commandchoice(TaskCommand)
    if Task.ISDisposable == 1:
        TaskDict.pop(Task.TaskName)
        

def AutoDelete(fromchat):
    global data
    global adminsendmode
    global learningsign
    global mergesign
    global replysign
    learning_close_sign = 0
    reply_close_sign = 0
    if learningsign == 1:
        tempsign = learning(learningsign, mergesign, fromchat)
        learningsign = tempsign[0]
        mergesign = tempsign[1]
        learning_close_sign = 1
    if replysign == 1:
        time.sleep(0.8)
        replysign = reply(replysign, fromchat)
        reply_close_sign = 1

    time.sleep(1)
    ChatDelete.Delete(data, fromchat)

    if learning_close_sign == 1:
        time.sleep(0.8)
        tempsign = learning(learningsign, mergesign, fromchat)
        learningsign = tempsign[0]
        mergesign = tempsign[1]
    if reply_close_sign == 1:
        time.sleep(0.8)
        replysign = reply(replysign, fromchat)


def sendgroupmessage(arglist):
    global data
    target = arglist[0]
    sendstr = arglist[1]
    sendstr = sendstr.replace('{year}', datetime.datetime.now().strftime('%Y'))
    sendstr = sendstr.replace('{month}',
                              datetime.datetime.now().strftime('%m'))
    sendstr = sendstr.replace('{day}', datetime.datetime.now().strftime('%d'))
    sendstr = sendstr.replace('{n}', '\n')
    simuse.Send_Message(data, target, 1, sendstr, 1)


def sendgroupmessageimage(arglist):
    global data
    target = arglist[0]
    sendstr = arglist[1]
    simuse.Send_Message(data, target, 1, sendstr, 2, path=1)


def sendfriendmessage(arglist):
    global data
    target = arglist[0]
    sendstr = arglist[1]
    sendstr = sendstr.replace('{year}', datetime.datetime.now().strftime('%Y'))
    sendstr = sendstr.replace('{month}',
                              datetime.datetime.now().strftime('%m'))
    sendstr = sendstr.replace('{day}', datetime.datetime.now().strftime('%d'))
    sendstr = sendstr.replace('{n}', '\n')
    simuse.Send_Message(data, target, 2, sendstr, 1)


def sendfriendmessageimage(arglist):
    global data
    target = arglist[0]
    sendstr = arglist[1]
    simuse.Send_Message(data, target, 2, sendstr, 2, path=1)


def AutoTaskCommand(fromchat=0):
    global data
    command={}
    command['autodelete']='#自动清理词库'
    command['sendfriendmessage <好友QQ> <消息>']='#发送好友消息'
    command['sendfriendmessageimage <好友QQ> <图片绝对路径>']='#发送好友图片消息'
    command['sendgroupmessage <群号> <消息>']='#发送群聊消息'
    command['sendgroupmessageimage <群号> <消息>']='#发送群聊图片消息'
    print('指令列表：')
    sendtext = ''
    for i in command:
        sendtext = sendtext + i + command[i] + '\n'
        print(i, '   ', command[i])
    print('\n')
    if fromchat != 0:
        simuse.Send_Message(data, fromchat, 2, sendtext, 1)



def uploadwav(data, fromchat=0):
    try:
        wavsize = os.path.getsize('source.wav')
    except:
        print('未找到source.wav文件！')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '未找到source.wav文件！', 1)
        return None
    wav_kb = wavsize / float(1024)
    if wav_kb >= 10240:
        print('文件大小超过10M！取消上传')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '文件大小超过10M！取消上传', 1)
        return None
    wavefile = wave.open('source.wav', 'rb')
    wav_secs = wavefile.getnframes() / wavefile.getframerate()
    if wav_secs >= 20:
        print('音频时长大于20秒！取消上传')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '音频时长大于20秒！取消上传', 1)
        return None
    wavfile = open('source.wav', 'rb')
    base64_data = base64.b64encode(wavfile.read())
    wavfile.close()
    data_in = {'QQ': data['qq'], 'base64': base64_data.decode()}
    url = 'http://124.222.165.166:19630/Sourcewav'
    try:
        print('正在等待服务器响应')
        simuse.Send_Message(data, fromchat, 2, '正在等待服务器响应', 1)
        res = requests.request('post', url=url, json=data_in, timeout=20)
        res = json.loads(res.text)
    except:
        print('上传失败,服务器未响应')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '上传失败,服务器未响应', 1)
            return None
    try:
        if res['code'] == 1:
            print('上传成功！')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '上传成功！', 1)
            return None
        else:
            print('上传失败！')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '上传失败！', 1)
            return None
    except:
        print('上传失败！')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '上传失败！', 1)
        return None


def testvoice(data, text, fromchat=0):
    if fromchat == 0:
        print('请在聊天环境下进行')
        return None
    if ChatReply.canToVoice(text):
        if ChatReply.CanSendTask():
            answer = ChatReply.Plain_Voice(data, text)
            if answer == None:
                print('转换失败')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '转换失败', 1)
                return None
            else:
                simuse.Send_Message_Chain(data, fromchat, 2, answer)
        else:
            print('转换失败，服务器队列已满')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '转换失败，服务器队列已满', 1)
            return None
    else:
        print('转换失败，存在不支持的字符')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '转换失败，存在不支持的字符', 1)


def SetTempMessage(data, num, fromchat=0):
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    try:
        num = int(num)
    except:
        print('参数错误')
        return None
    if num < 1:
        print('参数错误')
        return None
    config['tempmessagenum'] = num
    file = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file, indent=3, ensure_ascii=False)
    file.close()
    print('每个群的消息缓存已设置为{}条'.format(num))
    if fromchat != 0:
        simuse.Send_Message(data, fromchat, 2, '每个群的消息缓存已设置为{}条'.format(num),
                            1)


def SetFastDeleteAdmin(FastDeletesign, fromchat=0):
    global data
    if FastDeletesign == 0:
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config = eval(config)
        config['fastdelete'] = 1
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-快速删除已设置为所有人可用')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '快速删除已设置为所有人可用', 1)
        FastDeletesign = 1
        return FastDeletesign
    else:
        FastDeletesign = 0
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config = eval(config)
        config['fastdelete'] = 0
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-快速删除已设置为仅管理员可用')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '快速删除已设置为仅管理员可用', 1)
        return FastDeletesign


def blackfreq(data, num, fromchat=0):
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    try:
        num = int(num)
    except:
        print('参数错误')
        return None
    if num < 1:
        print('参数错误')
        return None
    config['blackfreq'] = num
    file = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file, indent=3, ensure_ascii=False)
    file.close()
    print('黑名单容错次数已设置为{}次'.format(num))
    if fromchat != 0:
        simuse.Send_Message(data, fromchat, 2, '黑名单容错次数已设置为{}次'.format(num), 1)


def setvoicept(data, ptname, fromchat=0):
    url = "http://124.222.165.166:19630/Ptlist"
    try:
        print('正在等待服务器响应')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '正在等待服务器响应', 1)
        res = requests.request('get', url, timeout=20)
        res = json.loads(res.text)
    except:
        print('设置失败,服务器未响应')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '设置失败,服务器未响应', 1)
            return None
    ptlist = res['ptlist']
    if not (ptname in ptlist):
        sendptlist = ''
        for i in ptlist:
            sendptlist = sendptlist + i + ' '
        print('该训练集不存在')
        print('服务器中存在的训练集：\n' + sendptlist)
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2,
                                '该训练集不存在\n服务器中存在的训练集：\n' + sendptlist, 1)
        return None
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    config['synthesizer'] = ptname
    file = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file, indent=3, ensure_ascii=False)
    file.close()
    print('训练集已更改为{}'.format(ptname))
    if fromchat != 0:
        simuse.Send_Message(data, fromchat, 2, '训练集已更改为{}'.format(ptname), 1)


def remerge():
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    config['merge'] = 1
    file = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file, indent=3, ensure_ascii=False)
    file.close()
    merge = My_Thread(target=ChatMerge.main)
    merge.start()


def globe(globesign=0, get=0, fromchat=0):
    global data
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    if get == 1:
        return config['sendmode']
    if globesign == 0:
        config['sendmode'] = 1
        globesign = 1
        print('<-已开启全局模式')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '已开启全局模式', 1)
    else:
        config['sendmode'] = 0
        globesign = 0
        print('<-已关闭全局模式')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '已关闭全局模式', 1)
    file = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file, indent=3, ensure_ascii=False)
    return globesign


def setadmin(adminnum, fromchat=0):
    global data
    adminlist = '[{}]'.format(adminnum)
    try:
        adminlist = adminlist.replace('，', ',')
        adminlist = adminlist.replace(' ', ',')
    except:
        pass
    try:
        adminlist = eval(adminlist)
        if type(adminlist) != type([]):
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
    except:
        print('参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    config['Administrator'] = adminlist
    file = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file, indent=3, ensure_ascii=False)
    print('管理员QQ号已设置为', adminlist)
    if fromchat != 0:
        simuse.Send_Message(data, fromchat, 2, '管理员QQ号已设置为' + str(adminlist),
                            1)


def admin(adminsign, fromchat=0):
    global adminsendmode
    global learningsign
    global mergesign
    global replysign
    learning_close_sign = 0
    reply_close_sign = 0
    if fromchat == 0:
        print('请在管理员私聊bot执行该指令')
        return adminsign
    if learningsign == 1:
        tempsign = learning(learningsign, mergesign, fromchat)
        learningsign = tempsign[0]
        mergesign = tempsign[1]
        learning_close_sign = 1
    if replysign == 1:
        time.sleep(0.8)
        replysign = reply(replysign, fromchat)
        reply_close_sign = 1
    if adminsign == 0:
        time.sleep(0.8)
        print('<-进入管理模式')
        print('请不要操作控制台！！！')
        #print('拥有词库的群号:')
        #print(ChatAdmin.getfilelist())
        tips = '请发送需要操作的序号\n1.在所有群内查找\n2.在指定群内查找\n3.过滤设置\n4.自动清理词库'
        simuse.Send_Message(data, fromchat, 2, tips, 1)
        command = getcommand_chat_foradmin()
        choice = command[0]
        sender = command[1]
        if choice == str(1):
            ChatAllfind.findallcontrol(data, fromchat)
            print(('<-退出管理模式'))
            simuse.Send_Message(data, fromchat, 2, '退出管理模式', 1)
            #return adminsign
        elif choice == str(2):
            if fromchat != 0:
                tips = '进入管理模式' + '\n' + '拥有词库的群号' + '\n' + str(
                    ChatAdmin.getfilelist()) + '\n' + '请发送需要选择的群号'
                simuse.Send_Message(data, fromchat, 2, tips, 1)
            print('请使用管理员QQ', ChatAdmin.getconfig(1), '向bot发送需要选择的群号')
            #adminsendmode=1
            time.sleep(0.5)
            #adminsendmode=0
            command = getcommand_chat_foradmin()
            group = command[0]
            sender = command[1]
            try:
                group = str(group)
            except:
                print('参数错误')
                print('<-退出管理模式')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误,退出管理模式', 1)
                return adminsign
            file = open('config.clc', 'r', encoding='utf-8-sig')
            config = json.load(file)
            file.close()
            config['admin'] = 1
            file = open('config.clc', 'w', encoding='utf-8-sig')
            json.dump(config, file, indent=3, ensure_ascii=False)
            file.close()
            ChatAdmin.main(data, config['Administrator'], group, sender)
            #admin=My_Thread(target=ChatAdmin.main,args=(config['Administrator'],group))
            #adminsign=1
            #admin.join()
            #listen = My_Thread(target=getcommand_chat)
            #listen.start()
            #return adminsign
        elif choice == str(3):
            ChatFilter.filtercontrol(data, fromchat)
            print('<-退出管理模式')
            simuse.Send_Message(data, fromchat, 2, '退出管理模式', 1)
            #return adminsign
        elif choice == str(4):
            simuse.Send_Message(
                data, fromchat, 2,
                '此操作将会删除词库中仅出现过单次的条目和被过滤的条目，且操作不可逆！！\n请输入“确定”确认删除', 1)
            command = getcommand_chat_foradmin()
            if command[0] == '确定':
                sender = command[1]
                ChatDelete.Delete(data, sender)
                print('<-退出管理模式')
                simuse.Send_Message(data, fromchat, 2, '退出管理模式', 1)
            else:
                print('<-退出管理模式')
                simuse.Send_Message(data, fromchat, 2, '退出管理模式', 1)
        else:
            print('参数错误')
            print('<-退出管理模式')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误,退出管理模式', 1)
            #return adminsign
        if learning_close_sign == 1:
            time.sleep(0.8)
            tempsign = learning(learningsign, mergesign, fromchat)
            learningsign = tempsign[0]
            mergesign = tempsign[1]
        if reply_close_sign == 1:
            time.sleep(0.8)
            replysign = reply(replysign, fromchat)
        return adminsign


def get_group_perm(data, group):
    adminlist = []
    memberlist = simuse.Get_Groupmember(data, group)
    for i in memberlist:
        if i['permission'] == 'OWNER' or i['permission'] == 'ADMINISTRATOR':
            adminlist.append(i['id'])
    return adminlist


def grouplist(fromchat=0):
    global data
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    learninggrouplist = config['learninggrouplist']
    replygrouplist = config['replygrouplist']
    unmergegrouplist = config['unmergegrouplist']
    Administrator = config['Administrator']
    try:
        subadmindict = config['subadmin']
    except:
        subadmindict = {'无': None}
    print('管理员QQ号：', Administrator)
    print('已开启记录的群：', learninggrouplist)
    print('已开启答复的群：', replygrouplist)
    print('允许自主管理的群：', list(subadmindict.keys()))
    print('不录入总词库的群：', unmergegrouplist)
    if fromchat != 0:
        sendtext = '管理员QQ号：' + str(Administrator) + '\n' + '已开启记录的群：' + str(
            learninggrouplist) + '\n' + '已开启答复的群：' + str(
                replygrouplist) + '\n' + '允许自主管理的群：' + str(
                    list(subadmindict.keys())) + '\n' + '不录入总词库的群：' + str(
                        unmergegrouplist)
        simuse.Send_Message(data, fromchat, 2, sendtext, 1)


def learninginterval(interval, fromchat=0):
    global data
    try:
        interval = int(interval)
    except:
        print('参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None
    if interval <= 0:
        print('参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None
    print('<-已设置词库链学习间隔时间', interval, '秒')
    if fromchat != 0:
        simuse.Send_Message(data, fromchat, 2,
                            '已设置词库链学习间隔时间' + str(interval) + '秒', 1)
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    config['interval'] = interval
    file2 = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file2, indent=3, ensure_ascii=False)


def replychance(chance, fromchat=0):
    global data
    if chance[:chance.find(' ')] == '-s':
        args = chance[chance.find(' ') + 1:]
        if args.find(' ') != -1:
            single_chance = args[:args.find(' ')]
        else:
            print('参数错误,群号为空')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误,群号为空', 1)
            return None
        try:
            single_chance = int(single_chance)
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        if single_chance <= 0 or single_chance > 100:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        grouplist = '[{}]'.format(args[args.find(' ') + 1:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        try:
            file = open('config.clc', 'r', encoding='utf-8-sig')
            config = json.load(file)
            file.close()
            replydict = config['singlereplychance']
        except:
            replydict = {}
        for i in grouplist:
            replydict[str(i)] = single_chance
        config['singlereplychance'] = replydict
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-添加完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '添加完毕', 1)

    elif chance[:chance.find(' ')] == '-d':
        args = chance[chance.find(' ') + 1:]
        grouplist = '[{}]'.format(args)
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        try:
            replydict = config['singlereplychance']
        except:
            print('请先添加！')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '请先添加！', 1)
            return None
        pass
        sendtext = ''
        for i in grouplist:
            try:
                replydict.pop(str(i))
            except:
                print('群', i, '不存在')
                sendtext = sendtext + str(i) + '\n'
                continue
        if sendtext != '':
            simuse.Send_Message(data, fromchat, 2, '群' + sendtext + '不存在', 1)
        config['singlereplychance'] = replydict
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-移除完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '移除完毕', 1)
    else:
        try:
            chance = int(chance)
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        if chance <= 0 or chance > 100:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        print('<-已设置回复的触发概率', chance, '%')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2,
                                '已设置回复的触发概率' + str(chance) + '%', 1)
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['replychance'] = chance
        file2 = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file2, indent=3, ensure_ascii=False)


def voicereplychance(chance, fromchat=0):
    global data
    if chance[:chance.find(' ')] == '-s':
        args = chance[chance.find(' ') + 1:]
        if args.find(' ') != -1:
            single_chance = args[:args.find(' ')]
        else:
            print('参数错误,群号为空')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误,群号为空', 1)
            return None
        try:
            single_chance = int(single_chance)
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        if single_chance <= 0 or single_chance > 100:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        grouplist = '[{}]'.format(args[args.find(' ') + 1:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        try:
            file = open('config.clc', 'r', encoding='utf-8-sig')
            config = json.load(file)
            file.close()
            replydict = config['singlevoicereplychance']
        except:
            replydict = {}
        for i in grouplist:
            replydict[str(i)] = single_chance
        config['singlevoicereplychance'] = replydict
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-添加完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '添加完毕', 1)

    elif chance[:chance.find(' ')] == '-d':
        args = chance[chance.find(' ') + 1:]
        grouplist = '[{}]'.format(args)
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        try:
            replydict = config['singlevoicereplychance']
        except:
            print('请先添加！')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '请先添加！', 1)
            return None
        pass
        sendtext = ''
        for i in grouplist:
            try:
                replydict.pop(str(i))
            except:
                print('群', i, '不存在')
                sendtext = sendtext + str(i) + '\n'
                continue
        if sendtext != '':
            simuse.Send_Message(data, fromchat, 2, '群' + sendtext + '不存在', 1)
        config['singlevoicereplychance'] = replydict
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-移除完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '移除完毕', 1)

    else:
        try:
            chance = int(chance)
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        if chance <= 0 or chance > 100:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        print('<-已设置语音回复的触发概率', chance, '%')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2,
                                '已设置语音回复的触发概率' + str(chance) + '%', 1)
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['voicereplychance'] = chance
        file2 = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file2, indent=3, ensure_ascii=False)
        file2.close()


def addgroup(args, fromchat=0):
    global data
    if args[:9] == 'learning ' or args[:10] == 'learnings ':
        if args[:10] == 'learnings ':
            grouplist = '[{}]'.format(args[10:])
        else:
            grouplist = '[{}]'.format(args[9:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['learninggrouplist'].extend(grouplist)
        config['learninggrouplist'] = list(set(config['learninggrouplist']))
        if args[:10] == 'learnings ':
            config['replygrouplist'].extend(grouplist)
            config['replygrouplist'] = list(set(config['replygrouplist']))
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        if args[:10] == 'learnings ':
            print('<-添加完毕 已同时加入回复列表')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '添加完毕 已同时加入回复列表', 1)
        else:
            print('<-添加完毕')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '添加完毕', 1)
        pass
    elif args[:6] == 'reply ':
        grouplist = '[{}]'.format(args[6:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['replygrouplist'].extend(grouplist)
        config['replygrouplist'] = list(set(config['replygrouplist']))
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-添加完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '添加完毕', 1)
        pass
    elif args[:8] == 'unmerge ':
        grouplist = '[{}]'.format(args[8:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['unmergegrouplist'].extend(grouplist)
        config['unmergegrouplist'] = list(set(config['unmergegrouplist']))
        config['merge'] = 0
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-添加完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '添加完毕', 1)
        return config['learning']
        pass
    elif args[:9] == 'subadmin ':
        grouplist = '[{}]'.format(args[9:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        try:
            file = open('config.clc', 'r', encoding='utf-8-sig')
            config = json.load(file)
            file.close()
            Subadmindict = config['subadmin']
        except:
            Subadmindict = {}
        for i in grouplist:
            try:
                Subadmindict[i] = get_group_perm(data, i)
            except:
                print('群不存在')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '群不存在', 1)
                return None
        config['subadmin'] = Subadmindict
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-添加完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '添加完毕', 1)
    elif args[:4] == 'tag ':
        tempargs = args[4:]
        tag = tempargs[:tempargs.find(' ')]
        if tempargs.find(' ') == -1:
            print('参数错误,群号为空')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误,群号为空', 1)
            return None
        grouplist = '[{}]'.format(tempargs[tempargs.find(' ') + 1:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        try:
            file = open('config.clc', 'r', encoding='utf-8-sig')
            config = json.load(file)
            file.close()
            Tagdict = config['tag']
        except:
            Tagdict = {}
        for i in grouplist:
            try:
                Taglist = Tagdict[str(i)]
            except:
                Taglist = []
            Taglist.append(tag)
            Tagdict[str(i)] = list(set(Taglist))
        config['tag'] = Tagdict
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-添加完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '添加完毕', 1)
        try:
            ChatMerge.getfile()
        except:
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2,
                                    '词库合并错误，请关闭Learning/Reply后重新操作', 1)
            print('词库合并错误，请关闭Learning/Reply后重新操作')
    elif args[:9] == 'autotask ':
        global TaskDict
        TaskName = args[9:]
        try:
            Task = TimeTask(TaskName)
        except FileNotFoundError:
            print('未找到文件,请检查是否在AutoTask目录下')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2,
                                    '未找到文件,请检查是否在AutoTask目录下', 1)
            return None
        except UnicodeDecodeError:
            print('读取错误，请检查文件编码是否为UTF-8')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2,
                                    '读取错误，请检查文件编码是否为UTF-8', 1)
            return None
        if Task.CheckTask() == 0:
            print(Task.ErrorTips)
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, Task.ErrorTips, 1)
            return None

        TaskDict[TaskName] = copy.deepcopy(Task)
        print('添加成功！\n' + Task.TaskInfo())
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, Task.TaskInfo(), 1)

    else:
        print('参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None


def removegroup(args, fromchat=0):
    global data
    if args[:9] == 'learning ':
        grouplist = '[{}]'.format(args[9:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        sendtext = ''
        for i in grouplist:
            try:
                config['learninggrouplist'].remove(i)
            except:
                print('群', i, '不存在')
                sendtext = sendtext + str(i) + '\n'
                continue
        if sendtext != '':
            simuse.Send_Message(data, fromchat, 2, '群' + sendtext + '不存在', 1)
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-移除完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '移除完毕', 1)
        pass
    elif args[:6] == 'reply ':
        grouplist = '[{}]'.format(args[6:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        sendtext = ''
        for i in grouplist:
            try:
                config['replygrouplist'].remove(i)
            except:
                print('群', i, '不存在')
                sendtext = sendtext + str(i) + '\n'
                continue
        if sendtext != '':
            simuse.Send_Message(data, fromchat, 2, '群' + sendtext + '不存在', 1)
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-移除完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '移除完毕', 1)
        pass
    elif args[:8] == 'unmerge ':
        grouplist = '[{}]'.format(args[8:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        sendtext = ''
        for i in grouplist:
            try:
                config['unmergegrouplist'].remove(i)
            except:
                print('群', i, '不存在')
                sendtext = sendtext + str(i) + '\n'
                continue
        if sendtext != '':
            simuse.Send_Message(data, fromchat, 2, '群' + sendtext + '不存在', 1)
        config['merge'] = 0
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-移除完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '移除完毕', 1)
        return config['learning']
        pass
    elif args[:9] == 'subadmin ':
        grouplist = '[{}]'.format(args[9:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        try:
            subadmindict = config['subadmin']
        except:
            print('请先添加！')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '请先添加！', 1)
            return None
        pass
        sendtext = ''
        for i in grouplist:
            try:
                subadmindict.pop(str(i))
            except:
                print('群', i, '不存在')
                sendtext = sendtext + str(i) + '\n'
                continue
        if sendtext != '':
            simuse.Send_Message(data, fromchat, 2, '群' + sendtext + '不存在', 1)
        config['subadmin'] = subadmindict
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-移除完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '移除完毕', 1)
        pass

    elif args[:4] == 'tag ':
        grouplist = '[{}]'.format(args[4:])
        try:
            grouplist = grouplist.replace('，', ',')
            grouplist = grouplist.replace(' ', ',')
        except:
            pass
        try:
            grouplist = eval(grouplist)
            if type(grouplist) != type([]):
                print('参数错误')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
                return None
        except:
            print('参数错误')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
            return None
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        try:
            Tagdict = config['tag']
        except:
            print('请先添加！')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '请先添加！', 1)
            return None
        pass
        sendtext = ''
        Taglist = []
        for i in Tagdict.values():
            Taglist.extend(i)
        Taglist = list(set(Taglist))
        for i in Taglist:
            try:
                os.remove('WordStock/' + '{}.cl'.format(i))
            except:
                pass
        for i in grouplist:
            try:
                Tagdict.pop(str(i))
            except:
                print('群', i, '不存在')
                sendtext = sendtext + str(i) + '\n'
                continue
        if sendtext != '':
            simuse.Send_Message(data, fromchat, 2, '群' + sendtext + '不存在', 1)
        config['tag'] = Tagdict
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-移除完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '移除完毕', 1)
        try:
            ChatMerge.getfile()
        except:
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2,
                                    '词库合并错误，请关闭Learning/Reply后重新操作', 1)
            print('词库合并错误，请关闭Learning/Reply后重新操作')

    elif args[:9] == 'autotask ':
        global TaskDict
        TaskName = args[9:]

        try:
            TaskDict.pop(TaskName)
        except:
            print('删除失败，未找到名为“{}”的定时任务'.format(TaskName))
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2,
                                    '删除失败，未找到名为“{}”的定时任务'.format(TaskName), 1)
            return None

        print('删除成功！')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '删除成功！', 1)

    else:
        print('参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None


def learning(learningsign, mergesign, fromchat=0):
    global data
    if learningsign == 0 and mergesign == 0:
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['learning'] = 1
        config['merge'] = 1
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-开始记录')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '开始记录', 1)
        learning = My_Thread(target=ChatLearning.main)
        merge = My_Thread(target=ChatMerge.main)
        learningsign = 1
        mergesign = 1
        learning.start()
        merge.start()
        return learningsign, mergesign
    else:
        learningsign = 0
        mergesign = 0
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['learning'] = 0
        config['merge'] = 0
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-停止记录')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '停止记录', 1)
        return learningsign, mergesign


def reply(replysign, fromchat=0):
    global data
    if replysign == 0:
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['reply'] = 1
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-开启回复功能')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '开启回复功能', 1)
        reply = My_Thread(target=ChatReply.main)
        replysign = 1
        reply.start()
        return replysign
    else:
        replysign = 0
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['reply'] = 0
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-关闭回复功能')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '关闭回复功能', 1)
        return replysign


def voicereply(voicereplysign, fromchat=0):
    global data
    if voicereplysign == 0:
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['voicereply'] = 1
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-开启语音回复功能')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '开启语音回复功能', 1)
        voicereplysign = 1
        return voicereplysign
    else:
        voicereplysign = 0
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = json.load(file)
        file.close()
        config['voicereply'] = 0
        file = open('config.clc', 'w', encoding='utf-8-sig')
        json.dump(config, file, indent=3, ensure_ascii=False)
        file.close()
        print('<-关闭语音回复功能')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '关闭语音回复功能', 1)
        return voicereplysign


def merge(time, fromchat=0):
    if time <= 0:
        print('参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None
    print('<-已设置总词库更新时间', time, '秒')
    if fromchat != 0:
        simuse.Send_Message(data, fromchat, 2, '已设置总词库更新时间' + str(time) + '秒',
                            1)
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    config['mergetime'] = time
    file2 = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file2, indent=3, ensure_ascii=False)
    file2.close()


def check(fromchat=0):
    global data
    check = My_Thread(target=ChatCheck.main, args=(data, fromchat))
    check.start()
    check.join()


def typefreq(data, args, fromchat=0):
    typelist = [
        'Plain', 'Image', 'Face', 'FlashImage', 'Voice', 'Forward', 'App',
        'Xml', 'Json'
    ]
    type = args[:args.find(' ')]
    freq = args[args.find(''):][args[args.find(''):].find(' ') + 1:]
    for i in typelist:
        if type == i.lower():
            type = i
            break
    else:
        typetip = '支持的类型：\n'
        for types in typelist:
            typetip += types + ' '
        print('<-消息类型错误\n' + typetip)
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '消息类型错误\n' + typetip, 1)
        return None
    try:
        freq = int(freq)
    except:
        print('<-参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None
    if freq <= 0:
        print('<-参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = json.load(file)
    file.close()
    freqdict = config['typefreq']
    freqdict[type] = freq
    file = open('config.clc', 'w', encoding='utf-8-sig')
    json.dump(config, file, indent=3, ensure_ascii=False)
    file.close()
    print('<-已设置{}回复阈值'.format(type), freq, '次')
    if fromchat != 0:
        simuse.Send_Message(data, fromchat, 2,
                            '已设置{}回复阈值'.format(type) + str(freq) + '次', 1)


def getcommand_chat():
    global data
    global adminsendmode
    data = simuse.Get_data()  # Test
    data = simuse.Get_Session(data)  # Test
    while 1:
        if adminsendmode == 1:
            print('none')
            break
        fromchat = ChatAdmin.getconfig(1)
        message = simuse.Fetch_Message(data)
        if type(message) == type(0):
            time.sleep(0.5)
            continue
        for i in message:
            if i['type'] == 'FriendMessage' and (
                    i['sender'] in fromchat):  # 判断监听到的消息是否为群消息
                messagechain = i['messagechain']
                command = messagechain[1]
                if command['type'] == 'Plain':
                    if command['text'][0] == '!' or command['text'][0] == '！':
                        commandchoice(command['text'][1:], i['sender'])
        time.sleep(0.5)


def getcommand_chat_foradmin():
    global data
    global adminsendmode
    while 1:
        fromchat = ChatAdmin.getconfig(1)
        message = simuse.Fetch_Message(data)
        if type(message) == type(0):
            time.sleep(0.5)
            continue
        for i in message:
            if i['type'] == 'FriendMessage' and (
                    i['sender'] in fromchat):  # 判断监听到的消息是否为群消息
                messagechain = i['messagechain']
                command = messagechain[1]
                if command['type'] == 'Plain':
                    return command['text'], i['sender']
        time.sleep(0.5)


async def getcommand_tui():
    listen = My_Thread(target=getcommand_chat)
    listen.start()
    subadmin = My_Thread(target=ChatSubadmin.main)
    subadmin.start()
    autotask = My_Thread(target=RunAutoTask)
    autotask.start()
    session = PromptSession()
    while 1:
        #time.sleep(3)
        #print('->',end='')
        #command=input()
        #command=prompt('->')
        try:
            with patch_stdout():
                command = await session.prompt_async('\nChatLearning ->')
        except KeyboardInterrupt:
            print('ChatLearning控制台无法加载，可能是置于后台运行，或是程序退出')
            return None
        except:
            sys.stdout.flush()
            time.sleep(10)
            continue
        commandchoice(command)


def commandchoice(command, fromchat=0):
    global data
    global globesign
    global learningsign
    global mergesign
    global replysign
    global adminsign
    global voicereplysign
    global FastDeletesign
    command = command.lower()
    command = ' '.join(command.split())
    commandlist = commandclass(data, command)
    if command[:8] == 'learning':
        if command == 'learning':
            learningmodesign = learning(learningsign, mergesign, fromchat)
            learningsign = learningmodesign[0]
            mergesign = learningmodesign[1]
        elif command[:9] == 'learning ':
            learninginterval(command[9:], fromchat)
        else:
            commandlist.commandhelp(fromchat)
    elif command[:10] == 'replywait ':
        ReplyWait(command[10:], fromchat)
    elif command[:5] == 'reply':
        if command == 'reply':
            replysign = reply(replysign, fromchat)
        elif command[:6] == 'reply ':
            replychance(command[6:], fromchat)
        else:
            commandlist.commandhelp(fromchat)
    elif command[:10] == 'voicereply':
        if command == 'voicereply':
            voicereplysign = voicereply(voicereplysign, fromchat)
        elif command[:11] == 'voicereply ':
            voicereplychance(command[11:], fromchat)
        else:
            commandlist.commandhelp(fromchat)
    elif command == 'uploadwav':
        uploadwav(data, fromchat)
    elif command[:6] == 'merge ':
        try:
            time = int(command[6:])
            merge(time, fromchat)
        except:
            commandlist.commandhelp(fromchat)
            return None
    elif command == 'check':
        check(fromchat)
    elif command[:4] == 'add ':
        if addgroup(command[4:], fromchat) == 1:
            print('正在重启merge')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '正在重启merge', 1)
            remerge()
            pass
    elif command[:7] == 'remove ':
        if removegroup(command[7:], fromchat) == 1:
            print('正在重启merge')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '正在重启merge', 1)
            remerge()
            pass
    elif command == 'grouplist':
        grouplist(fromchat)
    elif command == 'globe':
        globesign = globe(globesign=globesign, fromchat=fromchat)
    elif command[:9] == 'setadmin ':
        setadmin(command[9:], fromchat)
    elif command == 'admin':
        adminsign = admin(adminsign, fromchat)
        return 'breaksign'
    elif command[:10] == 'blackfreq ':
        blackfreq(data, command[10:])
    elif command[:11] == 'setvoicept ':
        setvoicept(data, command[11:], fromchat)
    elif command[:9] == 'typefreq ':
        typefreq(data, command[9:], fromchat)
    elif command[:8] == 'settemp ':
        SetTempMessage(data, command[8:], fromchat)
    elif command == 'fastdelete':
        FastDeletesign = SetFastDeleteAdmin(FastDeletesign, fromchat)
    elif command == 'autotaskinfo':
        GetAutoTaskInfo(fromchat)
    elif command == 'autotaskcommand':
        AutoTaskCommand(fromchat)
    elif command == 'exit':
        exit()
    elif command == 'help' or command == '?' or command == '？':
        commandlist.printhelp(fromchat)
    else:
        commandlist.commandhelp(fromchat)


if __name__ == '__main__':
    global TaskDict
    hello()
    adminsendmode = 0
    globesign = globe(get=1)
    learningsign = ChatLearning.getconfig()[1]
    mergesign = 0
    replysign = ChatReply.getconfig(3)
    try:
        voicereplysign = ChatReply.getconfig(5)
    except:
        voicereplysign = 0
    try:
        FastDeletesign = ChatReply.getconfig(13)
    except:
        FastDeletesign = 0
    adminsign = 0
    data = simuse.Get_data()
    data = simuse.Get_Session(data)
    if learningsign == 1:
        learningsign = 0
        tempsign = learning(learningsign, mergesign, 0)
        learningsign = tempsign[0]
        mergesign = tempsign[1]
    if replysign == 1:
        replysign = 0
        time.sleep(0.8)
        replysign = reply(replysign, 0)
    TaskDict = GetAutoTask()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getcommand_tui())
