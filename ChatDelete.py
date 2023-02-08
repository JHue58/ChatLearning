import copy
import os
import pickle
import time

import ChatFilter
import ChatMerge
import simuse
from ChatClass import json_dump, json_load, pickle_dump, pickle_load


def Delete(data, sender):
    simuse.Send_Message(data, sender, 2, '清理中……', 1)
    tagdict = ChatMerge.getconfig()[3]
    Taglist = []
    for i in tagdict.values():
        Taglist.extend(i)
    Taglist = list(set(Taglist))
    filelist = os.listdir('WordStock')
    cllist = []
    for i in filelist:
        if i[-3:] == '.cl':
            #print(i)
            cllist.append(i)
    #print(cllist)
    Mergedict = {}
    for i in cllist:
        if Mergedict == None:
            print('清理失败')
            simuse.Send_Message(data, sender, 2, '清理失败,存在不同版本的词库', 1)
            time.sleep(0.8)
            return None
        if i == 'Merge.cl':
            continue
        elif i[:-3] in Taglist:
            continue
        Mergedict = Merge(Mergedict, i)

    deltipdict = {}

    for i in cllist:
        delnumlist = []
        if i == 'Merge.cl':
            continue
        elif i[:-3] in Taglist:
            continue
        delnumlist.append(Delete_freq(Mergedict, i))
        delnumlist.append(Delete_Filter(i))
        deltipdict[i] = delnumlist
    tips = ''
    for i in deltipdict:
        tiplist = deltipdict[i]
        if tiplist[0] != 0 and tiplist[1] != 0:
            tips = tips + '已清理{}低频条目{}个，过滤条目{}个\n'.format(
                i, tiplist[0], tiplist[1])
        elif tiplist[0] != 0 and tiplist[1] == 0:
            tips = tips + '已清理{}低频条目{}个\n'.format(i, tiplist[0])
        elif tiplist[0] == 0 and tiplist[1] != 0:
            tips = tips + '已清理{}过滤条目{}个\n'.format(i, tiplist[1])
    if tips != '':
        print(tips)
        simuse.Send_Message(data, sender, 2, tips, 1)
    else:
        print('无需清理')
        simuse.Send_Message(data, sender, 2, '无需清理', 1)
    time.sleep(0.8)


def Merge(Mergedict, filename):
    version_error = 0
    cldict = pickle_load('WordStock/' + filename)
    #print(Mergedict)
    try:
        repeatquestion = Mergedict.keys() & cldict.keys()
        for i in repeatquestion:
            tempquestiondict = cldict[i]
            newquestiondict = Mergedict[i]
            try:
                newquestiondict['freq'] += tempquestiondict['freq']
            except:
                version_error = 1
            #print(newanswer)
            newanswer = newquestiondict['answer']
            tempanswer = tempquestiondict['answer']
            newanswer.extend(tempanswer)
            del cldict[i]
            #print('相同问题已合并')
    except:
        pass
    Mergedict.update(cldict)
    if version_error == 1:
        print('问题次数无法合并，请确认是否存在2.8.0版本以下的词库？ 错误词库：{}'.format(filename))
        return None
    return Mergedict


def Delete_freq(Mergedict, filename):
    cldict = pickle_load('WordStock/' + filename)
    freqdel_num = 0
    for question in Mergedict:
        questiondict = Mergedict[question]
        if questiondict['freq'] < 2:
            try:
                cldict.pop(question)
                freqdel_num += 1
            except:
                continue
    pickle_dump(cldict, 'WordStock/' + filename)
    return freqdel_num


def Delete_Filter(filename):
    cldict = pickle_load('WordStock/' + filename)
    question_list = list(cldict.keys())
    filterdel_num = 0
    for question in question_list:
        if ChatFilter.filtercheck(eval(question), display=False) == 0:
            cldict.pop(question)
            filterdel_num += 1
    for question in cldict:
        questiondict = cldict[question]
        answerlist_origin = questiondict['answer']
        answerlist = copy.deepcopy(questiondict['answer'])
        for answerdict in answerlist:
            answertext = answerdict['answertext']
            if ChatFilter.filtercheck(eval(answertext), display=False) == 0:
                answerlist_origin.remove(answerdict)
                filterdel_num += 1
    pickle_dump(cldict, 'WordStock/' + filename)
    return filterdel_num
