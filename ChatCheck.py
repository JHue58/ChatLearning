import os
import time

import simuse


def clcheck(filename, data, fromchat):
    question_num = 0
    answer_num = 0
    allanswerlist = []
    file = open(filename, 'r', encoding='utf-8-sig')
    cldict = file.read()
    file.close()
    cldict = eval(cldict)
    for i in cldict:
        question_num += 1
        questioninfo = cldict[i]
        answerlist = questioninfo['answer']
        allanswerlist.extend(answerlist)
    try:
        for i in allanswerlist:
            answer_num += 1
    except:
        pass
    group = filename[:-3]
    print('群', group, '收集到问题', question_num, '个', ' 答案', answer_num, '个')
    if fromchat != 0:
        nodedict = {
            'senderId': data['qq'],
            'time': int(time.time()),
            'senderName': 'ChatLearning',
            'messageChain': [{
                'type': 'Plain',
                'text': ''
            }]
        }
        messagechain = nodedict['messageChain']
        messagedict = messagechain[0]
        messagedict['text'] = '群' + str(group) + '收集到问题' + str(
            question_num) + '个' + ' 答案' + str(answer_num) + '个'
        return nodedict
        #simuse.Send_Message(data, fromchat, 2, '群'+str(group)+'收集到问题'+str(question_num)+'个'+' 答案'+str(answer_num)+'个', 1)
        #time.sleep(1)


def main(data, fromchat):
    filelist = os.listdir()
    cllist = []
    nodelist = []
    for i in filelist:
        if i[-3:] == '.cl':
            #print(i)
            cllist.append(i)
    #print(cllist)
    for i in cllist:
        try:
            nodedict = clcheck(i, data, fromchat)
            nodelist.append(nodedict.copy())
        except:
            pass
    if fromchat != 0:
        sendmessagechain = [{'type': 'Forward', 'nodeList': ''}]
        sendmessagedict = sendmessagechain[0]
        sendmessagedict['nodeList'] = nodelist
        simuse.Send_Message_Chain(data, fromchat, 2, sendmessagechain)

    #os.system('pause')
