import os
import pickle
import re
import shutil
import threading
import time
import traceback
import platform

import simuse

version = '2.8.1'


# 控制台指令类
class commandclass():
    command = ''
    commandtips = {}
    commandtips['learning'] = '#开启/关闭记录'
    commandtips['reply'] = '#开启/关闭回复'
    commandtips['voicereply'] = '#开启/关闭文字转语音回复'
    commandtips['learning <秒>'] = '#设定词库链间隔时间'
    commandtips['reply <％>'] = '#设定回复的触发几率'
    commandtips['reply -s <％> <群号>'] = '#单独设定回复触发几率'
    commandtips['reply -d <群号>'] = '#清除单独设定的回复触发几率'
    commandtips['voicereply <％>'] = '#设定文字转语音回复几率'
    commandtips['voicereply -s <％> <群号>'] = '#单独设定文字转语音触发几率'
    commandtips['voicereply -d <群号>'] = '#清除单独设定的文字转语音触发几率'
    commandtips['merge <秒>'] = '#设定总词库更新时间'
    commandtips['typefreq <消息类型> <次数>'] = '#设定消息发送阈值'
    commandtips['add learning <群号>'] = '#添加开启记录的群'
    commandtips['add learnings <群号>'] = '#同时添加开启记录和回复的群'
    commandtips['add reply <群号>'] = '#添加开启回复的群'
    commandtips['add subadmin <群号>'] = '#添加可自行管理的群'
    commandtips['add unmerge <群号>'] = '#添加不录入总词库的群'
    commandtips['add tag <标签> <群号>'] = '#添加群标签'
    commandtips['remove learning <群号>'] = '#移除开启记录的群'
    commandtips['remove reply <群号>'] = '#移除开启回复的群'
    commandtips['remove subadmin <群号>'] = '#移除可自行管理的群'
    commandtips['remove unmerge <群号>'] = '#移除不录入总词库的群'
    commandtips['remove tag <群号>'] = '#移除群标签'
    commandtips['check'] = '#查看设置情况'
    commandtips['grouplist'] = '#查看开启记录/回复的群列表'
    commandtips['globe'] = '#开启/关闭全局模式'
    commandtips['setadmin <QQ号>'] = '#设置管理员QQ号'
    commandtips['setvoicept <训练集>'] = '#设置文字转语音回复的训练集'
    commandtips['blackfreq <次数>'] = '#设置黑名单容错次数'
    commandtips['uploadwav'] = '#上传源音频文件'
    commandtips['admin'] = '#进入管理模式'
    commandtips['exit'] = '#退出程序'

    def __init__(self, data, input):
        self.command = input.strip('*')
        self.command = self.command.strip(' ')
        self.data = data

    def printhelp(self, fromchat):
        print('指令列表：')
        sendtext = ''
        for i in self.commandtips:
            sendtext = sendtext + i + self.commandtips[i] + '\n'
            print(i, '   ', self.commandtips[i])
        print('\n')
        if fromchat != 0:
            simuse.Send_Message(self.data, fromchat, 2, sendtext, 1)

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
                        self.data, fromchat, 2,
                        '未知指令"{}"   你是否想输入以下指令？'.format(self.command), 1)
                for i in self.fuzzyfinder(self.command):
                    print(i, '   ', self.commandtips[i])
                    sendtext = sendtext + i + self.commandtips[i] + '\n'
                if sendtext != '':
                    simuse.Send_Message(self.data, fromchat, 2, sendtext, 1)
            else:
                print('<-未知指令"{}"   请输入help/?查看帮助'.format(self.command))
                if fromchat != 0:
                    simuse.Send_Message(
                        self.data, fromchat, 2,
                        '未知指令"{}"   请输入help/?查看帮助'.format(self.command), 1)
        except:
            print('<-未知指令"{}"   请输入help/?查看帮助'.format(self.command))
            if fromchat != 0:
                simuse.Send_Message(
                    self.data, fromchat, 2,
                    '未知指令"{}"   请输入help/?查看帮助'.format(self.command), 1)


# 多线程类的复写
class My_Thread(threading.Thread):
    daemon = True

    def run(self):
        # 常驻为守护线程
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except:
            log = open('log.log', 'a', encoding='utf-8-sig')
            traceback_str = traceback.format_exc()
            log.write(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' +
                traceback_str + '\n')
            log.close()
            print('抛出异常，已记录到日志(log.log文件)')
            print(traceback_str)
        finally:
            del self._target, self._args, self._kwargs


# 返回版本号
def Version():
    global version
    return version


# 2.7.0前版本更新需要更换词库的缓存形式
def ClChange():
    try:
        filelist = os.listdir('WordStock')  # 获取词库列表
    except:
        filelist = os.listdir()  # 获取词库列表
    cllist = []
    for i in filelist:
        if i[-3:] == '.cl':
            #print(i)
            cllist.append(i)
    #print(cllist)
    print('正在为更新做一些准备，请稍等')
    print('期间请勿关闭程序，否则将导致数据丢失！')
    for i in cllist:
        file = open(i, 'r', encoding='utf-8-sig')
        dicts = file.read()
        dicts = eval(dicts)
        file.close()
        pickle.dump(dicts, open(i, 'wb'))
    print('准备完毕！')


def Cl_version(version):
    version = int(version.replace('.', ''))
    try:
        filelist = os.listdir('WordStock')  # 获取词库列表
    except:
        filelist = os.listdir()
    cllist = []
    if not (os.path.exists('WordStock')):
        os.mkdir('WordStock')
    for i in filelist:
        if i[-3:] == '.cl':
            #print(i)
            cllist.append(i)
    #print(cllist)
    # 2.8.0前版本更新需要为词库Key添加"freq"次数键
    if version < 280:
        print('正在更新词库版本,{} -> 280 请勿中途退出'.format(version))
        for i in cllist:
            dicts = pickle.load(open(i, 'rb'))
            for k in dicts.keys():
                questiondict = dicts[k]
                if not ('freq' in questiondict.keys()):
                    questiondict['freq'] = 1
            pickle.dump(dicts, open(i, 'wb'))
            shutil.move(i, 'WordStock/' + i)


def Config_version(version):
    version = int(version.replace('.', ''))
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = eval(file.read())
    file.close()
    if version < 280:
        print('正在更新config, -> 280 请勿中途退出')
        config['tag'] = {}
        config['singlereplychance'] = {}
        config['singlevoicereplychance'] = {}
        config['typefreq'] = {}
    return config
