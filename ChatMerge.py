import os
import pickle
import time




def getconfig():
    file = open('config.clc', 'r', encoding='utf-8-sig')
    config = file.read()
    file.close()
    config = eval(config)
    #print(config)
    try:
        return config['merge'], config['mergetime'], config[
            'unmergegrouplist'], config['tag']
    except:
        return config['merge'], config['mergetime'], config['unmergegrouplist']


def Merge(Mergedict, filename):
    version_error = 0
    repeatquestion_num = 0
    cldict = pickle.load(open('WordStock/' + filename, 'rb'))
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
            repeatquestion_num += 1
            #print('相同问题已合并')
    except:
        pass
    Mergedict.update(cldict)
    if repeatquestion_num != 0:
        print('已合并', filename, repeatquestion_num, '个相同问题')
    if version_error == 1:
        print('问题次数无法合并，请确认是否存在2.8.0版本以下的词库？ 错误词库：{}'.format(filename))
    return Mergedict


def getfile():
    tagdict = getconfig()[3]
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
        if i == 'Merge.cl':
            continue
        elif i[:-3] in Taglist:
            continue
        try:
            if i[:-3] in str(getconfig()[2]):
                continue
        except:
            pass
        if not (i[:-3] in tagdict.keys()):
            Mergedict = Merge(Mergedict, i)
    pickle.dump(Mergedict, open('WordStock/' + 'Merge.cl', 'wb'))
    for i in Taglist:
        print('Tag:{} 合并'.format(i))
        Mergedict_Tag = {}
        for k in cllist:
            if k[:-3] in str(tagdict.keys()):
                if i in tagdict[k[:-3]]:
                    Mergedict_Tag = Merge(Mergedict_Tag, k)
        pickle.dump(Mergedict_Tag, open('WordStock/' + '{}.cl'.format(i),
                                        'wb'))

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '词库合并完成')
    #print('->',end='')
    #os.system('pause')


def main():
    while 1:
        config = getconfig()
        if config[0] == 0:
            return None
        getfile()
        time.sleep(config[1])
