<div align='center' >

  <img src="https://user-images.githubusercontent.com/46672817/161051284-63c8976d-21e9-40a7-a4da-6c8b93f1a401.png" width = "200" height = "165" alt="Nana-Miko"><br>

  <h1>ChatLearning</h1>

 

   [ChatLearning](https://github.com/Nana-Miko/ChatLearning) 是基于 [Mirai Console](https://github.com/mamoe/mirai-console) 的词库插件

[![Release](https://img.shields.io/github/v/release/Nana-Miko/ChatLearning?style=flat-square)](https://github.com/Nana-Miko/ChatLearning/releases)
![Downloads](https://img.shields.io/github/downloads/Nana-Miko/ChatLearning/total?style=flat-square)
[![MiraiForum](https://img.shields.io/badge/post-on%20MiraiForum-blueviolet?style=flat-square)](https://mirai.mamoe.net/topic/1018)
![](https://img.shields.io/badge/Python-100%25-orange?style=flat-square)
[![xxx](https://img.shields.io/badge/Mocking%20Bird-RTVC%20For%20zh-ff69b4?style=flat-square)](https://github.com/babysor/MockingBird)

# 欢迎 Pick💘 本项目 [官方网站](http://chat-learning.skadi.top/)

</div> 

 ## 开始使用

- [mirai-api-http](https://github.com/project-mirai/mirai-api-http) 配置 `http adapter` ， `singleMode` 为 `false`
- 配置 `data.json` 

```json
{
 "Key": "xxxxx", //在mirai-api-http中设置的密钥
 "host": "127.0.0.1", //mirai-api-http中设置的地址（若设置成0.0.0.0，请填写127.0.0.1）
 "port": "8080", //mirai-api-http中设置的端口
 "qq": "xxx",  //在mirai登陆的QQ号
 "session": "xxx" //无需修改
}
```

- Windows双击 <code>ChatLearning.exe</code> 直接运行
- Linux在<code>cd</code>到目录后使用<code>./ChatLearning</code>运行
- Win7或以下的32位系统(包括32位的Linux)则需下载**Source包**并确保Python版本≥3.6使用 <code>pip install -r requirements.txt</code> 安装依赖后运行 <code>Chatmain.py</code> 
> 请使用你喜欢的[虚拟环境](https://zhuanlan.zhihu.com/p/368095197)安装依赖，否则可能导致错误         
> 首次使用在控制台使用 `setadmin <你的QQ号>` 设置管理员； `blackfreq <次数>` 设置黑名单容错次数

## 指令

控制台发送 `help` 可获取指令表；管理员在聊天环境下私聊bot执行指令时，加上指令前缀 `！` 或 `!`

| 指令                                      | 描述                         |
|:----------------------------------------|:---------------------------|
| `admin`                       | 进入管理模式                     |
| `learning `            | 开启/关闭记录 |
| `reply`                  | 开启/关闭回复             |
| `globe`                       | 开启/关闭全局模式                     |
| `voicereply` | 开启/关闭文字转语音回复 |
| `setadmin  <QQ>`                       | 设置管理员QQ号，有多个用空格隔开                     |
| `blackfreq <次数>`                       | 设置黑名单容错次数                     |
| `merge <单位/秒>`                  | 设定总词库更新时间        |
| `check`                       | 查看词库的问答个数和属性设置                     |
| `grouplist`                       | 查看开启记录/回复的群列表                     |
| `add/remove learning <群号>`                       | 添加/移除开启记录的群，有多个用空格隔开                |
| `add/remove learnings <群号>`                       | 同时添加/移除开启记录和回复的群，有多个用空格隔开                  |
| `add/remove reply <群号>`                      | 添加/移除开启回复的群，有多个用空格隔开                   |
| `add/remove subadmin <群号>` | 添加/移除可自行管理的群，有多个用空格隔开 |
| `add/remove unmerge <群号>`                    | 添加/移除不录入总词库的群，有多个用空格隔开                   |
| `setvoicept  <训练集>` | 选择音源合成时的训练模型 |
| `uploadwav` | 上传音源文件 |



## 管理模式

- 词库管理：模糊 `搜索/查看/删除` `所有群/指定群` 的词库
- 过滤：自定义无用关键词，也可以通过在删除答案时前加<code>add</code>来直接添加进过滤列表
- 黑名单：自定义敏感关键词，不记录且将对象拉入黑名单，用 <code>blackfreq <次数></code> 自定义容错次数。



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







​	
