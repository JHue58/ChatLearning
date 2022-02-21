import os

def clcheck(filename):
    question_num=0
    answer_num=0
    allanswerlist=[]
    file=open(filename,'r',encoding='utf-8-sig')
    cldict=file.read()
    file.close()
    cldict=eval(cldict)
    for i in cldict:
        question_num+=1
        questioninfo=cldict[i]
        answerlist=questioninfo['answer']
        allanswerlist.extend(answerlist)
    try:
        for i in allanswerlist:
            answer_num+=1
    except:
        pass
    group=filename[:-3]
    print('群',group,'收集到问题',question_num,'个',' 答案',answer_num,'个')


def main():
    filelist=os.listdir()
    cllist=[]
    for i in filelist:
        if i[-3:]=='.cl':
            #print(i)
            cllist.append(i)
    #print(cllist)
    for i in cllist:
        clcheck(i)
    #os.system('pause')
