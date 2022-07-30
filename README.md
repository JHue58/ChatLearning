<div align='center' >

  <img src="https://user-images.githubusercontent.com/46672817/161051284-63c8976d-21e9-40a7-a4da-6c8b93f1a401.png" width = "200" height = "165" alt="Nana-Miko"><br>

  <h1>ChatLearning</h1>

 

   [ChatLearning](https://github.com/Nana-Miko/ChatLearning) 是基于 [Mirai Console](https://github.com/mamoe/mirai-console) 的词库插件

[![Release](https://img.shields.io/github/v/release/Nana-Miko/ChatLearning?style=flat-square)](https://github.com/Nana-Miko/ChatLearning/releases)
![Downloads](https://img.shields.io/github/downloads/Nana-Miko/ChatLearning/total?style=flat-square)
[![MiraiForum](https://img.shields.io/badge/post-on%20MiraiForum-blueviolet?style=flat-square)](https://mirai.mamoe.net/topic/1018)
![](https://img.shields.io/badge/Python-100%25-orange?style=flat-square)
[![xxx](https://img.shields.io/badge/Mocking%20Bird-RTVC%20For%20zh-ff69b4?style=flat-square)](https://github.com/babysor/MockingBird)

# 欢迎 Pick💘 本项目 [演示官网](http://chat-learning.skadi.top/)

</div> 

 ## 开始使用

- [mirai-api-http](https://github.com/project-mirai/mirai-api-http) 配置 `http adapter` ， `singleMode` 为 `false` 为了保证稳定性，请尽量使用mirai-api-http v2.3.3版本
- 配置 `data.json` 

```json
{
 "Key": "xxxxx", // 在mirai-api-http中设置的密钥,若使用singleMode也不需要校验,设置为""即可
 "host": "127.0.0.1", // mirai-api-http中设置的地址（若设置成0.0.0.0，请填写127.0.0.1）
 "port": "8080", // mirai-api-http中设置的端口
 "qq": "xxx",  // 在mirai登陆的QQ号
 "session": "xxx" // 无需修改
}
```

- Windows双击 <code>ChatLearning.exe</code> 直接运行
- Linux在<code>cd</code>到目录后使用<code>./ChatLearning</code>运行
- Win7或以下的32位系统(包括32位的Linux)则需下载**Source包**并确保Python版本≥3.6使用 <code>pip install -r requirements.txt</code> 安装依赖后运行 <code>Chatmain.py</code>         
> 首次使用在控制台使用 `setadmin <QQ号,多个请用空格隔开>` 设置管理员； `blackfreq <次数>` 设置黑名单容错次数

## 指令

控制台下可执行指令，发送 `help` 获取指令表；管理员在聊天环境下私聊bot执行指令时，加上指令前缀 `！` 或 `!`

| 基本                              | 描述                         |
|:----------------------------------------|:---------------------------|
| `help`                       | 指令表 |
| `check`                       | 查看词库的问答个数和属性设置   |
| `admin`                       | 进入管理模式  |
| `learning `            | 开启/关闭记录 |
| `reply`                  | 开启/关闭回复 |
| `voicereply` | 开启/关闭文字转语音回复 |
| `setadmin  <QQ>`     | 设置管理员QQ号，有多个用空格隔开 |

------

| 属性                                    | 描述                         |
|:----------------------------------------|:---------------------------|
| `globe`                       | 开启/关闭总词库 |
| `cosmatch`                       | 开启/关闭问题余弦相似度计算 |
| `cosmatch <匹配率>`                       | 设定问题余弦相似度计算匹配率阈值 |
| `blackfreq <次数>`   | 设置黑名单容错次数   |
| `merge <单位/秒>`            | 间隔多长时间合成一次总词库     |
| `learning <单位/秒>`            | 词库链间隔时间   |
| `typefreq <消息类型> <次数>` | 为消息类型设置回复阈值 |
| `voicereply` | 开启/关闭文字转语音回复 |
| `reply <百分比>`  | 回复概率，若没有触发也不会触发文字转语音 |
| `replywait <基准时间> <浮动时间>` | 设置回复时的等待时间（基准时间±浮动时间） |
| `replycd <秒>` | 设置回复的冷却时间 |
| `voicereply  <百分比>` | 文字转语音概率，若没有触发将会继续发送文字 |

- 回复阈值：Bot获取到答案时，需要这个答案在词库中**重复出现**的次数**大于或者等于这个阈值**时，才会回复
- 黑名单容错次数：根据你设置的敏感词，达到次数自动将对象拉入黑名单后，不记录此人所有的发言。
- 全局模式：未启用全局模式时，每个群的词库独立且实时生效（分群词库），上一秒从群中收集到一个词，下一秒就可以在本群中回复这个词。开启全局模式后，bot将采用由所有分群词库定时合成的总词库回复
- 词库链间隔时间：发消息后多长时间会进入空窗期，比如设置10s，一个人发完一条消息10s内没人继续说话，就会将10s后的第一条消息作为问，再下一条就是答，可能没什么卵用，毕竟群里经常上话不接下话，不在一个频道。
- 问题余弦相似度计算：当词库中无该问题时，会启用相似度计算引擎，会将问题与词库中所有的问题进行相似度计算，选取匹配率最高的进行回答（该阈值可设定），较消耗计算机资源，斟酌开启

| 群部分                                     | 描述                         |
|:----------------------------------------|:---------------------------|
| `grouplist`                       | 查看开启记录/回复的群列表  |
| `add/remove learning <群号>`      | 添加/移除开启记录的群，有多个用空格隔开      |
| `add/remove learnings <群号>`       | 同时添加/移除开启记录和回复的群，有多个用空格隔开  |
| `add/remove reply <群号>`        | 添加/移除开启回复的群，有多个用空格隔开 |
| `add/remove tag <标签> <群号>`| 添加/移除群标签(移除时不需要带上标签参数) |
| `add/remove subadmin <群号>` | 添加/移除可自行管理本群词库的群，有多个用空格隔开 |
| `add/remove unmerge <群号>`    | 添加/移除不录入总词库的群，有多个用空格隔开  |

- 群标签：群往往带有一些**属性**，例如xxx游戏群，xxx交流群，这时候可以为群添加相应的标签，在记录词库时，会**记录在相应标签的词库**内，这样在回复时，只会在**相应标签词库内寻找答案**，一个群可以拥有**多个标签，支持中文**

| 文字转语音                                     | 描述                         |
|:----------------------------------------|:---------------------------|
| `setvoicept  <训练集>` | 选择音源合成时的训练模型 |
| `uploadwav` | 上传音源文件 |

| 快速删除         | 描述                         |
| :--------------- | :--------------------------- |
| `fastdelete`     | 更改快速删除功能的使用权限   |
| `settemp` <条数> | 设置单个群中消息缓存最大数目 |

- `快速删除：在开启回复的群中，向Bot所发送的消息回复<code>!d</code> 、<code>!delete</code> 、<code>！d</code> 、<code>！delete</code> 即可在词库中删除该回复

| 定时任务                         | 描述                     |
| :------------------------------- | :----------------------- |
| `add/remove autotask <任务名称>` | 添加/移除定时任务        |
| `autotaskinfo`                   | 查看定时任务详情         |
| `autotaskcommand`                | 查看定时任务中的特殊指令 |

## 定时任务

------

**ChatLearning**在2.9.5版本中加入了定时任务功能，可以自定义地定时执行**ChatLearning**中的指令

**注：若发现输入正确却无法解析内容，请检查txt文件编码是否为UTF-8**

```
'''这是一个定时任务的模板，程序会自动解析带标记的行'''
'''请创建一个新的txt文件放置AutoTask文件夹下来自定义你的任务，文件名即是任务名'''

''开头使用"#"来标记任务的执行日期''
如"每日"：
#everyday
或是"周一 周日"：
#w1 w7
还可以是"每2天":
#x2
亦或是"具体日期"(不足十位请补0，如5→05)：
#2022-08-30

''开头使用"@"来标记执行结果发送的QQ号''
如：
@123456

''开头使用"*"来标记任务的执行时间''
如(请使用英文冒号哦，不足十位请补0，如5→05)：
*05:05

''开头使用"/"来标记任务所需执行的指令''
如(一个指令对应一行)：
/check
/autodelete

以下是示例（每天的12点和23点59分，按顺序执行check，grouplist指令，并将结果发送给123456）：
#everyday
@123456
*12:00 23:59
/check
/grouplist

-------------------
在自动任务中有一些特殊指令：
自动清理词库"autodelete"
发送群消息"sendgroupmessage <群号> <消息>"
发送群图片"sendgroupmessageimage <群号> <图片文件的绝对路径>"
发送好友消息"sendfriendmessage <好友QQ> <消息>"
发送好友图片"sendfriendmessageimage <好友QQ> <图片文件的绝对路径>"
在<消息>这个参数中，可以附带一些指定的标记，程序会将这些标记替换成相应的结果：
当前年：{year}
当前月：{month}
当前日：{day}
换行：{n}
如：
/sendgroupmessage 123456 今天是{year}年{month}月{day}日！{n}大家好啊！
-------------------

```



## 管理模式

- 词库管理：模糊 `搜索/查看/删除` `所有群/指定群` 的词库
- 过滤：自定义无用关键词，也可以通过在删除答案时前加<code>add</code>来直接添加进过滤列表
- 黑名单：自定义敏感关键词，不记录且将对象拉入黑名单，用 <code>blackfreq <次数></code> 自定义容错次数。
- 自动清理词库：删除词库中仅出现过单次的条目和被过滤的条目
- 添加定时任务：使用定时任务定义的语法添加定时任务
- 添加自定义回复：为词库添加回复，问答皆可除视频、文件任意形式的消息(只要QQ能发出来)，同时为答案定义**权重(词库中每个答案都有一个权重，意为答案出现过的次数)**



## **文字转语音**

[ChatLearning—ToVoice](https://github.com/Nana-Miko/ChatLearning/blob/master/ToVoice/ToVoice.md)



## Q&A



**Q：ChatLearning**的功能是什么？

**A：ChatLearning**可以自动的从群聊中收集聊天记录，并且将这些聊天记录整理成一个**问&答**的词库，当有人发送的消息与词库中的”**问**“匹配时，会从“**答**”中随机抽取其中一个回复在群聊中

------

**Q**：打开软件后，我应该如何使用？

**A**：首先应添加需要bot记录的群号，然后开启记录功能（输入<code>help</code>可查看到对应指令）

------

**Q**：要收集多久bot才会开始回复呢？

**A**：收集的时间完全由自己决定，理论上时间越久，效果会更好且更加有趣

------

**Q**：我要怎么才能让bot回复？

**A**：首先应添加需要bot回复的群号，然后开启回复功能（输入<code>help</code>可查看到对应指令）

------

**Q**：目录下的<code>.cl</code>和<code>.clc</code>文件是什么，我可以删除它吗？

**A**：<code>.cl</code>文件是**ChatLearning**所缓存在本地的词库，它的文件名就是所对应的QQ群号，如果你觉得不需要这个词库了，可以在**ChatLearning**退出后将它删除。<code>.clc</code>文件是**ChatLearning**的配置文件，删除后**ChatLearning**会随即崩溃

------

**Q**：目录下的<code>.cl</code>文件太大太占空间了怎么办？

**A**：一般来说不是每天都隔一会99+的群聊，是不会很占空间的， 目前只能选择进入管理模式手动清理一些不需要的回复，后续会更新根据记录的时间批量删除







​	
