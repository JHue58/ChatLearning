# Demo阶段
import simuse
import random
import time

def getanswer(group,question): # 从词库中获取答案
    for i in question: # 去除作为问题中的变动因素“url”
        try:
            i.pop('url')
        except:
            continue    
    question=str(question)
    filename=str(group)+'.cl' # 读取已缓存的词库
    file=open(filename,'r',encoding='utf-8-sig')
    tempdict=file.read()
    tempdict=eval(tempdict)
    try: # 检索问题，若词库中无该问题，则函数返回-1，若有，则返回所有答案（答案列表）
        print(question)
        questiondict=tempdict[question]
        answerlist=questiondict['answer']
    except:
        return -1
    print(answerlist)
    return answerlist
    
        
def replyanswer(data,group,answer): # 发送答案
    try:
        answer=random.choice(answer) # 尝试从答案列表中随机抽取一个答案，若答案列表为空，则不回复
        answer=answer['answertext']
    except:
        print('无答案，不给予回复')
        return None
    print(answer)
    try:
        answer=eval(answer)
    except:
        pass
    for i in answer: # 去除答案中的imageId，不去除mirai api http会无法回复
        try:
            i.pop('imageId')
        except:
            continue
    number=simuse.Send_Message_Chain(data,group,1,answer) # 让bot发送随机抽取中的答案
    if number != None:
        print('答案已发送',number)

def listening(data):
    while 1 :
        message=simuse.Fetch_Message(data) # 监听消息链
        if type(message)==type(0):
            time.sleep(0.5)
            continue
        for i in message :
            if i['type']=='GroupMessage': # 判断监听到的消息是否为群消息
                group=i['group'] # 记录群号
                messagechain=i['messagechain'] 
                messagechain.pop(0)
                question=messagechain
                answer=getanswer(group,question) # 获取答案
                if answer != -1:
                    replyanswer(data,group,answer) # 让bot回复
        time.sleep(0.5)


def main():
    data=simuse.Get_data()
    data=simuse.Get_Session(data)
    listening(data)

main()



