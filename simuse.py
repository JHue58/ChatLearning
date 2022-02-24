import json
import time

import requests as r


#取得数据包
def Get_data():
    data_file = open(r'data.json', 'r', encoding='utf-8-sig')
    data = data_file.read()
    data = json.loads(data)
    host = data['host']
    if host.find(':') == -1:
        data['host'] = data['host'] + ':' + data['port']
    try:
        host.strip('：', ':')
    except:
        pass
    return data


#取得缓存的事件
def Get_Meesage():
    time.sleep(0.5)
    try:
        tempfile = open(r'messagetemp.sim', 'r', encoding='utf-8')
    except:
        return 0
    try:
        Message = eval(tempfile.read())
    except:
        tempfile.close()
        return 0
    tempfile.close()
    return Message


#激活会话ID（不要单独调用）
def Check_Session(host, session, qq):
    url = 'http://' + host + '/bind'
    data_in = dict(sessionKey=session, qq=qq)
    res = r.request('post', url, json=data_in)
    res = json.loads(res.text)
    return (res['code'])


#取得会话ID  (getsession:传入不为0的int值可让函数返回已激活的会话ID)
#0-已启动mah但未登录qq，1-未启动mah或mah配置错误
def Get_Session(data, getsession=0):
    host = data['host']
    verifyKey = data['Key']
    qq = data['qq']
    url = 'http://' + host + '/verify'
    data_in = dict(verifyKey=verifyKey)
    try:
        res = r.request('post', url, json=data_in)
    except:
        return 1
    else:
        res = json.loads(res.text)
        session = res['session']
        code = Check_Session(host, session, qq)
        if (getsession == 0 and code == 0):
            data.update(session=session)
            return data
        elif (getsession != 0 and code == 0):
            return session
        else:
            #print('创建失败')
            return 0


#接收消息 (若传入deal=0，则表示返回不经过简化的原消息信息和事件)
def Fetch_Message(data, deal=1):
    host = data['host']
    session = data['session']
    url = 'http://' + host + '/fetchMessage' + '?sessionKey=' + session + '&count=10'
    res = r.request('get', url)
    res = json.loads(res.text)
    Message = res['data']
    if deal == 1:
        Message = Fetch_Message_info(Message)
        return Message
    elif deal == 0:
        return Message
    else:
        return 0


#接受消息/事件信息(简化处理)
def Fetch_Message_info(Message):
    messagemain = dict()
    messageinfo = dict()
    Message_c = []
    for i in Message:
        if i['type'] != 'GroupMessage' and i['type'] != 'FriendMessage':
            Message_c.append(i.copy())
        else:
            messageinfo.update(type=i['type'])
            messageinfo.update(messagechain=i['messageChain'])
            senderinfo = i['sender']
            messageinfo.update(sender=senderinfo['id'])
            if i['type'] == 'GroupMessage':
                groupinfo = senderinfo['group']
                messageinfo.update(group=groupinfo['id'])
            Message_c.append(messageinfo.copy())
    if str(Message_c) == '[]':
        return 0
    else:
        return (Message_c)


#发送消息(target_type:1-群,2-私聊,3-临时会话;message_type:1-文字,2-图片;path:传入不为0的int值可发送本地图片，默认为url)
##target_type为3，传入的target应当为一个字典dict，格式:{'qq':'123','group':'123'}
#返回值为本次发送的消息id
def Send_Message(data, target, target_type, message, message_type, path=0):
    host = data['host']
    session = data['session']
    if target_type == 1 and message_type == 1:
        #print('1')
        url = 'http://' + host + '/sendGroupMessage'
        messageinfo = []
        messagechain = dict(type='Plain', text=message)
        messageinfo.append(messagechain.copy())
    elif target_type == 2 and message_type == 1:
        #print('2')
        url = 'http://' + host + '/sendFriendMessage'
        messageinfo = []
        messagechain = dict(type='Plain', text=message)
        messageinfo.append(messagechain.copy())
    elif target_type == 1 and message_type == 2:
        #print('3')
        url = 'http://' + host + '/sendGroupMessage'
        messageinfo = []
        if path == 0:
            messagechain = dict(type='Image', url=message)
            messageinfo.append(messagechain.copy())
        elif path != 0:
            messagechain = dict(type='Image', path=message)
            messageinfo.append(messagechain.copy())
    elif target_type == 2 and message_type == 2:
        #print('4')
        url = 'http://' + host + '/sendFriendMessage'
        messageinfo = []
        if path == 0:
            messagechain = dict(type='Image', url=message)
            messageinfo.append(messagechain.copy())
        elif path != 0:
            messagechain = dict(type='Image', path=message)
            messageinfo.append(messagechain.copy())
    elif target_type == 3 and message_type == 1:
        #print('5')
        url = 'http://' + host + '/sendTempMessage'
        messageinfo = []
        messagechain = dict(type='Plain', text=message)
        messageinfo.append(messagechain.copy())
    elif target_type == 3 and message_type == 2:
        #print('6')
        url = 'http://' + host + '/sendTempMessage'
        messageinfo = []
        if path == 0:
            messagechain = dict(type='Image', url=message)
            messageinfo.append(messagechain.copy())
        elif path != 0:
            messagechain = dict(type='Image', path=message)
            messageinfo.append(messagechain.copy())
    else:
        return 0
    if target_type == 3:
        data_in = dict(sessionKey=session, messageChain=messageinfo)
        data_in.update(target)
    else:
        data_in = dict(sessionKey=session,
                       target=target,
                       messageChain=messageinfo)
    res = r.request('post', url, json=data_in)
    res = json.loads(res.text)
    if res['code'] == 0:
        return res['messageId']


#若了解mah的消息链后，可以用此函数发送消息链
#返回值为本次发送的消息id
def Send_Message_Chain(data, target, target_type, messagechain):
    host = data['host']
    session = data['session']
    if target_type == 1:
        url = 'http://' + host + '/sendGroupMessage'
    elif target_type == 2:
        url = 'http://' + host + '/sendFriendMessage'
    elif target_type == 3:
        url = 'http://' + host + '/sendTempMessage'
    else:
        return 0
    if target_type == 3:
        data_in = dict(sessionKey=session, messageChain=messagechain)
        data_in.update(target)
    else:
        data_in = dict(sessionKey=session,
                       target=target,
                       messageChain=messagechain)
    res = r.request('post', url, json=data_in)
    res = json.loads(res.text)
    if res['code'] == 0:
        return res['messageId']


#获取数据包，填入mah配置的地址host端口号port和密钥verifyKey以及登录mirai的qq，若已获取会话ID，则可填入会话IDsession
def Creat_data(host='127.0.0.1', port='8080', verifyKey='', qq='', session=''):
    host = str(host)
    port = str(port)
    verifyKey = str(verifyKey)
    qq = str(qq)
    host = host + ':' + port
    data = dict(host=host, Key=verifyKey, qq=qq, session=session)
    return data


#撤回消息，messageid为消息的id
def Recall_Message(data, messageid):
    session = data['session']
    host = data['host']
    url = 'http://' + host + '/recall'
    data_in = dict(sessionKey=session, target=messageid)
    res = r.request('post', url, json=data_in)
    res = json.loads(res.text)
    return res


#禁言成员(target为指定群，member为对象qq号，time为禁言时间，单位秒，若不传入member，则默认全体禁言)
#需要有相关权限
def Mute(
    data,
    target,
    member='0',
    time=0,
):
    session = data['session']
    host = data['host']
    if member != '0':
        url = 'http://' + host + '/mute'
        data_in = dict(sessionKey=session,
                       target=target,
                       memberId=member,
                       time=time)
        res = r.request('post', url, json=data_in)
        res = json.loads(res.text)
        return res
    else:
        url = 'http://' + host + '/muteAll'
        data_in = dict(sessionKey=session, target=target)
        res = r.request('post', url, json=data_in)
        res = json.loads(res.text)
        return res


#解除禁言(target为指定群，member为对象qq号，若不传入member，则默认解除全体禁言)
#需要有相关权限
def Unmute(data, target, member='0'):
    session = data['session']
    host = data['host']
    if member != '0':
        url = 'http://' + host + '/unmute'
        data_in = dict(sessionKey=session, target=target, memberId=member)
        res = r.request('post', url, json=data_in)
        res = json.loads(res.text)
        return res
    else:
        url = 'http://' + host + '/unmuteAll'
        data_in = dict(sessionKey=session, target=target)
        res = r.request('post', url, json=data_in)
        res = json.loads(res.text)
        return res


#踢出群成员(target为指定群，member为对象qq号)
#需要有相关权限
def Kick(data, target, member):
    session = data['session']
    host = data['host']
    url = 'http://' + host + '/kick'
    data_in = dict(sessionKey=session, target=target, memberId=member)
    res = r.request("post", url, json=data_in)
    res = json.loads(res.text)
    return res


#设置群 target为指定群，config为需设置内容,数据类型为字典dict,或在传参时指定参数名称传入
#例:Group_Config(data,target,name='ok',announcement='test'……)
#config中的参数名称：name(str)-群名，announcement(str)-群公告，confessTalk(bool)-是否开启坦白说；
#allowMemberInvite(bool)-是否允许群员邀请，autoApprove(bool)-是否开启自动审批入群，anonymousChat(bool)-是否允许匿名聊天
#需要有相关权限
def Group_Config(data, target, **config):
    session = data['session']
    host = data['host']
    url = 'http://' + host + '/groupConfig'
    data_in = dict(sessionKey=session, target=target, config=config)
    res = r.request('post', url, json=data_in)
    res = json.loads(res.text)
    return res


#设置群成员资料，target为指定群，memberid为群成员QQ，config为需设置内容,数据类型为字典dict,或在传参时指定参数名称传入
#例:Member_Info(data,target,memberid，name='ok',specialTitle='test'……)
#config中的参数名称：name(str)-群名片，specialTitle(str)-群头衔
#需要有相关权限
def Member_Info(data, target, memberid, **config):
    session = data['session']
    host = data['host']
    url = 'http://' + host + '/memberInfo'
    data_in = dict(sessionKey=session,
                   target=target,
                   memberId=memberid,
                   info=config)
    res = r.request('post', url, json=data_in)
    res = json.loads(res.text)
    return res


#退出群聊，target为指定群
def Quit(data, target):
    session = data['session']
    host = data['host']
    url = 'http://' + host + '/quit'
    data_in = dict(sessionKey=session, target=target)
    res = r.request('post', url, json=data_in)
    res = json.loads(res.text)
    return res


#取得bot的好友列表，返回值为列表
#参数名称：id-qq号，nickname-好友昵称，remark-备注
def Get_Friend(data):
    session = data['session']
    host = data['host']
    url = 'http://' + host + '/friendList?sessionKey=' + session
    res = r.request('get', url)
    res = json.loads(res.text)
    List = res['data']
    return List


#取得bot的群列表，返回值为列表
#参数名称：id-群号，name-群昵称，permission-权限
def Get_Group(data):
    session = data['session']
    host = data['host']
    url = 'http://' + host + '/groupList?sessionKey=' + session
    res = r.request('get', url)
    res = json.loads(res.text)
    List = res['data']
    return List


#取得指定群的设置信息，返回值为字典
#参数名称：name-群名称，confessTalk-是否开启坦白说，allowMemberInvite-是否允许群员邀请，autoApprove-是否开启自动审批入群，anonymousChat-是否允许匿名聊天
def Get_Groupinfo(data, target):
    session = data['session']
    host = data['host']
    target = str(target)
    url = 'http://' + host + '/groupConfig?sessionKey=' + session + '&target=' + target
    res = r.request('get', url)
    res = json.loads(res.text)
    return res


#取得指定群的群成员列表，返回值为列表
#参数名称：id-qq号，memberName-群名片，specialTitle-群头衔，permission-权限
#若传入deal=0，则还可返回群成员的joinTimestamp-入群时间戳，lastSpeakTimestamp-最后一次发言时间戳,muteTimeRemaining-禁言剩余时间
def Get_Groupmember(data, target, deal=1):
    if deal != 1 and deal != 0:
        return 0
    session = data['session']
    host = data['host']
    target = str(target)
    url = 'http://' + host + '/memberList?sessionKey=' + session + '&target=' + target
    res = r.request('get', url)
    res = json.loads(res.text)
    List = res['data']
    for i in List:
        i.pop('group')
        if deal != 0:
            i.pop('joinTimestamp')
            i.pop('lastSpeakTimestamp')
            i.pop('muteTimeRemaining')
    return List


#取得指定群的群成员资料，返回值为字典
#参数名称：id-qq号，memberName-群名片，specialTitle-群头衔，permission-权限，muteTimeRemaining-禁言剩余时间
#若传入deal=0，则还可返回joinTimestamp-入群时间戳，lastSpeakTimestamp-最后一次发言时间戳
def Get_memberinfo(data, target, id, deal=1):
    session = data['session']
    host = data['host']
    target = str(target)
    id = str(id)
    url = 'http://' + host + '/memberInfo?sessionKey=' + session + '&target=' + target + '&memberId=' + id
    res = r.request('get', url)
    res = json.loads(res.text)
    res.pop('group')
    if deal == 1:
        res.pop('joinTimestamp')
        res.pop('lastSpeakTimestamp')
        return res
    elif deal == 0:
        return res
    else:
        return 0
