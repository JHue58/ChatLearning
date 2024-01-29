import copy
import hashlib
import os
import pickle
import time
from datetime import datetime
import xlwt
from qcloud_cos import CosConfig, CosS3Client

import ChatAdmin
import ChatMerge
import simuse
from ChatClass import Version, json_dump, json_load, pickle_dump, pickle_load


def getcllist():
    tagdict = ChatMerge.getconfig()[3]
    filelist = os.listdir('WordStock')
    cllist = []
    Taglist = []
    for i in tagdict.values():
        Taglist.extend(i)
    Taglist = list(set(Taglist))
    for i in filelist:
        if i[-3:] == '.cl' and i != 'Merge.cl' and not (i[:-3] in Taglist):
            #print(i)
            cllist.append(i)
    return cllist


#生成工作表
def createxcel(groupcldict):
    lines_dict = {}
    filename = hashlib.md5(str(groupcldict).encode("utf-8")).hexdigest()
    book = xlwt.Workbook(encoding='utf-8-sig', style_compression=0)
    sheet = book.add_sheet('符合结果的词库', cell_overwrite_ok=True)
    sheet_version = book.add_sheet(Version(), cell_overwrite_ok=True)
    sheet.set_panes_frozen('1')
    sheet.set_horz_split_pos(1)
    sheet.set_vert_split_pos(1)

    #创建列宽样式
    line_text = sheet.col(0)
    question_text = sheet.col(2)
    answer_text = sheet.col(4)
    group_text = sheet.col(5)
    answer_time_text = sheet.col(6)
    question_time_text = sheet.col(7)
    line_text.width = 20 * 80
    question_text.width = 20 * 256
    answer_text.width = 20 * 512
    answer_time_text.width = 20 * 312
    question_time_text.width = 20 * 312
    group_text.width = 20 * 165

    #创建样式，字体样式
    style = xlwt.XFStyle()
    style_2 = xlwt.XFStyle()
    style_text = xlwt.XFStyle()
    style_text_2 = xlwt.XFStyle()
    #创建单元格背景样式
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 41
    font = xlwt.Font()
    font.name = '黑体'
    font.height = 20 * 11
    #创建单元格格式
    alignment = xlwt.Alignment()
    alignment_text = xlwt.Alignment()
    alignment.horz = 0x02
    alignment.vert = 0x01
    alignment_text.horz = 0x01
    alignment_text.vert = 0x00
    #创建单元格样式
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style.borders = borders
    style_2.borders = borders
    style_text.borders = borders
    style_text_2.borders = borders
    style.alignment = alignment
    style_2.alignment = alignment
    style_text_2.alignment = alignment_text
    style_text.alignment = alignment_text
    style.font = font
    style_2.font = font
    style_text.font = font
    style_text_2.font = font
    style_2.pattern = pattern
    style_text_2.pattern = pattern
    sheet.write(0, 0, '行号', style=style)
    sheet.write(0, 1, '问题类型', style=style)
    sheet.write(0, 2, '详情', style=style)
    #sheet.write(0, 3, '答案id', style=style)
    sheet.write(0, 3, '答案类型', style=style)
    sheet.write(0, 4, '详情', style=style)
    sheet.write(0, 5, '群', style=style)
    sheet.write(0, 6, '答案记录时间', style=style)
    sheet.write(0, 7, '问题记录时间', style=style)

    sheet_line = 1
    linecolorsign = 1

    for groupnum in list(groupcldict.keys()):
        cldict = groupcldict[groupnum]
        questionlist = list(cldict.keys())
        #print(questionlist)
        #os.system('pause')
        for question in questionlist:
            linecolorsign += 1
            if (linecolorsign % 2) == 0:
                setstyle = style
                setstyle_text = style_text
            else:
                setstyle = style_2
                setstyle_text = style_text_2
            questiondict = cldict[question]
            question_id = questiondict['node']
            question = eval(question)
            question_type = '未知'
            question_time = questiondict['time']
            timeArray_question = time.localtime(question_time)
            question_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                          timeArray_question)
            question_info = ''
            question_plainsign = 0
            question_imagesign = 0
            for question_messagechain in question:
                if question_messagechain['type'] == 'Plain':
                    question_plainsign = 1
                    question_info = question_info + question_messagechain[
                        'text']
                elif question_messagechain['type'] == 'Image':
                    question_imagesign = 1
                    question_info = question_info + question_messagechain[
                        'imageId']  ######
            if question_plainsign == 1 and question_imagesign == 0:
                question_type = '文字'
            elif question_plainsign == 0 and question_imagesign == 1:
                question_type = '图片'
            elif question_plainsign == 1 and question_imagesign == 1:
                question_type = '文字+图片'

            answerlist = questiondict['answer']
            for answerdict in answerlist:
                answer_plainsign = 0
                answer_imagesign = 0
                answer_id = answerdict['node']
                answer_type = '未知'
                answer_time = answerdict['time']
                # print("answer_time", answer_time)
                # timeArray_answer = time.localtime(answer_time)
                # answer_time = time.strftime("%Y-%m-%d %H:%M:%S",
                #                             timeArray_answer)
                answer_time = answer_time.strftime("%Y-%m-%d %H:%M:%S")
                answer_info = ''
                for answer_messagechain in eval(answerdict['answertext']):
                    if answer_messagechain['type'] == 'Plain':
                        answer_plainsign = 1
                        answer_info = answer_info + answer_messagechain['text']
                    elif answer_messagechain['type'] == 'Image':
                        answer_imagesign = 1
                        url = answer_messagechain['url']
                        answer_info = answer_info + answer_messagechain[
                            'url']  ######
                if answer_plainsign == 1 and answer_imagesign == 0:
                    answer_type = '文字'
                elif answer_plainsign == 0 and answer_imagesign == 1:
                    answer_type = '图片'
                elif answer_plainsign == 1 and answer_imagesign == 1:
                    answer_type = '文字+图片'
                try:
                    sheet.write(sheet_line, 0, sheet_line + 1, style=setstyle)
                    sheet.write(sheet_line, 1, question_type, style=setstyle)
                    sheet.write(sheet_line,
                                2,
                                question_info,
                                style=setstyle_text)
                    #sheet.write(sheet_line, 3, answer_id, style=style)
                    sheet.write(sheet_line, 3, answer_type, style=setstyle)
                    if answer_imagesign == 1:
                        text = answer_info
                        link = f'HYPERLINK("{url}";"{text}")'
                        sheet.write(sheet_line,
                                    4,
                                    xlwt.Formula(link),
                                    style=setstyle_text)
                    else:
                        sheet.write(sheet_line,
                                    4,
                                    answer_info,
                                    style=setstyle_text)
                    sheet.write(sheet_line, 5, groupnum, style=setstyle)
                    sheet.write(sheet_line, 6, answer_time, style=setstyle)
                    sheet.write(sheet_line, 7, question_time, style=setstyle)
                except:
                    pass
                lines_dict[sheet_line + 1] = {
                    'questionnode': question_id,
                    'answernode': answer_id,
                    'group': groupnum
                }
                sheet_line += 1
            #sheet.write_merge(question_line,sheet_line,0,0,question_id)
            #sheet.write_merge(question_line,sheet_line,1,1,question_type)
            #sheet.write_merge(question_line,sheet_line,2,2,question_info)
        #sheet.write_merge(group_line,sheet_line,8,8,groupnum,style=style_merge)
    book.save(filename + '.xls')
    #print(lines_dict)
    return filename, lines_dict


#上传工作表至cos
def uploadcos(data, filename):
    secret_id = 'XX'
    secret_key = 'XX'
    region = 'ap-shanghai'
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)
    Bucket_name = 'chatlearning-clxls-1302376822'
    response_upload = client.upload_file(Bucket=Bucket_name,
                                         LocalFilePath=filename + '.xls',
                                         Key=data['qq'] + '-' + filename +
                                         '.xls',
                                         ACL='public-read',
                                         EnableMD5=False)
    #print(response_upload)
    downloadcosurl = 'https://' + Bucket_name + '.cos.' + region + '.myqcloud.com/' + data[
        'qq'] + '-' + filename + '.xls'
    cosurl = downloadcosurl + '?ci-process=doc-preview&dstType=html'
    nodelist = []
    nodedict = {
        'senderId': data['qq'],
        'time': int(time.time()),
        'senderName': 'ChatLearning',
        'messageChain': []
    }
    tipmessageChain = [{
        'type':
        'Plain',
        'text':
        '请输入需要删除的行数(取消输入-1)\n多个用空格隔开\n若要删除xx行至xx行\n请输入"xx xx"(不要忘记双引号)'
    }]
    nodedict['messageChain'] = tipmessageChain
    nodelist.append(nodedict.copy())
    cosurlmessageChain = [{'type': 'Plain', 'text': '在线浏览：\n' + cosurl}]
    nodedict['messageChain'] = cosurlmessageChain
    nodelist.append(nodedict.copy())
    downloadcosurlmessageChain = [{
        'type': 'Plain',
        'text': '下载地址(浏览器打开)：\n' + downloadcosurl
    }]
    nodedict['messageChain'] = downloadcosurlmessageChain
    nodelist.append(nodedict.copy())
    os.remove(filename + '.xls')
    return nodelist


#删除词库
def delcl(data, sender, lines_dict, nodelist, target_type=0, group=0):
    if group != 0:
        target = group
    else:
        target = sender
    tipsmessagechain = [{'type': 'Forward', 'nodeList': nodelist}]
    simuse.Send_Message_Chain(data, target, target_type, tipsmessagechain)
    while 1:
        errorlines = 0
        seerrorlines = 0
        command = ChatAdmin.get_admin_command(data, sender=sender, group=group)
        if command != None:
            if command == str(-1) or command == '–1':
                print('取消删除')
                simuse.Send_Message(data, target, target_type, '取消删除', 1)
                return None
            try:
                command = command.replace('，', ',')
                command = command.replace(' ', ',')
                command = command.replace('–', '-')
            except:
                pass
            try:

                lines_list = '[{}]'.format(command)
                lines_list = eval(lines_list)
            except:
                print('参数错误，请重新输入')
                simuse.Send_Message(data, target, target_type, '参数错误，请重新输入', 1)
                continue
            if type(lines_list) != type([]):
                print('参数错误，请重新输入')
                simuse.Send_Message(data, target, target_type, '参数错误，请重新输入', 1)
                continue
            for i in lines_list:
                oncelines_list = [i]
                lines_list[lines_list.index(i)] = oncelines_list
            for i in lines_list:
                for k in i:
                    try:
                        if int(k) <= 1:
                            errorlines = 1
                    except:
                        pass
                    tempk = str(k)
                    if tempk.find(',') != -1:
                        startline = int(tempk[:tempk.find(',')])
                        endline = int(tempk[tempk.find(',') + 1:])
                        if startline <= 1 or endline <= 1:
                            errorlines = 1
                        if endline - startline >= 0:
                            templist = []
                            while 1:
                                templist.append(startline)
                                if startline == endline:
                                    break
                                startline += 1
                            lines_list[lines_list.index(i)] = templist
                        else:
                            seerrorlines = 1
                    else:
                        continue
            if errorlines == 0 and seerrorlines == 0:
                break
            elif errorlines != 0:
                print('行数错误，请重新输入\n最小行数为2')
                simuse.Send_Message(data, target, target_type,
                                    '行数错误，请重新输入\n最小行数为2', 1)
            elif errorlines == 0 and seerrorlines != 0:
                print('行数错误，请重新输入\n结束行应大于起始行')
                simuse.Send_Message(data, target, target_type,
                                    '行数错误，请重新输入\n结束行应大于起始行', 1)

        else:
            continue
    nofoundlines = []
    #changedict{'group':[{'questionnode':'','answernode':''}]}
    changedict = {}
    for onelines_list in lines_list:
        for lines in onelines_list:
            tempdict = {'questionnode': '', 'answernode': ''}
            try:
                qadict = lines_dict[lines]
            except:
                nofoundlines.append(lines)
                continue
            tempdict['questionnode'] = qadict['questionnode']
            tempdict['answernode'] = qadict['answernode']
            groupnum = qadict['group']
            try:
                changedict[groupnum].append(tempdict.copy())
            except:
                changedict[groupnum] = [tempdict]

    delsign = 0
    for group in changedict:
        cldict_orign = pickle_load(
            'WordStock/' + str(group) + '.cl')
        cldict = copy.deepcopy(cldict_orign)
        questionlist = list(cldict_orign.keys())
        changelist = changedict[group]
        for nodedict in changelist:
            question = questionlist[nodedict['questionnode']]
            questiondict = cldict[question]
            questiondict_orign = cldict_orign[question]
            answerlist = questiondict['answer']
            if answerlist == []:
                cldict.pop(question)
                delsign += 1
                continue
            answerlist_orign = questiondict_orign['answer']
            answerlist.remove(answerlist_orign[nodedict['answernode']])
            delsign += 1
            ##定位根据原定位，数据改动通过新
            if answerlist == []:
                cldict.pop(question)
        cldict_orign = cldict
        pickle_dump(cldict_orign, 'WordStock/' + str(group) + '.cl')
    if changedict != {} and nofoundlines == []:
        print('删除{}个条目成功'.format(delsign))
        simuse.Send_Message(data, target, target_type,
                            '删除{}个条目成功'.format(delsign), 1)
    elif nofoundlines != []:
        tips = ''
        for i in nofoundlines:
            tips = tips + str(i)
        print('删除{}个条目成功\n未找到行{}'.format(delsign, tips))
        simuse.Send_Message(data, target, target_type,
                            '删除{}个条目成功\n未找到行{}'.format(delsign, tips), 1)
    else:
        print('删除失败')
        simuse.Send_Message(data, target, target_type, '删除失败'.format(delsign),
                            1)


#查找问题
def findallquestion(data,
                    sender,
                    cllist,
                    question,
                    allquestion=0,
                    group=0,
                    target_type=0):
    if group != 0:
        target = group
    else:
        target = sender
    simuse.Send_Message(data, target, target_type, '查找中……', 1)
    #findquestion={'群号':'问题字典'}
    findquestion = {}
    for i in question:
        try:
            i.pop('url')
        except:
            pass
    for i in cllist:
        findquestiondict = {}
        findquestion[i[:-3]] = findquestiondict
        try:
            cldict = pickle.load(open('WordStock/' + i, 'rb'))
            questionlist = list(cldict.keys())
        except:
            print('该群无词库')
            simuse.Send_Message(data, target, target_type, '该群无词库', 1)
            return None
        for k in question:
            for j in questionlist:
                if k['type'] == 'Plain':
                    if str(j).find(k['text']) != -1 and allquestion == 0:
                        #print(1)
                        questiondict = cldict[j]
                        questiondict['node'] = questionlist.index(j)
                        answerlist = questiondict['answer']
                        if answerlist == []:
                            answerlist = [{
                                'answertext':
                                "[{'type':'Plain','text':'该问题无答案'}]",
                                'time': 100
                            }]
                        for answerdict in answerlist:
                            answerdict['node'] = answerlist.index(answerdict)
                        questiondict['answer'] = answerlist
                        cldict[j] = questiondict
                        findquestiondict[j] = cldict[j]
                    elif allquestion != 0:
                        questiondict = cldict[j]
                        questiondict['node'] = questionlist.index(j)
                        answerlist = questiondict['answer']
                        if answerlist == []:
                            answerlist = [{
                                'answertext':
                                "[{'type':'Plain','text':'该问题无答案'}]",
                                'time': 100
                            }]
                        for answerdict in answerlist:
                            answerdict['node'] = answerlist.index(answerdict)
                        questiondict['answer'] = answerlist
                        cldict[j] = questiondict
                        findquestiondict[j] = cldict[j]
                elif k['type'] == 'Image':
                    if str(j).find(k['imageId']) != -1 and allquestion == 0:
                        #print(2)
                        questiondict = cldict[j]
                        questiondict['node'] = questionlist.index(j)
                        answerlist = questiondict['answer']
                        if answerlist == []:
                            answerlist = [{
                                'answertext':
                                "[{'type':'Plain','text':'该问题无答案'}]",
                                'time': 100
                            }]
                        for answerdict in answerlist:
                            answerdict['node'] = answerlist.index(answerdict)
                        questiondict['answer'] = answerlist
                        cldict[j] = questiondict
                        findquestiondict[j] = cldict[j]
                    elif allquestion != 0:
                        questiondict = cldict[j]
                        questiondict['node'] = questionlist.index(j)
                        answerlist = questiondict['answer']
                        if answerlist == []:
                            answerlist = [{
                                'answertext':
                                "[{'type':'Plain','text':'该问题无答案'}]",
                                'time': 100
                            }]
                        for answerdict in answerlist:
                            answerdict['node'] = answerlist.index(answerdict)
                        questiondict['answer'] = answerlist
                        cldict[j] = questiondict
                        findquestiondict[j] = cldict[j]
    #print(findquestion)
    questionnum = 0
    groupquestionnum = {}
    #os.system('pause')
    for i in findquestion.keys():
        groupquestionnum[i] = len(findquestion[i])
        questionnum = questionnum + len(findquestion[i])
    tips = '共找到{}个符合的问题\n'.format(questionnum)
    for i in groupquestionnum:
        if groupquestionnum[i] != 0:
            tips = tips + '群{} 找到{}个\n'.format(i, groupquestionnum[i])
    if allquestion != 0:
        tips = '共找到{}个问题\n'.format(questionnum)
    print(tips)
    simuse.Send_Message(data, target, target_type, tips, 1)
    if questionnum == 0:
        return 3
    filename_lines_dict = createxcel(findquestion)
    filename = filename_lines_dict[0]
    lines_dict = filename_lines_dict[1]
    if allquestion == 1:
        try:
            nodelist = uploadcos(data, filename)
        except:
            print('网络连接出错')
            simuse.Send_Message(data, target, target_type, '网络连接出错', 1)
            os.remove(filename + '.xls')
            return None
        time.sleep(1)
        delcl(data,
              sender,
              lines_dict,
              nodelist,
              target_type=target_type,
              group=group)
        return None
    time.sleep(1)
    simuse.Send_Message(data, target, target_type,
                        '请输入你的选择\n1.查看查找结果\n2.继续查找\n3.返回', 1)
    while 1:
        command = ChatAdmin.get_admin_command(data, sender=sender, group=group)
        if command == str(1):
            try:
                nodelist = uploadcos(data, filename)
            except:
                print('网络连接出错')
                simuse.Send_Message(data, target, target_type, '网络连接出错', 1)
                os.remove(filename + '.xls')
                break
            time.sleep(1)
            delcl(data,
                  sender,
                  lines_dict,
                  nodelist,
                  target_type=target_type,
                  group=group)
            break
        elif command == str(2):
            os.remove(filename + '.xls')
            return 2
        elif command == str(3):
            os.remove(filename + '.xls')
            return 3
        else:
            continue


#查找答案
def findallanswer(data, sender, cllist, answer, group=0, target_type=0):
    if group != 0:
        target = group
    else:
        target = sender
    simuse.Send_Message(data, target, target_type, '查找中……', 1)
    findquestion = {}
    for i in answer:
        try:
            i.pop('url')
        except:
            pass
    for i in cllist:
        findquestiondict = {}
        findquestion[i[:-3]] = findquestiondict
        cldict = pickle_load('WordStock/' + i)
        for l in answer:
            for k in cldict:
                questiondict = cldict[k]
                answerlist = questiondict['answer']
                questiondict['node'] = list(cldict.keys()).index(k)
                tempanswerlist = []
                findsign = 0
                for j in answerlist:
                    answermessagechain = j['answertext']
                    j['node'] = answerlist.index(j)
                    if l['type'] == 'Plain':
                        if str(answermessagechain).find(l['text']) != -1:
                            findsign = 1
                            tempanswerlist.append(j.copy())
                    if l['type'] == 'Image':
                        if str(answermessagechain).find(l['imageId']) != -1:
                            findsign = 1
                            tempanswerlist.append(j.copy())
                if findsign != 0:
                    questiondict['answer'] = tempanswerlist
                    findquestiondict[k] = questiondict
    #print(findquestion)
    answernum = 0
    groupanswernum = {}
    #os.system('pause')
    for i in findquestion:
        groupanswernum[i] = 0
        cldict_check = findquestion[i]
        for k in cldict_check:
            questiondict_check = cldict_check[k]
            answerlist_check = questiondict_check['answer']
            answernum = answernum + len(answerlist_check)
            groupanswernum[i] = groupanswernum[i] + len(answerlist_check)
    tips = '共找到{}个符合的答案\n'.format(answernum)
    #print(groupanswernum)
    for i in groupanswernum:
        if groupanswernum[i] != 0:
            tips = tips + '群{} 找到{}个\n'.format(i, groupanswernum[i])
    print(tips)
    simuse.Send_Message(data, target, target_type, tips, 1)
    if answernum == 0:
        return 3
    filename_lines_dict = createxcel(findquestion)
    filename = filename_lines_dict[0]
    lines_dict = filename_lines_dict[1]
    time.sleep(1)
    simuse.Send_Message(data, target, target_type,
                        '请输入你的选择\n1.查看查找结果\n2.继续查找\n3.返回', 1)
    while 1:
        command = ChatAdmin.get_admin_command(data, sender=sender, group=group)
        if command == str(1):
            try:
                nodelist = uploadcos(data, filename)
            except:
                print('网络连接出错')
                simuse.Send_Message(data, target, target_type, '网络连接出错', 1)
                os.remove(filename + '.xls')
                break
            time.sleep(1)
            delcl(data,
                  sender,
                  lines_dict,
                  nodelist,
                  target_type=target_type,
                  group=group)
            break
        elif command == str(2):
            os.remove(filename + '.xls')
            return 2
        elif command == str(3):
            os.remove(filename + '.xls')
            return 3
        else:
            continue


def findallcontrol(data, sender, group=0):
    if group == 0:
        cllist = getcllist()
        target = sender
        target_type = 2
    else:
        cllist = [str(group) + '.cl']
        target = group
        target_type = 1
    while 1:
        time.sleep(1)
        if group == 0:
            tips = '请选择你的操作\n0.返回\n1.查找问题\n2.查找答案\n3.查看某个群的所有词库'
        else:
            tips = '进入管理模式\n请选择你的操作\n1.查找问题\n2.查找答案\n3.查看所有词库\n4.返回'
        simuse.Send_Message(data, target, target_type, tips, 1)
        while 1:
            command = ChatAdmin.get_admin_command(data,
                                                  sender=sender,
                                                  group=group)
            if command != None:
                break
        if command == str(1):
            simuse.Send_Message(data, target, target_type, '请发送关键字', 1)
            while 1:
                time.sleep(0.5)
                question = ChatAdmin.get_admin_question(data,
                                                        sender=sender,
                                                        group=group)
                if question != None:
                    if findallquestion(data,
                                       sender,
                                       cllist,
                                       question,
                                       group=group,
                                       target_type=target_type) == 2:
                        simuse.Send_Message(data, target, target_type,
                                            '请发送关键字', 1)
                        continue
                    else:
                        break
        elif command == str(2):
            simuse.Send_Message(data, target, target_type, '请发送关键字', 1)
            while 1:
                time.sleep(0.5)
                question = ChatAdmin.get_admin_question(data,
                                                        sender=sender,
                                                        group=group)
                if question != None:
                    if findallanswer(data, sender, cllist, question, group,
                                     target_type) == 2:
                        simuse.Send_Message(data, target, target_type,
                                            '请发送关键字', 1)
                        continue
                    else:
                        break

        elif command == str(3) and group == 0:
            grouplist = []
            for i in cllist:
                grouplist.append(i[:-3])
            simuse.Send_Message(data, sender, 2,
                                '以下是拥有词库的群\n' + str(grouplist) + '\n请发送群号', 1)
            while 1:
                time.sleep(0.5)
                choicegroup = ChatAdmin.get_admin_command(data, sender=sender)
                if choicegroup != None:
                    try:
                        choicegroup = str(choicegroup)
                    except:
                        simuse.Send_Message(data, sender, 2, '参数错误', 1)
                        break
                    if choicegroup in grouplist:
                        onecllist = []
                        onecllist.append(str(choicegroup) + '.cl')
                        findallquestion(data,
                                        sender,
                                        onecllist,
                                        question=[{
                                            'type': 'Plain',
                                            'text': 'AllFind'
                                        }],
                                        allquestion=1,
                                        group=group,
                                        target_type=target_type)
                        break
                    else:
                        simuse.Send_Message(data, sender, 2, '群不存在', 1)
                        break
        elif command == str(3) and group != 0:
            findallquestion(data,
                            sender,
                            cllist,
                            question=[{
                                'type': 'Plain',
                                'text': 'AllFind'
                            }],
                            allquestion=1,
                            group=group,
                            target_type=target_type)
        else:
            return None
