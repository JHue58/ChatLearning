<div align='center' >
  
  <h1>ChatLearning</h1>
 
  ChatLearning 是基于 [Mirai Console](https://github.com/mamoe/mirai-console) 的词库插件

  <img src="http://sayuri.fumiama.top/cmoe?name=yourname&theme=r34" alt="yourname" />
 
[![Release](https://img.shields.io/github/v/release/Nana-Miko/ChatLearning?style=flat-square)](https://github.com/Nana-Miko/ChatLearning/releases)
![Downloads](https://img.shields.io/github/downloads/Nana-Miko/ChatLearning/total?style=flat-square)
[![MiraiForum](https://img.shields.io/badge/post-on%20MiraiForum-ff69b4?style=flat-square)](https://mirai.mamoe.net/topic/1018)
[![issues](https://img.shields.io/github/issues/Nana-Miko/ChatLearning?style=flat-square)](https://github.com/Nana-Miko/ChatLearning/issues)

</div> 

 ## 开始使用

**使用前应该查阅的相关文档或项目**

* [User Manual](https://github.com/mamoe/mirai/blob/dev/docs/UserManual.md)
* [Permission Command](https://github.com/mamoe/mirai/blob/dev/mirai-console/docs/BuiltInCommands.md#permissioncommand)
* [Chat Command](https://github.com/project-mirai/chat-command)

前置插件：[mirai-api-http](https://github.com/project-mirai/mirai-api-http)请先安装并配置好，使用 `http ` ，并确保 `singleMode` 为 `false`

在 `data.json` 文件中填入 `mirai-api-http` 的配置信息

```json
{
 "Key": "xxxxx", //在mirai-api-http中设置的密钥
 "host": "127.0.0.1", //mirai-api-http中设置的地址（若设置成0.0.0.0，请填写127.0.0.1）
 "port": "8080", //mirai-api-httpmirai-api-http中设置的端口
 "qq": "xxx",  //所登录mirai的QQ号
 "session": "xxx" //任意，由程序自动获取
}
```

**Windows**用户点击<code>Chatmain.exe</code>运行

**Linux**用户则使用python运行<code>Chatmain.py</code>脚本 **（python版本需为3.5以上）**

输入<code>help</code>来查看命令列表



## 依赖

本项目所使用的一些Python模块：

<code>asyncio </code>   <code>prompt_toolkit</code>   <code>nest_asyncio</code>   <code>threading</code> <code>cos-python-sdk-v5</code>

以上模块**Linux**用户可能会缺少，请先用<code>cd</code>切换到所在目录，然后使用<code>pip install -r requirements.txt</code>安装所需依赖

也可自行通过<code>pip install</code>来安装对应模块

## 指令

发送 `help` 可获取指令表 如需在聊天环境下使用指令，请使用管理员QQ私聊bot，且指令前加上<code>！</code>如<code>！help</code>

| 指令                                      | 描述                         |
|:----------------------------------------|:---------------------------|
| `learning`                       | 开启/关闭记录 |
| `reply`                  | 开启/关闭回复             |
| `merge xxx`                  | 设定总词库更新时间，xxx的单位为秒         |
| `add learning xxx`                       | 添加开启记录的群，有多个用空格隔开                |
| `add learnings xxx`                       | 同时添加开启记录和回复的群，有多个用空格隔开                  |
| `add reply xxx`                      | 添加开启回复的群，有多个用空格隔开                   |
| `add unmerge xxx`                    | 添加不录入总词库的群，有多个用空格隔开                   |
| `remove learning xxx`                        | 移除开启记录的群，有多个用空格隔开                |
| `remove reply xxx`                       | 移除开启回复的群，有多个用空格隔开                     |
| `remove unmerge xxx`                       | 移除不录入总词库的群，有多个用空格隔开                     |
| `check`                       | 查看词库的问答个数和属性设置                     |
| `grouplist`                       | 查看开启记录/回复的群列表                     |
| `globe`                       | 开启/关闭全局模式                     |
| `setadmin  xxx`                       | 设置管理员QQ号，有多个用空格隔开                     |
| `blackfreq xxx`                       | 设置黑名单容错次数                     |
| `admin`                       | 进入管理模式                     |

## **管理模式**

在**ChatLearning 1.2.0**版本后，使用了全新的管理模式

### 	在所有群内搜索

​		该模式下支持模糊搜索所有群的词库，或者查看指定群的词库，**预览结果不包含无答案词条**（出现找到xx个结果却无显示结果）

​		需删除时请按照提示输入指定行，**注意是行不是ID！**

### 	在指定群内搜索

​		与**1.2.0**版本之前的管理模式一致，在特定的群词条中删除词库

### 	过滤设置

#### 		过滤条目

​			在收集词库的的过程中，往往有一些你认为无意义，没必要的答案，这时可以添加到过滤条目中，ChatLearning将不会记录与之			匹配的问题与答案，你也可以通过在删除答案时前加<code>add</code>来直接添加进过滤列表

#### 		敏感关键字

​			在这里你可以添加一些过于敏感的词语（或是图片），如涉政，涉黄，涉暴等，当ChatLearning检测到问题中有这些关键字时，			将不会记录，与此同时将发送者列入黑名单

#### 		黑名单

​			处于黑名单的账号，都会有自己的容错次数（也就是触发敏感词的次数），当它超过你的设定值时，ChatLearning会将其屏蔽，			此账号下的任何发言都将不作记录

​			你可以通过<code>blackfreq *</code>指令来更改容错次数



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

**Q**：什么是全局模式？

**A**：未启用全局模式时，bot只会回复所对应群中收集的词库（这个是实时生效的，上一秒从群中收集到词库，下一秒就可以在本群中回复这个词库了），当开启全局模式时，bot只会从**ChatLearning周期性**整合的从所有群收集到的**总词库**中回复相应数据，你可以**自行调整这个周期**的时间，并且你也可以选择不让某些群的词库被整合进这个**总词库**中

------

**Q**：什么是词库链间隔时间？

**A：ChatLearning**将第一个人的消息定义为一个词库链的头，他的消息只会被记录为问题，不会被记录为答案，而第一个人在**ChatLearning**中的定义是间隔一定时间无人发言后，**第一个发言的人**，你可以自行调整这个间隔时间，默认为900秒

------

**Q**：什么是管理模式？

**A**：在这个模式中，你可以删除一些你觉得需要删除的回复，首先需要设置管理员QQ

------

**Q**：为什么管理员QQ只能设置一个？

~~**A**：懒，如果有需求的话后续版本可以更新~~

**A**：V1.1.0以上版本已支持

------

**Q**：目录下的<code>.cl</code>和<code>.clc</code>文件是什么，我可以删除它吗？

**A**：<code>.cl</code>文件是**ChatLearning**所缓存在本地的词库，它的文件名就是所对应的QQ群号，如果你觉得不需要这个词库了，可以在**ChatLearning**退出后将它删除。<code>.clc</code>文件是**ChatLearning**的配置文件，删除后**ChatLearning**会随即崩溃

------

**Q**：目录下的<code>.cl</code>文件太大太占空间了怎么办？

**A**：一般来说不是每天都隔一会99+的群聊，是不会很占空间的， 目前只能选择进入管理模式手动清理一些不需要的回复，后续会更新根据记录的时间批量删除







