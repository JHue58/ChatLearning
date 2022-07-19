import copy
import datetime
import json
import os
import pickle
import platform
import re
import shutil
import threading
import time
import traceback
from asyncio import Task

import requests
#import tqdm

import simuse

version = '2.9.8'


def pickle_dump(obj, file):
    while True:
        try:
            pickle.dump(obj, file)
            break
        except:
            time.sleep(0.1)
            continue
    return True


def pickle_load(file):
    while True:
        try:
            obj = pickle.load(file)
            break
        except:
            time.sleep(0.1)
            continue
    return obj


def json_dump(obj, file, indent=3, ensure_ascii=False):
    while True:
        try:
            json.dump(obj, file, indent=indent, ensure_ascii=ensure_ascii)
            break
        except:
            time.sleep(0.1)
            continue
    return True


def json_load(file):
    while True:
        try:
            obj = json.load(file)
            break
        except:
            time.sleep(0.1)
            continue
    return obj


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
    commandtips['replywait <基准时间> <浮动时间>'] = '#设定回复的等待时间'
    commandtips['replycd <秒>'] = '#设定回复的冷却时间'
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
    commandtips['add autotask <任务名称>'] = '#添加定时任务'
    commandtips['remove learning <群号>'] = '#移除开启记录的群'
    commandtips['remove reply <群号>'] = '#移除开启回复的群'
    commandtips['remove subadmin <群号>'] = '#移除可自行管理的群'
    commandtips['remove unmerge <群号>'] = '#移除不录入总词库的群'
    commandtips['remove tag <群号>'] = '#移除群标签'
    commandtips['remove autotask <任务名称>'] = '#移除定时任务'
    commandtips['autotaskinfo'] = '#查看定时任务详情'
    commandtips['fastdelete'] = '#更改快速清除的权限'
    commandtips['check'] = '#查看设置情况'
    commandtips['grouplist'] = '#查看开启记录/回复的群列表'
    commandtips['globe'] = '#开启/关闭全局模式'
    commandtips['setadmin <QQ号>'] = '#设置管理员QQ号'
    commandtips['setvoicept <训练集>'] = '#设置文字转语音回复的训练集'
    commandtips['settemp <条数>'] = '#设置单个群中消息缓存最大数目'
    commandtips['blackfreq <次数>'] = '#设置黑名单容错次数'
    commandtips['uploadwav'] = '#上传源音频文件'
    commandtips['autotaskcommand'] = '#查看定时任务的特殊指令'
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
        print('管理员可通过私聊Bot，开头加上感叹号来执行相应的指令\n')
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


# 定时任务类
class TimeTask():

    TaskName = ''

    ISDisposable = 1

    Tips = {}
    ErrorTips = ''

    SendList = []
    TimeList = []
    DayList = []
    TaskList = []
    TimeList_Origin = []

    runday = ''
    AfterDay = 0

    def __init__(self, TaskName: str, TaskText: str = None) -> None:
        self.Default()

        self.TaskName = TaskName
        if TaskText == None:
            TaskPath = 'AutoTask/{}.txt'.format(TaskName)
            with open(TaskPath, 'r', encoding='utf-8') as TaskFile:
                TextList = TaskFile.readlines()
        else:
            TextList = TaskText.split('\n')
        for lines in TextList:
            lines = ' '.join(lines.split())
            if lines == '':
                continue

            if lines[0] == '#':
                self.DayList.extend(lines[1:].split(' '))
            elif lines[0] == '*':
                self.TimeList.extend(lines[1:].split(' '))
            elif lines[0] == '@':
                self.SendList.extend(lines[1:].split(' '))
            elif lines[0] == '/':
                self.TaskList.append(lines[1:])

        self.TimeList_Origin = copy.deepcopy(self.TimeList)

    # 初始化
    def Default(self):
        self.TaskName = ''
        self.ISDisposable = 1
        self.Tips = {}
        self.ErrorTips = ''
        self.SendList = []
        self.TimeList = []
        self.DayList = []
        self.TaskList = []
        self.runday = datetime.datetime.now().strftime('%d')

    # 解析任务
    def CheckTask(self) -> bool:
        week = ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7']
        week_C = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

        SendTips = ''
        DayTips = ''
        TimeTips = ''
        TaskTips = ''

        # 解析发送结果QQ
        for sendqq in self.SendList:
            try:
                int(sendqq)
            except:
                SendTips = 'SendError'
            else:
                SendTips = SendTips + sendqq + ' '

        # 解析日期
        for days in self.DayList:
            if days == 'everyday':
                DayTips = DayTips + '每日 '
                self.ISDisposable = 0
                break
            elif days in week:
                self.ISDisposable = 0
                DayTips = DayTips + week_C[week.index(days)] + ' '
            elif days[0] == 'x':
                try:
                    if int(days[1:]) <= 0:
                        continue
                    DayTips = DayTips + '每' + str(int(days[1:])) + '天' + ' '
                    self.ISDisposable = 0
                except:
                    continue
            else:
                try:
                    datetime.datetime.strptime(days, '%Y-%m-%d')
                except:
                    continue
                else:
                    DayTips = DayTips + days + ' '

        # 解析时间
        for times in self.TimeList:
            try:
                datetime.datetime.strptime(times, '%H:%M')
            except:
                continue
            else:
                TimeTips = TimeTips + times + ' '

        # 解析指令
        for task in self.TaskList:
            TaskTips = TaskTips + task + '\n'

        Tips = '无法解析任务的 '

        if SendTips == 'SendError':
            Tips = Tips + '执行结果反馈QQ号 '
        if DayTips == '':
            Tips = Tips + '执行日期 '
        if TimeTips == '':
            Tips = Tips + '执行时间 '
        if TaskTips == '':
            Tips = Tips + '执行指令 '

        if Tips != '无法解析任务的 ':
            self.ErrorTips = Tips
            return 0
        else:
            self.Tips = {
                "执行结果反馈QQ号": SendTips,
                "执行日期": DayTips,
                "执行时间": TimeTips,
                "执行指令": TaskTips
            }
            return 1

    # 重写__repr__
    def __repr__(self):
        return self.TaskName

    # 返回任务详情
    def TaskInfo(self):
        String = "任务名称:" + self.TaskName + "\n执行结果反馈QQ号:" + self.Tips[
            "执行结果反馈QQ号"] + "\n执行日期:" + self.Tips[
                "执行日期"] + "\n执行时间:" + self.Tips[
                    "执行时间"] + "\n执行指令:\n" + self.Tips["执行指令"]
        return String

    # 判断是否达到任务执行时间
    def ISTaskTime(self) -> bool:

        nowtime = datetime.datetime.now().strftime('%H:%M')
        nowday = datetime.datetime.now().strftime('%Y-%m-%d')
        weekday = datetime.datetime.now().weekday() + 1
        today = datetime.datetime.now().strftime('%d')

        #判断日期是否变化
        if today != self.runday:
            self.TimeList = copy.deepcopy(self.TimeList_Origin)
            self.runday = today
            self.AfterDay += 1

        daysign = 0

        for days in self.DayList:
            if days == 'everyday':
                daysign = 1
            elif days == 'w' + str(weekday):
                daysign = 1
            elif days == 'x' + str(self.AfterDay) and self.AfterDay > 0:
                daysign = 1
                self.AfterDay = 0
            elif days == nowday:
                daysign = 1

        if daysign == 1:
            for Time in self.TimeList:
                if Time == nowtime:
                    self.TimeList.remove(Time)
                    return 1
        else:
            return 0


# 多线程类的复写
class My_Thread(threading.Thread):
    Trynum = 0

    # 常驻为守护线程
    daemon = True

    def TrynumSet(self, Trynum):
        self.Trynum = Trynum

    def Raise_log(self, traceback_str):
        log = open('log.log', 'a', encoding='utf-8-sig')
        log.write(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' +
            traceback_str + '\n')
        log.close()
        print('抛出异常，已记录到日志(log.log文件)')
        print(traceback_str)

    def run(self):
        if self._target:
            try:
                self._target(*self._args, **self._kwargs)
            except ConnectionError:
                if self.Trynum == 0:
                    print('{}：未与api-http取得连接，或mirai未登录'.format(self._target))
                print('{}：正在进行第{}次重试'.format(self._target.__name__,
                                             self.Trynum + 1))
                time.sleep(2)
                New_Thread = My_Thread(target=self._target, args=self._args)
                New_Thread.TrynumSet(self.Trynum + 1)
                New_Thread.start()
            except requests.exceptions.ConnectionError:
                #print('{}：与api-http连接被强制中断'.format(self._target))
                self.Raise_log('{}：与api-http连接被强制中断'.format(self._target))
                New_Thread = My_Thread(target=self._target, args=self._args)
                New_Thread.start()
            except:
                self.Raise_log(traceback.format_exc())

        #finally:
        #    del self._target, self._args, self._kwargs


# 返回版本号
def Version():
    global version
    return version


def stop_run():

    config = json_load(open('config.clc', 'r', encoding='utf-8-sig'))
    sign = config["stopsign"]

    if sign == 0:
        return False
    elif sign == 1:
        return True


# 更新类
class Update():

    def __init__(self, config_version) -> None:
        self.version = config_version
        self.version = int(self.version.replace('.', ''))

    # def down_new_file(self, data={'qq': '123456'}):
    #     url = 'http://124.222.165.166:19630/Update'
    #     try:
    #         res = requests.request('get', url=url, timeout=20)
    #         res = json.loads(res.text)
    #     except:
    #         return None

    #     server_version = int(res['version'].replace('.', ''))
    #     server_version_format = res['version']

    #     if server_version > self.version:
    #         try:
    #             url = "http://124.222.165.166:19630/DownLoadFile"
    #             data_in = {
    #                 'version': self.version,
    #                 'system': platform.system(),
    #                 'qq': data['qq']
    #             }
    #             res = requests.request('post', url, json=data_in, stream=True)
    #         except:
    #             return None
    #         print('正在下载……')
    #         total = int(res.headers.get('content-length', 0))
    #         with open('ChatLearning_new', 'wb') as file, tqdm.tqdm(
    #                 desc='ChatLearning_v{}'.format(server_version_format),
    #                 total=total,
    #                 unit='iB',
    #                 unit_scale=True,
    #                 unit_divisor=1024) as bar:
    #             for file_data in res.iter_content(chunk_size=1024):
    #                 size = file.write(file_data)
    #                 bar.update(size)

    #         return 1, server_version_format
    #     else:
    #         return 0, server_version_format

    # 2.7.0前版本更新需要更换词库的缓存形式
    def ClChange(self):
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
            pickle_dump(dicts, open(i, 'wb'))
        print('准备完毕！')

    def Cl_version(self):
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
        if self.version < 280:
            print('正在更新词库版本,{} -> 280 请勿中途退出'.format(self.version))
            for i in cllist:
                dicts = pickle_load(open(i, 'rb'))
                for k in dicts.keys():
                    questiondict = dicts[k]
                    if not ('freq' in questiondict.keys()):
                        questiondict['freq'] = 1
                pickle_dump(dicts, open(i, 'wb'))
                shutil.move(i, 'WordStock/' + i)

    def Config_version(self):

        file = open('config.clc', 'r', encoding='utf-8-sig')
        try:
            config = json.load(file)
        except json.decoder.JSONDecodeError:
            file.close()
            file = open('config.clc', 'r', encoding='utf-8-sig')
            config = eval(file.read())
        file.close()
        # 280版本功能加入
        if self.version < 280:
            print('正在更新config, -> 280 请勿中途退出')
            config['tag'] = {}
            config['singlereplychance'] = {}
            config['singlevoicereplychance'] = {}
            config['typefreq'] = {}
        # 290版本功能加入
        if self.version < 290:
            print('正在更新config, -> 290 请勿中途退出')
            config['tempmessagenum'] = 32
            config['fastdelete'] = 0
        if self.version < 295:
            print('正在更新config, -> 295 请勿中途退出')
            config['replywait'] = [0, 0]
            config['voicecharerror'] = '存在违规字符，转换失败'
            config['voicecderror'] = '转换冷却中'
            config['voicelengtherror'] = '长度超过限制'
        if self.version < 297:
            print('正在更新config, -> 297 请勿中途退出')
            config['deletesuccess'] = '已从词库内删除！'
            config['deletetemperror'] = '删除失败，该消息已不在缓存内'
            config['deletefinderror'] = '删除失败，词库中已无法找到该答案'
        if self.version < 298:
            print('正在更新config, -> 298 请勿中途退出')
            config['replycd'] = 3
            config['stopsign'] = 0
            config['voicecommand'] = '快说 '

        return config
