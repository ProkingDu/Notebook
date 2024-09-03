
## step.1 在讯飞星火平台报名比赛：
赛事链接：[https://challenge.xfyun.cn/h5/detail?type=role-element-extraction&ch=dw24_y0SCtd](https://challenge.xfyun.cn/h5/detail?type=role-element-extraction&ch=dw24_y0SCtd)
![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/55d1a515f0ce354f025a45eda996db07.png)


## step.2 申请讯飞开放平台API

链接：https://console.xfyun.cn/app/myapp

![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/fd39fe8849a940b3766f058d776af117.png)

点击应用名称进入控制台：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/22b4bc56922b18c8bf6fff8724c6cabf.png)

点击更多服务信息查询：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/ba3f4de499fb24ff8b6c0f2e969a5c3f.png)

红框部分即为所需要的服务接口认证信息


讯飞开放平台为新用户免费提供了一亿次token，有效期为一年，在之后的task中可能也会用得到，在![https://console.xfyun.cn/sale/buy?wareId=9108&packageId=9108001&serviceName=Spark3.5%20Max&businessId=bm35]()中领取。

![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/86a4743dd53c27f344a61c58e69cd4fc.png)
## step.2 尝试baseline

项目链接：https://aistudio.baidu.com/projectdetail/8095619

![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/070b85734f485984c4f21cec18509ab7.png)

## step.3 运行项目

![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/00951f4a090d64778bb87a2f197f62c2.png)

在控制台的main.ipynb中输入自己在讯飞开放平台得到的服务接口认证信息，包括APPID、API_SECRET、API_TOKEN。

随后，点击一键运行全部Cell运行任务项目：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/979a347063ce99a1ef873cb6c0f3f3c0.png)

运行大概需要30分钟，在这个时间内去观看了暑期夏令营开营仪式的回放~

运行完成之后，找到右侧生成的output.json文件，右击下载。
![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/64929ae5bed4b9f5150efc05243e89b5.png)

下载完成之后，在电脑上打开确认生成结果无误，同时观察下生成的数据和项目中执行的格式是否一致。

![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/0ef9ed699cfdcfe26539b64ab5c05f70.png)

上图是项目中定义的输出数据结构。

![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/a538c15be12ef94c016274547676c829.png)

下载后打开output.json查看，数据基本一致，可以提交结果至讯飞赛事平台。

## step.4 上传结果，查看分数。

在讯飞开放平台进入赛事，点击提交结果，上传Output.json，点击提交按钮，等待系统评分。
![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/20439f755c6bf7208ff2d1aceac2779e.png)


最终评分结果：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/b5b50278b01d32926f027e50ff3ca9e7.png)

## step.4 提交问卷

在夏令营问卷中提交结果，并附上本笔记链接。
![小杜的个人图床](http://src.xiaodu0.com/2024/07/01/38b9fd01e592b95e9386fadc147ce64f.png)



## Tag

本笔记来自DataWhale（[Datawhale (linklearner.com)](https://linklearner.com)）暑期夏令营活动学习过程中记录。
关于DataWhale：

- Datawhale是一个专注于AI领域的开源组织，致力于构建一个纯粹的学习圈子，帮助学习者更好地成长。我们专注于机器学习，深度学习，编程和数学等AI领域内容的产出与学习。  
  
- Datawhale发展于2018年12月6日。团队成员规模也在不断扩大，有来自双非院校的优秀同学，也有来自上交、武大、清华等名校的小伙伴，同时也有来自微软、字节、百度等企业的工程师。  
  
- 我们将一群有能力有想法的理想青年们集结在一起，共同改善学习的模式。在这里，我们没有标签。如果你是小白，我们将为你提供学习和改变的机会，如果你是优秀的学习者，我们将向你提供提升和发展的平台。