import os
import time

def Merge(Mergedict,filename):
    repeatquestion_num=0
    file=open(filename,'r',encoding='utf-8-sig')
    cldict=file.read()
    file.close()
    cldict=eval(cldict)
    #print(Mergedict)
    try:
        repeatquestion=Mergedict.keys()&cldict.keys()
        for i in repeatquestion:
            tempanswer=cldict[i]
            newanswer=Mergedict[i]
            #print(newanswer)
            newanswer=newanswer['answer']
            tempanswer=tempanswer['answer']
            newanswer.extend(tempanswer)
            del cldict[i]
            repeatquestion_num+=1
            #print('相同问题已合并')
    except:
        pass
    Mergedict.update(cldict)
    if repeatquestion_num!=0:
        print('已合并',filename,repeatquestion_num,'个相同问题')
    return Mergedict


def main():
    filelist=os.listdir()
    cllist=[]
    for i in filelist:
        if i[-3:]=='.cl':
            print(i)
            cllist.append(i)
    print(cllist)
    Mergedict={}
    for i in cllist:
        if i=='Merge.cl':
            continue
        Mergedict=Merge(Mergedict,i)
    file=open('Merge.cl','w',encoding='utf-8-sig')
    file.write(str(Mergedict))
    file.close()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'词库合并完成')
    #os.system('pause')

while 1:
    main()
    time.sleep(3600)