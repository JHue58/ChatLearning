# Demo阶段
import simuse
import time
import os
import copy



def getconfig():
    file=open('config.txt','r',encoding='utf-8-sig')
    config=file.read()
    config=eval(config)
    interval=config['interval']
    interval=int(interval)
    return interval


def creatquestion(question,group):  # 记录问题      
    #print("old")
    tempquestion=copy.deepcopy(question)  #作为问题，不需要“url”标签，所以对消息链(list)进行深拷贝备用
    for i in question: # 去除作为问题中的变动因素“url”
        try:
            i.pop('url')
        except:
            continue
    question=str(question)  
    filename=str(group)+".cl"
    try: # 读取已缓存的词库
        file=open(filename,'r',encoding='utf-8-sig')
        tempdict=file.read()
        file.close()
        tempdict=eval(tempdict)
    except:
        tempdict={}
    if not(question in tempdict.keys()):  # 判断词库中问题是否存在，若不存在则记录问题
        questiondict={}
        questiontime=int(time.time())
        answerlist=[]
        questiondict["time"]=questiontime
        questiondict["answer"]=answerlist
        tempdict[question]=questiondict
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"\n问题已记录",filename)
    #print(tempdict)
    file=open(filename,'w',encoding='utf-8-sig')
    file.write(str(tempdict))
    file.close()
    return tempquestion  # 返回未去除“url”的消息链，为记录答案做准备

def creatanswer(question,answer,group): # 记录答案
    #print("new")
    #os.system("pause")
    for i in question: # 去除作为问题中的变动因素“url”
        try:
            i.pop('url')
        except:
            continue
    question=str(question)
    answer=str(answer)
    filename=str(group)+".cl"
    file=open(filename,'r',encoding='utf-8-sig') # 读取缓存的词库
    tempdict=file.read()
    file.close()
    tempdict=eval(tempdict)
    answertime=int(time.time())
    answerdict={"answertext":"","time":""}
    answerdict["answertext"]=answer
    answerdict["time"]=answertime
    questiondict=tempdict[question]  #找到问题，将答案添加进“answer”属性
    questiondict["answer"].append(answerdict.copy())
    tempdict[question]=questiondict
    file=open(filename,'w',encoding='utf-8-sig')
    file.write(str(tempdict))
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"\n答案已记录",filename)
    file.close()

def extractmessage(data,tempdict): # 将消息链转化为字典格式（key为群号，value为消息链）
    message=simuse.Fetch_Message(data) # 监听消息链
    if type(message)==type(0):
        return tempdict
    for i in message:
        if i['type']=='GroupMessage': # 判断监听到的消息是否为群消息
            if i['group'] in tempdict.keys():
                #tempdict[i['group']]=[]
                messagechain=i['messagechain']
                #messagechain.pop(0)
                tempdict[i['group']].append(messagechain)
            else:
                tempdict[i['group']]=[]
                messagechain=i['messagechain']
                #messagechain.pop(0)
                tempdict[i['group']].append(messagechain)
    return tempdict

def listening(data):
    global interval
    textdict={}
    sign={}  # 创建一个字典，用来标记第一个记录的问题，即标记“1”
    while 1:
        #print(sign)
        textdict={}
        textdict=extractmessage(data,textdict) # 不同群的消息链对应存储
        #print(textdict)
        #file=open('texttemp.cl','w',encoding='utf-8-sig')
        #file.write(str(textdict))
        #file.close()
        for i in textdict: # 遍历群号
            if not(i in sign.keys()): # 若有新的群号，将收集到的第一个消息标记“1”
                sign[i]={"id":"","signtime":0,"befor":""}
            for k in textdict[i]: # 开始记录问题
                messagesign=sign[i]
                messagechain=k
                messageinfo=messagechain[0]  # 获取消息链的信息属性（消息id和时间戳）
                messagechain.pop(0)
                if messageinfo['time']-messagesign["signtime"]>interval: # 若相同群，收集到的两个消息的间隔大于900秒，则新的消息重新标记“1”
                    #print(messageinfo['time'])
                    #os.system("pause")
                    messagesign["id"]=messageinfo['id']  # 将该消息重新标记“1”
                if messageinfo['id']==messagesign["id"]:  # 将标记“1”的消息，记录为问题              
                    creatquestion(messagechain,i) # 记录问题
                    messagesign["signtime"]=messageinfo['time']
                    messagesign["befor"]=messagechain # 将该消息标记为“上一个问题”
                else:  # 剩下的问题，记录为上一个问题的答案和新的问题
                    #print(messagechain)
                    messagechain=creatquestion(messagechain,i) # 记录问题
                    #print(messagechain)
                    creatanswer(messagesign["befor"],messagechain,i) # 记录答案
                    messagesign["signtime"]=messageinfo['time'] # 更新消息的时间戳
                    messagesign["befor"]=messagechain # 将该消息标记为“上一个问题”
                sign[i]=messagesign

        time.sleep(0.5)





def main():
    data=simuse.Get_data()
    data=simuse.Get_Session(data)
    listening(data)

interval=getconfig()
main()





#{
#    "question text":{"time":"","answer":[{"answer text":"","time":""},{"answer text":"","time":""}]}
#}

#词库的缓存格式