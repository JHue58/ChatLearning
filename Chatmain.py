import threading
import re
import ChatLearning
import ChatReply
import ChatMerge
import ChatCheck
import ChatAdmin
import asyncio
import nest_asyncio
import time
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
nest_asyncio.apply()
version='1.0.0'

class commandclass():
    command=''
    commandtips={}
    commandtips['learning']='#开启/关闭记录'
    commandtips['reply']='#开启/关闭回复'
    commandtips['learning *']='#设定词库链间隔时间，*的单位为秒'
    commandtips['reply *']='#设定回复的触发几率'
    commandtips['merge *']='#设定总词库更新时间，*的单位为秒'
    commandtips['add learning *']='#添加开启记录的群，有多个用,隔开'
    commandtips['add reply *']='#添加开启回复的群，有多个用,隔开'
    commandtips['add unmerge *']='#添加不录入总词库的群，有多个用,隔开'
    commandtips['remove learning *']='#移除开启记录的群，有多个用,隔开'
    commandtips['remove reply *']='#移除开启回复的群，有多个用,隔开'
    commandtips['remove unmerge *']='#移除不录入总词库的群，有多个用,隔开'
    commandtips['check']='#查看词库的问答个数'
    commandtips['grouplist']='#查看开启记录/回复的群列表'
    commandtips['globe']='#开启/关闭全局模式'
    commandtips['setadmin *']='#设置管理员QQ号，仅能存在一个'
    commandtips['admin']='#进入管理模式'

    def __init__(self,input):
        self.command=input.strip('*')
        self.command=self.command.strip(' ')

    def printhelp(self):
        print('指令列表：')
        for i in self.commandtips:
            print(i,'   ',self.commandtips[i])
        print('\n')

    def commandlist(self):
        return list(self.commandtips.keys())

    def fuzzyfinder(self,user_input):
        collection=self.commandlist()
        suggestions = []
        pattern = '.*?'.join(user_input)
        regex = re.compile(pattern)
        for i in collection:
            match = regex.search(i)
            if match:
                suggestions.append((len(match.group()), match.start(), i))
        return [x for _, _, x in sorted(suggestions)]

    def commandhelp(self):
        try:
            if self.fuzzyfinder(self.command)!=[] and self.command!='':
                print('<-未知指令"{}"   你是否想输入以下指令？'.format(self.command))
                for i in self.fuzzyfinder(self.command):
                    print(i,'   ',self.commandtips[i])
            else:
                print('<-未知指令"{}"   请输入help/?查看帮助'.format(self.command))
        except:
            print('<-未知指令"{}"   请输入help/?查看帮助'.format(self.command))



def hello():
    file=open('config.clc','r',encoding='utf-8-sig')
    config=file.read()
    file.close()
    config=eval(config)
    config['reply']=0
    config['merge']=0
    config['learning']=0
    config['admin']=0
    file=open('config.clc','w',encoding='utf-8-sig')
    file.write(str(config))
    file.close()
    global version
    print('欢迎使用ChatLearning应用 版本号：',version)
    #print('遇到问题和bug请在mirai论坛回复我或发送至我的邮箱1121917292@qq.com')
    print('输入help来查看指令列表吧！')

def unknowcommand(command):
    print('<-未知指令"{}"   请输入help/?查看帮助'.format(command))
    pass

def remerge():
    file=open('config.clc','r',encoding='utf-8-sig')
    config=file.read()
    file.close()
    config=eval(config)
    config['merge']=1
    file=open('config.clc','w',encoding='utf-8-sig')
    file.write(str(config))
    file.close()
    merge=threading.Thread(target=ChatMerge.main)
    merge.start()

def globe(globesign=0,get=0):
    file=open('config.clc','r',encoding='utf-8-sig')
    config=file.read()
    config=eval(config)
    file.close()
    if get==1:
        return config['sendmode']
    if globesign==0:
        config['sendmode']=1
        globesign=1
        print('<-已开启全局模式')
    else:
        config['sendmode']=0
        globesign=0
        print('<-已关闭全局模式')
    file=open('config.clc','w',encoding='utf-8-sig')
    file.write(str(config))
    return globesign

def setadmin(adminnum):
    try:
        adminnum=int(adminnum)
    except:
        print('参数错误')
        return None
    file=open('config.clc','r',encoding='utf-8-sig')
    config=file.read()
    file.close()
    config=eval(config)
    config['Administrator']=adminnum
    file=open('config.clc','w',encoding='utf-8-sig')
    file.write(str(config))
    print('管理员QQ号已设置为',adminnum)

def admin(adminsign):
    if adminsign==0:
        print('<-进入管理模式')
        print('拥有词库的群号:')
        print(ChatAdmin.getfilelist())
        group=input('->请输入需要管理的群号:')
        try:
            group=int(group)
        except:
            print('参数错误')
            print('<-退出管理模式')
            return adminsign
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        config['admin']=1
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        ChatAdmin.main(config['Administrator'],group)
        #admin=threading.Thread(target=ChatAdmin.main,args=(config['Administrator'],group))
        #adminsign=1
        #admin.join()
        return adminsign
    else:
        adminsign=0
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        config['admin']=0
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-关闭管理模式')
        return adminsign


def grouplist():
    file=open('config.clc','r',encoding='utf-8-sig')
    config=file.read()
    config=eval(config)
    file.close()
    admin
    learninggrouplist=config['learninggrouplist']
    replygrouplist=config['replygrouplist']
    unmergegrouplist=config['unmergegrouplist']
    Administrator=config['Administrator']
    print('管理员QQ号：',Administrator)
    print('已开启记录的群：',learninggrouplist)
    print('已开启答复的群：',replygrouplist)
    print('不录入总词库的群：',unmergegrouplist)

def learninginterval(interval):
    try:
        interval=int(interval)
    except:
        print('参数错误')
        return None
    if interval<=0:
        print('参数错误')
        return None
    print('<-已设置词库链学习间隔时间',interval,'秒')
    file=open('config.clc','r',encoding='utf-8-sig')
    config=file.read()
    config=eval(config)
    file.close()
    config['interval']=interval
    file2=open('config.clc','w',encoding='utf-8-sig')
    file2.write(str(config))    

def replychance(chance):
    try:
        chance=int(chance)
    except:
        print('参数错误')
        return None
    if chance<=0 or chance>100:
        print('参数错误')
        return None
    print('<-已设置回复的触发概率',chance,'%')
    file=open('config.clc','r',encoding='utf-8-sig')
    config=file.read()
    config=eval(config)
    file.close()
    config['replychance']=chance
    file2=open('config.clc','w',encoding='utf-8-sig')
    file2.write(str(config))

def addgroup(args):
    if args[:9]=='learning ':
        grouplist='[{}]'.format(args[9:])
        try:
            grouplist=eval(grouplist)
            if type(grouplist)!=type([]):
                print('参数错误')
                return None
        except:
            print('参数错误')
            return None
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        config['learninggrouplist'].extend(grouplist)
        config['learninggrouplist']=list(set(config['learninggrouplist']))
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-添加完毕') 
        pass
    elif args[:6]=='reply ':
        grouplist='[{}]'.format(args[6:])
        try:
            grouplist=eval(grouplist)
            if type(grouplist)!=type([]):
                print('参数错误')
                return None
        except:
            print('参数错误')
            return None
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        config['replygrouplist'].extend(grouplist)
        config['replygrouplist']=list(set(config['replygrouplist']))
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()       
        print('<-添加完毕') 
        pass
    elif args[:8]=='unmerge ':
        grouplist='[{}]'.format(args[8:])
        try:
            grouplist=eval(grouplist)
            if type(grouplist)!=type([]):
                print('参数错误')
                return None
        except:
            print('参数错误')
            return None
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        config['unmergegrouplist'].extend(grouplist)
        config['unmergegrouplist']=list(set(config['unmergegrouplist']))
        config['merge']=0
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()       
        print('<-添加完毕') 
        return config['learning'] 
        pass
    else:
        print('参数错误')
        return None
    pass

def removegroup(args):
    if args[:9]=='learning ':
        grouplist='[{}]'.format(args[9:])
        try:
            grouplist=eval(grouplist)
            if type(grouplist)!=type([]):
                print('参数错误')
                return None
        except:
            print('参数错误')
            return None
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        for i in grouplist:
            try:
                config['learninggrouplist'].remove(i)
            except:
                print('群',i,'不存在')
                continue
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-移除完毕') 
        pass
    elif args[:6]=='reply ':
        grouplist='[{}]'.format(args[6:])
        try:
            grouplist=eval(grouplist)
            if type(grouplist)!=type([]):
                print('参数错误')
                return None
        except:
            print('参数错误')
            return None
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        for i in grouplist:
            try:
                config['replygrouplist'].remove(i)
            except:
                print('群',i,'不存在')
                continue
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()        
        print('<-移除完毕') 
        pass
    elif args[:8]=='unmerge ':
        grouplist='[{}]'.format(args[8:])
        try:
            grouplist=eval(grouplist)
            if type(grouplist)!=type([]):
                print('参数错误')
                return None
        except:
            print('参数错误')
            return None
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        for i in grouplist:
            try:
                config['unmergegrouplist'].remove(i)
            except:
                print('群',i,'不存在')
                continue
        config['merge']=0
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()        
        print('<-移除完毕')
        return config['learning'] 
        pass
    else:
        print('参数错误')
        return None
    pass

def learning(learningsign,mergesign):
    if learningsign==0 and mergesign==0:
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        config['learning']=1
        config['merge']=1
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-开始记录')
        learning=threading.Thread(target=ChatLearning.main)
        merge=threading.Thread(target=ChatMerge.main)
        learningsign=1
        mergesign=1
        learning.start()
        merge.start()
        return learningsign,mergesign
    else:
        learningsign=0
        mergesign=0
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        config['learning']=0
        config['merge']=0
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-停止记录')
        return learningsign,mergesign

def reply(replysign):
    if replysign==0:
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        config['reply']=1
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-开启回复功能')
        reply=threading.Thread(target=ChatReply.main)
        replysign=1
        reply.start()
        return replysign
    else:
        replysign=0
        file=open('config.clc','r',encoding='utf-8-sig')
        config=file.read()
        file.close()
        config=eval(config)
        config['reply']=0
        file=open('config.clc','w',encoding='utf-8-sig')
        file.write(str(config))
        file.close()
        print('<-关闭回复功能')
        return replysign


def merge(time):
    if time<=0:
        print('参数错误')
        return None
    print('<-已设置总词库更新时间',time,'秒')
    file=open('config.clc','r',encoding='utf-8-sig')
    config=file.read()
    config=eval(config)
    file.close()
    config['mergetime']=time
    file2=open('config.clc','w',encoding='utf-8-sig')
    file2.write(str(config))

def check():
    check=threading.Thread(target=ChatCheck.main)
    check.start()   
    check.join()


async def tui():
    session = PromptSession()
    globesign=globe(get=1)
    learningsign=0
    mergesign=0
    replysign=0
    adminsign=0
    while 1:
        #time.sleep(3)
        #print('->',end='')
        #command=input()
        #command=prompt('->')
        with patch_stdout():
            command=await session.prompt_async('\nChatLearning ->')
            command=command.lower()
            commandlist=commandclass(command)
        if command[:8]=='learning':
            if command=='learning':
                learningmodesign=learning(learningsign,mergesign)
                learningsign=learningmodesign[0]
                mergesign=learningmodesign[1]
            elif command[:9]=='learning ':
                learninginterval(command[9:])
            else:
                commandlist.commandhelp()
        elif command[:5]=='reply':
            if command=='reply':
                replysign=reply(replysign)
            elif command[:6]=='reply ':
                replychance(command[6:])
            else:
                commandlist.commandhelp()
        elif command[:6]=='merge ':
            try:
                time=int(command[6:])
                merge(time)
            except:
                commandlist.commandhelp()
                continue
        elif command=='check':
            check()
        elif command[:4]=='add ':
            if addgroup(command[4:])==1:
                print('正在重启merge')
                remerge()
                pass
        elif command[:7]=='remove ':
            if removegroup(command[7:])==1:
                print('正在重启merge')
                remerge()
                pass
        elif command=='grouplist':
            grouplist()
        elif command=='globe':
            globesign=globe(globesign=globesign)
        elif command[:9]=='setadmin ':
            setadmin(command[9:])
        elif command=='admin':
            if learningsign==1:
                tempsign=learning(learningsign,mergesign)
                learningsign=tempsign[0]
                mergesign=tempsign[1]
            if replysign==1:
                replysign=reply(replysign)
            adminsign=admin(adminsign)
        elif command=='help' or command=='?' or command=='？':
            commandlist.printhelp()
        else:
            commandlist.commandhelp()

hello()
loop=asyncio.get_event_loop()
loop.run_until_complete(tui())