import os
import re
import tkinter
import time
from tkinter import filedialog


def getcl():
    filelist = os.listdir()
    cllist = []
    nodelist = []
    for i in filelist:
        if i[-3:] == '.cl':
            #print(i)
            cllist.append(i)
    #print(cllist)


def restore(path):
    try:
        file = open(path, 'r', encoding='utf-8-sig')
        data = file.readline()
        data = re.findall('(\d+)', data)
    except:
        print('转换失败\n首行标记不正确')
        return None
    questionnum = 0
    answernnum = 0
    #print(data)
    questiondict = {}
    linesign = 0
    with file:
        for line in file:
            linesign += 1
            try:
                line = line.strip('\n')
                #print(line)
                qindex = line.find('问')
                aindex = line.find('答')
                signindex = line.find('：')
                #print(qindex)
                if qindex != -1 and qindex < signindex:
                    questionsign = line[:qindex]
                    #print('1')
                    questionnum += 1
                    question = line[qindex + 2:line.rfind('|')]
                    questiondict[question] = {
                        'answer': [],
                        'time': int(line[line.rfind('|') + 1:])
                    }
                    #print(question)
                    #os.system('pause')
                    tempdict = questiondict[question]
                    answerlist = tempdict['answer']
                    #print(tempdict)
                    #os.system('pause')

                elif aindex != -1 and aindex < signindex:
                    answersion = line[:aindex]
                    if questionsign != answersion:
                        continue
                    answernnum += 1
                    answerdict = {'answertext': '', 'time': ''}
                    answerdict['answertext'] = line[line.find('：') +
                                                    1:line.rfind('|')]
                    answerdict['time'] = int(line[line.rfind('|') + 1:])
                    #print(answerdict)
                    answerlist.append(answerdict.copy())
                    #print(answerlist)
                    #os.system('pause')
                else:
                    continue
            except:
                print('转换失败\n第{}行格式不匹配'.format(linesign + 1))
                return None
    file.close()
    questionchange = questionnum - int(data[0])
    answerchange = answernnum - int(data[1])
    if questionchange == 0 and answerchange == 0:
        path = path[:-4] + '.cl'
    else:
        path = path[:-4] + '_change.cl'
    file = open(path, 'w', encoding='utf-8-sig')
    file.write(str(questiondict))
    file.close()
    if questionchange > 0:
        print('增加问题{}个'.format(questionchange))
    elif questionchange == 0:
        print('问题无变动')
    elif questionchange < 0:
        print('删除问题{}个'.format(abs(questionchange)))
    if answerchange > 0:
        print('增加答案{}个'.format(answerchange))
    elif answerchange == 0:
        print('答案无变动')
    elif answerchange < 0:
        print('删除答案{}个'.format(abs(answerchange)))


def changecl(path):
    file = open(path, 'r', encoding='utf-8-sig')
    tempdict = file.read()
    file.close()
    tempdict = eval(tempdict)
    lens = len(tempdict)
    questionlist = tempdict.keys()
    questiondictlist = tempdict.values()
    displaystr = ''
    questionnode = 0
    allanswernum = 0
    sign = 0
    percent = 0
    start = time.time()
    for (question, questiondict) in zip(questionlist, questiondictlist):
        #os.system('pause')
        #last_time=time.time()
        sign += 1
        answernode = 0
        answerlist = questiondict['answer']
        displaystr = displaystr + '{}问：'.format(questionnode) + str(
            question) + '|' + str(questiondict['time']) + '\n'
        for answerdict in answerlist:
            answer = answerdict['answertext']
            displaystr = displaystr + '{0}答{1}：'.format(
                questionnode, answernode) + str(answer) + '|' + str(
                    answerdict['time']) + '\n'
            answernode += 1
            allanswernum += 1
        questionnode += 1
        if percent < (sign / lens):
            if percent != 0:
                end = time.time()
                use_time = end - start
                all_time = use_time / percent
                res_time = all_time - use_time
                tips = "%.0f%%" % (percent * 100) + '    剩余时间{}秒'.format(
                    int(res_time)) + '      已用时间{}秒'.format(int(use_time))
                print(tips, '\r', end='')
            percent = percent + 0.01

    displaystr = '共有问：{0}个，答：{1}个\n'.format(questionnode,
                                            allanswernum) + displaystr
    #lens=len(tempdict)
    #print(lens)
    #tempdict= iter(tempdict.items())
    #dictstr=''
    #for i in range(lens):
    #    alinedict=dict(itertools.islice(tempdict,1))
    #    dictstr=dictstr+str(alinedict)+'\n'
    file = open(path[:-3] + '.txt', 'w', encoding='utf-8-sig')
    file.write(displaystr)
    file.close()


#cllist=getcl()
root = tkinter.Tk()
root.withdraw()
path = filedialog.askopenfilename(title='请选择cl文件或者txt文件',
                                  filetypes=[('ChatLearning缓存的词库', '*.cl'),
                                             ('所编辑好的词库', '*.txt')])
if path[path.rfind('.'):] == '.cl':
    print('请稍等，正在转换中')
    changecl(path)
    print('\n转换完成！')
    os.system('pause')
elif path[path.rfind('.'):] == '.txt':
    print('请稍等，正在转换中')
    restore(path)
    os.system('pause')
else:
    print('error')
    os.system('pause')
