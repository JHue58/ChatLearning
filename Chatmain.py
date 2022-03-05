import asyncio
import re
import threading
import time
import base64
import nest_asyncio
import os
import json
import requests
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from qcloud_cos import CosConfig, CosS3Client

import ChatAdmin
import ChatAllfind
import ChatCheck
import ChatFilter
import ChatLearning
import ChatMerge
import ChatReply
import simuse

nest_asyncio.apply()
version = '2.5.0'


class commandclass():
    command = ''
    commandtips = {}
    commandtips['learning'] = '#开启/关闭记录'
    commandtips['reply'] = '#开启/关闭回复'
    commandtips['voicereply']='#开启/关闭文字转语音回复'
    commandtips['learning *'] = '#设定词库链间隔时间，*的单位为秒'
    commandtips['reply *'] = '#设定回复的触发几率'
    commandtips['voicereply *']='#设定文字转语音回复几率'
    commandtips['merge *'] = '#设定总词库更新时间，*的单位为秒'
    commandtips['add learning *'] = '#添加开启记录的群，有多个用空格隔开'
    commandtips['add learnings *'] = '#同时添加开启记录和回复的群，有多个用空格隔开'
    commandtips['add reply *'] = '#添加开启回复的群，有多个用空格隔开'
    commandtips['add unmerge *'] = '#添加不录入总词库的群，有多个用空格隔开'
    commandtips['remove learning *'] = '#移除开启记录的群，有多个用空格隔开'
    commandtips['remove reply *'] = '#移除开启回复的群，有多个用空格隔开'
    commandtips['remove unmerge *'] = '#移除不录入总词库的群，有多个用空格隔开'
    commandtips['check'] = '#查看词库的问答个数'
    commandtips['grouplist'] = '#查看开启记录/回复的群列表'
    commandtips['globe'] = '#开启/关闭全局模式'
    commandtips['setadmin *'] = '#设置管理员QQ号，有多个用空格隔开'
    commandtips['setvoicept *']='#设置文字转语音回复的训练集'
    commandtips['blackfreq *'] = '#设置黑名单容错次数'
    commandtips['uploadwav']='#上传源音频文件'
    commandtips['admin'] = '#进入管理模式'

    def __init__(self, input):
        self.command = input.strip('*')
        self.command = self.command.strip(' ')

    def printhelp(self, fromchat):
        print('指令列表：')
        sendtext = ''
        for i in self.commandtips:
            sendtext = sendtext + i + self.commandtips[i] + '\n'
            print(i, '   ', self.commandtips[i])
        print('\n')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, sendtext, 1)

    def commandlist(self):
        return list(self.commandtips.keys())

    def fuzzyfinder(self, user_input):
        collection = self.commandlist()
        suggestions = []
        pattern = '.*?'.join(user_input)
        regex = re.compile(pattern)
        for i in collection:
            match = regex.search(i)
            if match:
                suggestions.append((len(match.group()), match.start(), i))
        return [x for _, _, x in sorted(suggestions)]

    def commandhelp(self, fromchat):
        sendtext = ''
        try:
            if self.fuzzyfinder(self.command) != [] and self.command != '':
                print('<-未知指令"{}"   你是否想输入以下指令？'.format(self.command))
                if fromchat != 0:
                    simuse.Send_Message(
                        data, fromchat, 2,
                        '未知指令"{}"   你是否想输入以下指令？'.format(self.command), 1)
                for i in self.fuzzyfinder(self.command):
                    print(i, '   ', self.commandtips[i])
                    sendtext = sendtext + i + self.commandtips[i] + '\n'
                if sendtext != '':
                    simuse.Send_Message(data, fromchat, 2, sendtext, 1)
            else:
                print('<-未知指令"{}"   请输入help/?查看帮助'.format(self.command))
                if fromchat != 0:
                    simuse.Send_Message(
                        data, fromchat, 2,
                        '未知指令"{}"   请输入help/?查看帮助'.format(self.command), 1)
        except:
            print('<-未知指令"{}"   请输入help/?查看帮助'.format(self.command))
            if fromchat != 0:
                simuse.Send_Message(
                    data, fromchat, 2,
                    '未知指令"{}"   请输入help/?查看帮助'.format(self.command), 1)


def hello():
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    file.close()
    config = eval(config)
    config['reply'] = 0
    config['merge'] = 0
    config['learning'] = 0
    config['admin'] = 0
    file = open('config.clc', 'w', encoding='utf-8-sig')
    file.write(str(config))
    file.close()
    global version
    print('欢迎使用ChatLearning应用 版本号：', version)
    #print('遇到问题和bug请在mirai论坛回复我或发送至我的邮箱1121917292@qq.com')
    print('输入help来查看指令列表吧！')


def unknowcommand(command):
    print('<-未知指令"{}"   请输入help/?查看帮助'.format(command))
    pass


def uploadwav(data,fromchat=0):
    try:
        wavsize=os.path.getsize('source.wav')
    except:
        print('未找到source.wav文件！')
        if fromchat!=0:
            simuse.Send_Message(data, fromchat, 2, '未找到source.wav文件！', 1)
        return None
    wav_kb=wavsize/float(1024)
    if wav_kb>=10240:
        print('文件大小超过10M！取消上传')
        if fromchat!=0:
            simuse.Send_Message(data, fromchat, 2, '文件大小超过10M！取消上传', 1)
        return None
    wavfile=open('source.wav','rb')
    base64_data=base64.b64encode(wavfile.read())
    wavfile.close()
    data_in={'QQ':data['qq'],'base64':base64_data.decode()}
    url='http://124.222.165.166:19630/Sourcewav'
    try:
        print('正在等待服务器响应')
        simuse.Send_Message(data, fromchat, 2, '正在等待服务器响应', 1)
        res=requests.request('post',url=url,json=data_in,timeout=20)
        res=json.loads(res.text)
    except:
        print('上传失败,服务器未响应')
        if fromchat!=0:
            simuse.Send_Message(data, fromchat, 2, '上传失败,服务器未响应', 1)
            return None
    try:
        if res['code']==1:
            print('上传成功！')
            if fromchat!=0:
                simuse.Send_Message(data, fromchat, 2, '上传成功！', 1)
            return None
        else:
            print('上传失败！')
            if fromchat!=0:
                simuse.Send_Message(data, fromchat, 2, '上传失败！', 1)
            return None
    except:
        print('上传失败！')
        if fromchat!=0:
            simuse.Send_Message(data, fromchat, 2, '上传失败！', 1)
        return None

        
def testvoice(data,text,fromchat=0):
    if fromchat==0:
        print('请在聊天环境下进行')
        return None
    if ChatReply.canToVoice(text):
        if ChatReply.CanSendTask():
            answer=ChatReply.Plain_Voice(data,text)
            if answer==None:
                print('转换失败')
                if fromchat!=0:
                    simuse.Send_Message(data, fromchat, 2, '转换失败', 1)
                return None
            else:
                simuse.Send_Message_Chain(data,fromchat,2,answer)
        else:
            print('转换失败，服务器队列已满')
            if fromchat!=0:
                simuse.Send_Message(data, fromchat, 2, '转换失败，服务器队列已满', 1)
            return None
    else:
        print('转换失败，存在不支持的字符')
        if fromchat!=0:
            simuse.Send_Message(data, fromchat, 2, '转换失败，存在不支持的字符', 1)




def blackfreq(num, fromchat=0):
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    file.close()
    config = eval(config)
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
    file.write(str(config))
    file.close()
    print('黑名单容错次数已设置为{}次'.format(num))
    if fromchat != 0:
        simuse.Send_Message(data, fromchat, 2, '黑名单容错次数已设置为{}次'.format(num), 1)


def setvoicept(data,ptname,fromchat=0):
    url="http://124.222.165.166:19630/Ptlist"
    try:
        print('正在等待服务器响应')
        if fromchat!=0:
            simuse.Send_Message(data, fromchat, 2, '正在等待服务器响应', 1)
        res=requests.request('get',url,timeout=20)
        res=json.loads(res.text)
    except:
        print('设置失败,服务器未响应')
        if fromchat!=0:
            simuse.Send_Message(data, fromchat, 2, '设置失败,服务器未响应', 1)
            return None
    ptlist=res['ptlist']
    if not(ptname in ptlist):
        sendptlist=''
        for i in ptlist:
            sendptlist=sendptlist+i+' '
        print('该训练集不存在')
        print('服务器中存在的训练集：\n'+sendptlist)
        if fromchat!=0:
            simuse.Send_Message(data, fromchat, 2, '该训练集不存在\n服务器中存在的训练集：\n'+sendptlist, 1)
        return None
    file=open('config.clc','r',encoding='utf-8-sig')
    config=eval(file.read())
    file.close()
    config['synthesizer']=ptname
    file=open('config.clc','w',encoding='utf-8-sig')
    file.write(str(config))
    file.close()
    print('训练集已更改为{}'.format(ptname))
    if fromchat!=0:
        simuse.Send_Message(data, fromchat, 2, '训练集已更改为{}'.format(ptname), 1)
    



def remerge():
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    file.close()
    config = eval(config)
    config['merge'] = 1
    file = open('config.clc', 'w', encoding='utf-8-sig')
    file.write(str(config))
    file.close()
    merge = threading.Thread(target=ChatMerge.main)
    merge.start()


def globe(globesign=0, get=0, fromchat=0):
    global data
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    config = eval(config)
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
    file.write(str(config))
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
    config = file.read()
    file.close()
    config = eval(config)
    config['Administrator'] = adminlist
    file = open('config.clc', 'w', encoding='utf-8-sig')
    file.write(str(config))
    print('管理员QQ号已设置为', adminlist)
    if fromchat != 0:
        simuse.Send_Message(data, fromchat, 2, '管理员QQ号已设置为' + str(adminlist),
                            1)


def admin(adminsign, fromchat=0):
    global adminsendmode
    global learningsign
    global mergesign
    global replysign
    if fromchat == 0:
        print('请在聊天环境中执行该指令')
        return adminsign
    if learningsign == 1:
        tempsign = learning(learningsign, mergesign, fromchat)
        learningsign = tempsign[0]
        mergesign = tempsign[1]
    if replysign == 1:
        time.sleep(0.8)
        replysign = reply(replysign, fromchat)
    if adminsign == 0:
        time.sleep(0.8)
        print('<-进入管理模式')
        print('请不要操作控制台！！！')
        #print('拥有词库的群号:')
        #print(ChatAdmin.getfilelist())
        tips = '请发送需要操作的序号\n1.在所有群内查找\n2.在指定群内查找\n3.过滤设置'
        simuse.Send_Message(data, fromchat, 2, tips, 1)
        command = getcommand_chat_foradmin()
        choice = command[0]
        sender = command[1]
        if choice == str(1):
            ChatAllfind.findallcontrol(data, fromchat)
            print(('<-退出管理模式'))
            simuse.Send_Message(data, fromchat, 2, '退出管理模式', 1)
            return adminsign
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
                group = int(group)
            except:
                print('参数错误')
                print('<-退出管理模式')
                if fromchat != 0:
                    simuse.Send_Message(data, fromchat, 2, '参数错误,退出管理模式', 1)
                return adminsign
            file = open('config.clc', 'r', encoding='utf-8-sig')
            config = file.read()
            file.close()
            config = eval(config)
            config['admin'] = 1
            file = open('config.clc', 'w', encoding='utf-8-sig')
            file.write(str(config))
            file.close()
            ChatAdmin.main(data, config['Administrator'], group, sender)
            #admin=threading.Thread(target=ChatAdmin.main,args=(config['Administrator'],group))
            #adminsign=1
            #admin.join()
            #listen = threading.Thread(target=getcommand_chat)
            #listen.start()
            return adminsign
        elif choice == str(3):
            ChatFilter.filtercontrol(data, fromchat)
            print('<-退出管理模式')
            simuse.Send_Message(data, fromchat, 2, '退出管理模式', 1)
            return adminsign
        else:
            print('参数错误')
            print('<-退出管理模式')
            if fromchat != 0:
                simuse.Send_Message(data, fromchat, 2, '参数错误,退出管理模式', 1)
            return adminsign


def grouplist(fromchat=0):
    global data
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    config = eval(config)
    file.close()
    learninggrouplist = config['learninggrouplist']
    replygrouplist = config['replygrouplist']
    unmergegrouplist = config['unmergegrouplist']
    Administrator = config['Administrator']
    print('管理员QQ号：', Administrator)
    print('已开启记录的群：', learninggrouplist)
    print('已开启答复的群：', replygrouplist)
    print('不录入总词库的群：', unmergegrouplist)
    if fromchat != 0:
        sendtext = '管理员QQ号：' + str(Administrator) + '\n' + '已开启记录的群：' + str(
            learninggrouplist) + '\n' + '已开启答复的群：' + str(
                replygrouplist) + '\n' + '不录入总词库的群：' + str(unmergegrouplist)
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
    config = file.read()
    config = eval(config)
    file.close()
    config['interval'] = interval
    file2 = open('config.clc', 'w', encoding='utf-8-sig')
    file2.write(str(config))


def replychance(chance, fromchat=0):
    global data
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
    config = file.read()
    config = eval(config)
    file.close()
    config['replychance'] = chance
    file2 = open('config.clc', 'w', encoding='utf-8-sig')
    file2.write(str(config))

def voicereplychance(chance, fromchat=0):
    global data
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
    config = file.read()
    config = eval(config)
    file.close()
    config['voicereplychance'] = chance
    file2 = open('config.clc', 'w', encoding='utf-8-sig')
    file2.write(str(config))


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
        config = file.read()
        file.close()
        config = eval(config)
        config['learninggrouplist'].extend(grouplist)
        config['learninggrouplist'] = list(set(config['learninggrouplist']))
        if args[:10] == 'learnings ':
            config['replygrouplist'].extend(grouplist)
            config['replygrouplist'] = list(set(config['replygrouplist']))
        file = open('config.clc', 'w', encoding='utf-8-sig')
        file.write(str(config))
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
        config = file.read()
        file.close()
        config = eval(config)
        config['replygrouplist'].extend(grouplist)
        config['replygrouplist'] = list(set(config['replygrouplist']))
        file = open('config.clc', 'w', encoding='utf-8-sig')
        file.write(str(config))
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
        config = file.read()
        file.close()
        config = eval(config)
        config['unmergegrouplist'].extend(grouplist)
        config['unmergegrouplist'] = list(set(config['unmergegrouplist']))
        config['merge'] = 0
        file = open('config.clc', 'w', encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-添加完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '添加完毕', 1)
        return config['learning']
        pass
    else:
        print('参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None
    pass


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
        config = file.read()
        file.close()
        config = eval(config)
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
        file.write(str(config))
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
        config = file.read()
        file.close()
        config = eval(config)
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
        file.write(str(config))
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
        config = file.read()
        file.close()
        config = eval(config)
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
        file.write(str(config))
        file.close()
        print('<-移除完毕')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '移除完毕', 1)
        return config['learning']
        pass
    else:
        print('参数错误')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '参数错误', 1)
        return None
    pass


def learning(learningsign, mergesign, fromchat=0):
    global data
    if learningsign == 0 and mergesign == 0:
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = file.read()
        file.close()
        config = eval(config)
        config['learning'] = 1
        config['merge'] = 1
        file = open('config.clc', 'w', encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-开始记录')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '开始记录', 1)
        learning = threading.Thread(target=ChatLearning.main)
        merge = threading.Thread(target=ChatMerge.main)
        learningsign = 1
        mergesign = 1
        learning.start()
        merge.start()
        return learningsign, mergesign
    else:
        learningsign = 0
        mergesign = 0
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = file.read()
        file.close()
        config = eval(config)
        config['learning'] = 0
        config['merge'] = 0
        file = open('config.clc', 'w', encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-停止记录')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '停止记录', 1)
        return learningsign, mergesign


def reply(replysign, fromchat=0):
    global data
    if replysign == 0:
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = file.read()
        file.close()
        config = eval(config)
        config['reply'] = 1
        file = open('config.clc', 'w', encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-开启回复功能')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '开启回复功能', 1)
        reply = threading.Thread(target=ChatReply.main)
        replysign = 1
        reply.start()
        return replysign
    else:
        replysign = 0
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = file.read()
        file.close()
        config = eval(config)
        config['reply'] = 0
        file = open('config.clc', 'w', encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-关闭回复功能')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '关闭回复功能', 1)
        return replysign

def voicereply(voicereplysign, fromchat=0):
    global data
    if voicereplysign == 0:
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = file.read()
        file.close()
        config = eval(config)
        config['voicereply'] = 1
        file = open('config.clc', 'w', encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-开启语音回复功能')
        if fromchat != 0:
            simuse.Send_Message(data, fromchat, 2, '开启语音回复功能', 1)
        reply = threading.Thread(target=ChatReply.main)
        voicereplysign = 1
        reply.start()
        return voicereplysign
    else:
        voicereplysign = 0
        file = open('config.clc', 'r', encoding='utf-8-sig')
        config = file.read()
        file.close()
        config = eval(config)
        config['voicereply'] = 0
        file = open('config.clc', 'w', encoding='utf-8-sig')
        file.write(str(config))
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
    config = file.read()
    config = eval(config)
    file.close()
    config['mergetime'] = time
    file2 = open('config.clc', 'w', encoding='utf-8-sig')
    file2.write(str(config))


def check(fromchat=0):
    global data
    check = threading.Thread(target=ChatCheck.main, args=(data, fromchat))
    check.start()
    check.join()


def getcommand_chat():
    global data
    global adminsendmode
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
    listen = threading.Thread(target=getcommand_chat)
    listen.start()
    session = PromptSession()
    while 1:
        #time.sleep(3)
        #print('->',end='')
        #command=input()
        #command=prompt('->')
        try:
            with patch_stdout():
                command = await session.prompt_async('\nChatLearning ->')
        except:
            print('ChatLearning控制台无法加载，可能是置于后台运行')
        commandchoice(command)


def commandchoice(command, fromchat=0):
    command = command.lower()
    commandlist = commandclass(command)
    global data
    global globesign
    global learningsign
    global mergesign
    global replysign
    global adminsign
    global voicereplysign
    if command[:8] == 'learning':
        if command == 'learning':
            learningmodesign = learning(learningsign, mergesign, fromchat)
            learningsign = learningmodesign[0]
            mergesign = learningmodesign[1]
        elif command[:9] == 'learning ':
            learninginterval(command[9:], fromchat)
        else:
            commandlist.commandhelp(fromchat)
    elif command[:5] == 'reply':
        if command == 'reply':
            replysign = reply(replysign, fromchat)
        elif command[:6] == 'reply ':
            replychance(command[6:], fromchat)
        else:
            commandlist.commandhelp(fromchat)
    elif command[:10]=='voicereply':
        if command=='voicereply':
            voicereplysign=voicereply(voicereplysign,fromchat)
        elif command[:11]=='voicereply ':
            voicereplychance(command[11:],fromchat)
        else:
            commandlist.commandhelp(fromchat)
    elif command=='uploadwav':
        uploadwav(data,fromchat)
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
        blackfreq(command[10:])
    elif command[:11]=='setvoicept ':
        setvoicept(data,command[11:],fromchat)
    elif command == 'help' or command == '?' or command == '？':
        commandlist.printhelp(fromchat)
    else:
        commandlist.commandhelp(fromchat)


adminsendmode = 0
globesign = globe(get=1)
learningsign = 0
mergesign = 0
replysign = 0
try:    
    voicereplysign=ChatReply.getconfig(5)
except:
    voicereplysign=0
adminsign = 0
data = simuse.Get_data()
data = simuse.Get_Session(data)
hello()
loop = asyncio.get_event_loop()
loop.run_until_complete(getcommand_tui())
