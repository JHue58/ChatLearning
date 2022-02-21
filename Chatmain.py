import threading
import ChatLearning
import ChatReply
import ChatMerge
import ChatCheck
import time

def unknowcommand(command):
    print('未知指令',command)
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
        print('开始记录')
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
        print('停止记录')
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
        print('开启回答功能')
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
        print('关闭回答功能')
        return replysign


def merge(time):
    print('已设置总词库更新时间',time,'秒')
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




learningsign=0
mergesign=0
replysign=0
while 1:
    #time.sleep(3)
    print('->',end='')
    command=input()
    if command=='learning':
        learningmodesign=learning(learningsign,mergesign)
        learningsign=learningmodesign[0]
        mergesign=learningmodesign[1]
    elif command=='reply':
        replysign=reply(replysign)
    elif command[:6]=='merge ':
        try:
            time=int(command[6:])
        except:
            unknowcommand(command)
            continue
        merge(time)
    elif command=='check':
        check()
    else:
        unknowcommand(command)