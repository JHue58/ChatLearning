import simuse
import time
import os
def creatquestion(question,group):
    #print("old")
    question=str(question)
    filename=str(group)+".cl"
    try:
        file=open(filename,'r',encoding='utf-8-sig')
        tempdict=file.read()
        file.close()
        tempdict=eval(tempdict)
    except:
        tempdict={}
    if not(question in tempdict.keys()):
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

def creatanswer(question,answer,group):
    #print("new")
    #os.system("pause")
    question=str(question)
    answer=str(answer)
    filename=str(group)+".cl"
    file=open(filename,'r',encoding='utf-8-sig')
    tempdict=file.read()
    file.close()
    tempdict=eval(tempdict)
    answertime=int(time.time())
    answerdict={"answertext":"","time":""}
    answerdict["answertext"]=answer
    answerdict["time"]=answertime
    questiondict=tempdict[question]
    questiondict["answer"].append(answerdict.copy())
    tempdict[question]=questiondict
    file=open(filename,'w',encoding='utf-8-sig')
    file.write(str(tempdict))
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"\n答案已记录",filename)
    file.close()

def extractmessage(data,tempdict):
    message=simuse.Fetch_Message(data)
    if type(message)==type(0):
        return tempdict
    for i in message:
        if i['type']=='GroupMessage':
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
    textdict={}
    sign={}
    while 1:
        #print(sign)
        textdict={}
        textdict=extractmessage(data,textdict)
        #print(textdict)
        file=open('texttemp.cl','w',encoding='utf-8-sig')
        file.write(str(textdict))
        file.close()
        for i in textdict:
            if not(i in sign.keys()):
                sign[i]={"id":"","signtime":0,"befor":""}
            for k in textdict[i]:
                messagesign=sign[i]
                messagechain=k
                messageinfo=messagechain[0]
                messagechain.pop(0)
                if messageinfo['time']-messagesign["signtime"]>1800:
                    #print(messageinfo['time'])
                    #os.system("pause")
                    messagesign["id"]=messageinfo['id']
                if messageinfo['id']==messagesign["id"]:                
                    creatquestion(messagechain,i)
                    messagesign["signtime"]=messageinfo['time']
                    messagesign["befor"]=messagechain
                else:
                    creatquestion(messagechain,i)
                    creatanswer(messagesign["befor"],messagechain,i)
                    messagesign["signtime"]=messageinfo['time']
                    messagesign["befor"]=messagechain
                sign[i]=messagesign

        time.sleep(0.5)





def main():
    data=simuse.Get_data()
    data=simuse.Get_Session(data)
    listening(data)

main()





#{
#    "question text":{"time":"","answer":[{"answer text":"","time":""},{"answer text":"","time":""}]}
#}