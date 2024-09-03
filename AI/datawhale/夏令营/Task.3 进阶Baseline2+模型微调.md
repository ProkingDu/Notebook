## 任务解析

速读一遍task3的文档之后，大概了解到这个task是在baseline基础上针对模型进行微调来优化表现，其中涉及到几个关键的部分：
1. 制作训练集和测试集
2. 在微调平台创建并上传数据集
3. 创建微调任务等待任务完成后发布模型
4. 进行微调推理获取输出文件并提交到赛题进行评分
5. 代码精读

task3的大致步骤如上，这一部分的代码和baseline的示例代码不同，加入了指定模型进行推理的过程。

在完成基础的微调任务之后，自然少不了代码精读，毕竟咱不能只做个CV工程师，对于优秀的代码理解其中的思路也是提升水平的重要方法！

## 一、制作训练集与测试集

这一步骤根据文档给出的操作来，文档地址：[Task3：进阶 baseline2【微调方向】 + 知识点讲解 - 飞书云文档 (feishu.cn)](https://datawhaler.feishu.cn/wiki/Q48xwICyHiV0O2kSwjccuTE1nrb)

这里就不详细截图记录了，涉及到比较重要的部分如下：

### 1.1 训练集的格式

首先是训练集的格式，不同于传统的json文件格式，由于需要使用讯飞平台进行微调，讯飞平台指定的数据集文件格式是`.jsonl` 实际上`.jsonl`与`.json`格式文件唯一的区别在于 **.json文件内包含一个完成的json对象或者数组，一个文件即使一个json对象，而.jsonl文件则相当于由多个json文件组成的集合，他以行为分隔符，每一行是一个json对象。**

简单的示例：
.json:
```json
{ "name": "John", "age": 30, "city": "New York", "languages": ["English", "Spanish"] }
```

.jsonl:
```json
{"name": "John", "age": 30, "city": "New York"}
{"name": "Jane", "age": 25, "city": "Los Angeles"}
{"name": "Mike", "age": 35, "city": "Chicago"}
```

当编程语言解析时，例如Python解析时，.json文件产生的是一个对象，而jsonl是一组对象组成的对象。


### 1.2 Prompt设计

在制作训练集时，对原群聊对话设计了一个总结Prompt，目的是将原始对话内容进行精简。方便做微调数据。
一方面直接将群聊对话作为数据集的话，会**导致上下文过长，超过限制。还有上下文太长会导致抽取效果变差。**
**过长的上下文也会导致训练时长和费用倍增。**

这里的prompt相较于baseline01的区别还是比较明显的，这里的Prompt对需要抽取的任务做了一次总结，通过在原始对话数据中进行一次总结，将总结后的数据作为测试集，这样**一方面能够节约微调的运算资源，另一方面能够让数据被清洗后更容易被模型理解，达到更好的抽取效果。**

文档中给出的Prompt如下：
```python
prompt = f'''
你是一个数据分析大师，你需要从群聊对话中进行分析，里面对话的角色中大部分是客服角色，你需要从中区分出有需求的客户，并得到以下四类数据。
****群聊对话****
{content}
****分析数据****
客户基本信息：需要从中区分出客户角色，并得到客户基本信息，其中包括姓名、手机号码、邮箱、地区、详细地址、性别、年龄和生日
客户意向与预算信息： 客户意向与预算信息包括咨询类型、意向产品、购买异议点、预算是否充足、总体预算金额以及预算明细
客户购买准备情况：户购买准备情况包括竞品信息、客户是否有意向、客户是否有卡点以及客户购买阶段
跟进计划信息： 跟进计划信息包括参与人、时间点和具体事项，这些信息用于指导销售团队在未来的跟进工作中与客户互动
****注意****
1.只输出客户基本信息、客户意向与预算信息、客户购买准备情况、跟进计划信息对应的信息，不要输出无关内容
2.不要输出分析内容
3.输出内容格式为md格式
'''
```

简单分析一下这个prompt，这里首先给出一个身份的提示，也是为了有针对性的提示模型做出行为，同时明确指出所需要做的工作，包括客户的基本信息、客户意向与预算信息、客户购买准备情况、跟进计划信息这四大方面。
通过对原始数据总结，形成相对简洁、具有固定格式的数据，能够对模型训练起到积极的作用。

**但同时思考一下这个prompt是否还可以优化？**

虽然需要模型做的动作已经比较明确清晰，但是这只涉及到基本的提取，是否还可以进一步添加约束条件来提高数据提取的准确性？
例如，客户姓名应当是2-4个字的姓名，并且不要将多个人的姓名同时提取导致混淆。
对于手机号码和邮件这类具有固定格式的数据，给出提示应该可以提高模型的提取能力。
客户购买意向这类单值信息，应该明确值只有是和否。
......

### 1.3 制作训练集

运行NoteBook中给出的代码，等待一段时间即可得到训练集的jsonl文件，最后生成的文件片段如下：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/d9b7f613864b14cc7c908c3c990251e8.png)

其中每一行是一条数据，也是一个单独的json对象，以行分开来组成jsonl文件。其中包括指令、大模型整理后的原始对话数据、用于训练的提取后的数据。

### 1.4 制作测试集

测试集以csv文件存储，有input和target两列，由于我们没有这些数据的真实标签，我这里将target列设置为'-'。

这里也是只需要运行代码获取测试集即可，剩余的部分在代码精读部分解释代码。


## 二、创建数据集并导入

在讯飞大模型训练平台（training.xfuyn.cn）中，在控制台新建数据集：

![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/973b84b8e3e5c1391e9bbda1d3829410.png)


上传制作好的数据集：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/3e90caffff7b34cc8582e91e8577e216.png)

![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/9842ee11cccca10502699f97c4b591fb.png)


按照同样的步骤导入测试集，区别在于图一的选项中数据集类型选择测试集。

上传完成：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/1c199f571d7f1afe96bfed14e6d07179.png)


## 三、创建微调任务

在讯飞大模型定制训练平台中，在模型管理菜单中添加模型：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/5a42d65efecf1e42fc7685e5e7aac884.png)

这里训练方法只有一个lora，关于lora的具体介绍，将放在扩展部分。

提交之后等待微调任务完成：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/8787143f5be7e62cd8759404e1814691.png)


微调完成之后发布为服务：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/9ff34a65d21d9496955b2fef9264373c.png)


进入模型服务控制台找到服务接口信息：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/07e7ded4e6930b85550755cddf46df71.png)


## 四、微调推理并提交结果

将上一步的服务接口信息在NoteBook中替换：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/09cf8b7cc67b18e3cf5b4afee71071fa.png)

**注意这里的顺序是appid、app_secret、app_key，粘贴的时候不要弄倒了！**

之后逐步运行代码，完成之后下载结果提交至比赛平台获取得分：


## 五、代码精读

baseline2的代码有两部分：**制作数据集与微调推理。**



### 5.1 制作训练集的代码

首先是这一部分：
```python
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import numpy as np
from tqdm import tqdm

def chatbot(prompt):
    #星火认知大模型Spark3.5 Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
    SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
    #星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
    SPARKAI_APP_ID = '1c09a91e'
    SPARKAI_API_SECRET = 'MzA2Yjk1OThlYThmZjc4NmM1NzkwMTc1'
    SPARKAI_API_KEY = '0cdcc84efd1d160f05702da9b704d1dd'
    #星火认知大模型Spark3.5 Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
    SPARKAI_DOMAIN = 'generalv3.5'
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(
        role="user",
        content=prompt
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    return a.generations[0][0].message.content
```

这一部分是导入必要的模块，其中包括SparkAI的大语言模型模块，以及ChatMessage消息结构类，之后是最常见的numpy模块，最后的tqdm是用于显示进度条的模块。

这里定义了一个`chatbot()`方法，这个方法在微调推理部分也需要用到，方法内定义了一系列变量、包括SparkAI的webAPI的URL地址以及用于身份认证的appid、app_secret、app_key，这三个参数在大模型控制台获取，随后定义了使用的AI的Domain即指定使用哪一个智能体。

chatbox方法接受一个prompt字符串，并将prompt嵌入到消息体中发送给大语言模型，获取模型响应。

随后实例化大语言模型对象，对象名为`spark`，再实例化一个ChatMessage类的对象用于定义大语言模型接受的消息内容和角色，这里使用列表储存，在随后的调用生成消息的方法中传递的实参也是一个列表，可以大致看出大语言模型支持通过列表同时传递多个消息。

最后将`spark.generate()`返回的数据保存在变量a中，这里返回的是一个对象，然后将a对象的generations中索引为0的项中的第一项这个对象中的message对象的content属性返回。

从最后返回的语句也可以看出，大语言模型可以接受多个消息，并且返回多个消息响应组成的列表，每个列表项中包含一个message对象，其中的content属性是大语言模型的响应内容。


```python
jsonl_data = {"instruction":"假设你是一个智能交互助手，基于用户的输入文本，解析其中语义，抽取关键信息，以json格式生成结构化的语义内容。","input":"请调小空气净化器的湿度到1","output":"{\"intent\":\"CONTROL\",\"slots\":[{\"name\":\"device\",\"normValue\":\"airCleaner\",\"value\":\"空气净化器\"},{\"name\":\"insType\",\"normValue\":\"set\",\"value\":\"调小\"},{\"name\":\"attr\",\"normValue\":\"humidity\",\"value\":\"湿度\"},{\"name\":\"attrValue\",\"normValue\":\"1\",\"v
```
这段代码定义了jsonl_data的结构实例，其中instruction指微调使用数据集中的instruction字段的值，每个对象的此字段都是相同的，具体含义不明。

随后是测试集制作代码的核心部分：
```python
import json

# 打开并读取JSON文件
with open('train.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 训练集制作

# 打开一个文件用于写入，如果文件已存在则会被覆盖
with open('traindata.jsonl', 'w', encoding='utf-8') as file:
    # 训练集行数(130)不符合要求，范围：1500~90000000
    # 遍历数据列表，并将每一行写入文件
    # 这里为了满足微调需求我们重复12次数据集 130*12=1560
    
    for line_data in tqdm(data):
        line_input = line_data["chat_text"] 
        line_output = line_data["infos"]
        content = line_input
        
        prompt = f'''
                你是一个数据分析大师，你需要从群聊对话中进行分析，里面对话的角色中大部分是客服角色，你需要从中区分出有需求的客户，并得到以下四类数据。

                ****群聊对话****
                {content}

                ****分析数据****
                客户基本信息：需要从中区分出客户角色，并得到客户基本信息，其中包括姓名、手机号码、邮箱、地区、详细地址、性别、年龄和生日
                客户意向与预算信息： 客户意向与预算信息包括咨询类型、意向产品、购买异议点、预算是否充足、总体预算金额以及预算明细
                客户购买准备情况：户购买准备情况包括竞品信息、客户是否有意向、客户是否有卡点以及客户购买阶段
                跟进计划信息： 跟进计划信息包括参与人、时间点和具体事项，这些信息用于指导销售团队在未来的跟进工作中与客户互动

                ****注意****
                1.只输出客户基本信息、客户意向与预算信息、客户购买准备情况、跟进计划信息对应的信息，不要输出无关内容
                2.不要输出分析内容
                3.输出内容格式为md格式
                '''
        res = chatbot(prompt=prompt)
        # print(res)
        line_write = {
            "instruction":jsonl_data["instruction"],
            "input":json.dumps(res, ensure_ascii=False),
            "output":json.dumps(line_output, ensure_ascii=False)
        }
        # 因为数据共有130行，为了能满足训练需要的1500条及以上，我们将正常训练数据扩充12倍。
        for time in range(12):
            file.write(json.dumps(line_write, ensure_ascii=False) + '\n')  # '\n' 用于在每行末尾添加换行符
```

这一部分首先是导入了json模块用于处理json数据，随后使用`with open():`的方法打开json文件，并通过`json.load()`方法将json文件中的原始对话数据的json对象转为Python对象。

json文件格式如下：

![小杜的个人图床](http://src.xiaodu0.com/2024/07/07/c447ac1c25254e4e1416cd267c885451.png)

随后打开一个文件用于写入，这个文件就是保存测试集的jsonl文件。

进入主循环，在循环体中，从`data`变量中遍历出`line_data`变量，其中data即包含原始对话数据的对象，line_data对象是每一条对话数据。通过tqdm来展示循环进度。

之后的line_data中的input即为对话原始数据，infos即为整理后的数据，这两者被赋值为line_input与line_output变量作为输入和输出。

将line_input即原始对话数据赋值给content变量，嵌入到随后定义的prompt中，调用chatbot()方法，传入prompt获取模型响应。

并且将响应结果在line_write字典中保存到键为input的数据，也就是模型微调中的输入，这里的输入就是经过简单的总结提炼之后的对话数据，能够提高微调的效率。

数据即为原始数据集中的info字段，也就是已经被提取后的文本信息。

instruction为之前定义的jsonl_data中的指令。

### 5.2 制作测试集的代码

制作测试集与制作训练集的思路大致相同，不过训练集是以jsonl文件储存的，测试集以.csv文件储存。

```python
import json

# 打开并读取JSON文件
with open('test_data.json', 'r', encoding='utf-8') as file:
    data_test = json.load(file)

import csv

# 打开一个文件用于写入CSV数据
with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # 创建一个csv writer对象
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["input","target"])
    # 遍历数据列表，并将每一行写入CSV文件
    for line_data in tqdm(data_test):
        content = line_data["chat_text"]
        prompt = f'''
                你是一个数据分析大师，你需要从群聊对话中进行分析，里面对话的角色中大部分是客服角色，你需要从中区分出有需求的客户，并得到以下四类数据。

                ****群聊对话****
                {content}

                ****分析数据****
                客户基本信息：需要从中区分出客户角色，并得到客户基本信息，其中包括姓名、手机号码、邮箱、地区、详细地址、性别、年龄和生日
                客户意向与预算信息： 客户意向与预算信息包括咨询类型、意向产品、购买异议点、预算是否充足、总体预算金额以及预算明细
                客户购买准备情况：户购买准备情况包括竞品信息、客户是否有意向、客户是否有卡点以及客户购买阶段
                跟进计划信息： 跟进计划信息包括参与人、时间点和具体事项，这些信息用于指导销售团队在未来的跟进工作中与客户互动

                ****注意****
                1.只输出客户基本信息、客户意向与预算信息、客户购买准备情况、跟进计划信息对应的信息，不要输出无关内容
                2.不要输出分析内容
                3.输出内容格式为md格式
                '''
        res = chatbot(prompt=prompt)
        
        # print(line_data["chat_text"])
        ## 文件内容校验失败: test.jsonl(不含表头起算)第1行的内容不符合规则，限制每组input和target字符数量总和上限为8000，当前行字符数量：10721
        line_list = [res, "-"]   
        csvwriter.writerow(line_list)
        # break
```

这里同样使用到json模块，同时导入csv模块用于生成csv文件。

将原始测试集的json文件中的内容读取到data_test变量中，并且在打开csv文件之后，作为循环的范围。

写入csv文件首先需要创建一个csv.writer对象：
```python
writer=csv.writer(file_path)
```
之后通过writer对象的`writerow()`方法即可向csv文件中写入数据，这里接受的实参是一个列表，对应csv文件中每一列的数据。

创建之后写入第一行数据,包含两列：input与target，表示输入与标签。

在data_test中遍历，data_test中只包含chat_text即原始的文本数据。

将原始文本数据嵌入到prompt中，通过chatbot()函数获取大模型响应，并且将得到的总结后的原始对话输入写入到input列中。

### 5.3 微调推理的代码

微调推理部分首先定义了一个写入函数：
```python
# 定义写入函数
def write_json(json_file_path, data):
    #"""写入json文件"""
    with open(json_file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
```

这个函数用于向文件中写入json数据，比较简单，首先以只写模式打开一个文件句柄，然后通过json模块将列表数据转为json字符串并写入到文件中。

接下来定义了几个全局变量：
```python
import SparkApi
import json
#以下密钥信息从控制台获取
appid = "1c09a91e"     #填写控制台中获取的 APPID 信息
api_secret = "MzA2Yjk1OThlYThmZjc4NmM1NzkwMTc1"   #填写控制台中获取的 APISecret 信息
api_key ="0cdcc84efd1d160f05702da9b704d1dd"    #填写控制台中获取的 APIKey 信息
#调用微调大模型时，设置为“patch”
domain = "patchv3"
#云端环境的服务地址
# Spark_url = "wss://spark-api-n.xf-yun.com/v1.1/chat"  # 微调v1.5环境的地址
Spark_url = "wss://spark-api-n.xf-yun.com/v3.1/chat"  # 微调v3.0环境的地址
text =[]
```

这里即之前微调推理部分提到的服务认证信息，需要注意的是domain和Spark_url，如果在模型微调时使用的是Spark Lite模型，这里需要指定domain为patch，url为被注释的第一个微调1.5环境地址。

这里的text是全局共用的一个用于储存消息体的变量。

随后定义了几个功能函数：
```python
def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text
```

这个函数`getText()`接受一个角色和内容参数，在函数内定义一个字典类型的局部变量，在字典中加入role和content这两个键值对，并且将jsoncon即字典加入text即消息列表中。

```python
def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length
```

这个函数用于计算消息列表中的所有消息的长度，只统计content的长度。

```python
def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
```
这个函数用于检查消息长度，在一个循环中通过`getlength()`函数来获取消息列表内所有消息的长度，如果所有消息长度加起来大于8000个字符，则删除消息队列中的第一条消息，否则返回text即消息列表。

```python
def core_run(text,prompt):
    # print('prompt',prompt)
    text.clear
    Input = prompt
    question = checklen(getText("user",Input))
    SparkApi.answer =""
    # print("星火:",end = "")
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    getText("assistant",SparkApi.answer)
    # print(text)
    return text[-1]['content']
```

这个函数用于核心运行，接受一个text与prompt参数，分别表示消息列表和输入的Prompt，在函数内部，首先将text清空，随后将prompt赋值给input变量，下一行的question中，首先调用`getText()`函数将Input也就是接受的prompt参数和role='user'组成消息体，加入消息列表中，再调用检查长度的函数防止消息过长。
预定义SparkApi.answer即回答为空，初始化字符串。
调用SparkApi对象的main方法，传入服务认证信息与指定模型调用地址和domain以及问题（这里的question即prompt和role组成的message。）
在模型响应之后，通过SparkApi对象的answer属性获取响应的消息，通过getText方法来将响应消息加入列表。

随后调用一个测试demo：
```python
text = []

res = core_run(text,'你好吗？')
```

导入pandas和re库来加载之前制作的测试集的csv文件：
```python
import pandas as pd
import re

# 读取Excel文件
df_test = pd.read_csv('test.csv',)
```


定义提取的结构：
```python
data_dict_empty = {
                "基本信息-姓名": "",
                "基本信息-手机号码": "",
                "基本信息-邮箱": "",
                "基本信息-地区": "",
                "基本信息-详细地址": "",
                "基本信息-性别": "",
                "基本信息-年龄": "",
                "基本信息-生日": "",
                "咨询类型": [],
                "意向产品": [],
                "购买异议点": [],
                "客户预算-预算是否充足": "",
                "客户预算-总体预算金额": "",
                "客户预算-预算明细": "",
                "竞品信息": "",
                "客户是否有意向": "",
                "客户是否有卡点": "",
                "客户购买阶段": "",
                "下一步跟进计划-参与人": [],
                "下一步跟进计划-时间点": "",
                "下一步跟进计划-具体事项": ""
            }
```

开始从整理后的原始消息中提取关键信息：
```python
submit_data = []
for id,line_data in tqdm(enumerate(df_test['input'])):
    # print(line_data)
    content = line_data
    text = []
    prompt = json.dumps(content,ensure_ascii=False)
    
    # print(json.dumps(content,ensure_ascii=False))
    res = core_run(text,prompt)
    try:
        data_dict = json.loads(res)
    except json.JSONDecodeError as e:
        data_dict = data_dict_empty
    submit_data.append({"infos":data_dict,"index":id+1})
```

这里首先定义了一个空列表`submit_data`，然后在测试集的input列也就是经过大模型初步总结后的原始对话数据来遍历，在循环体中line_data即当前行的对话数据，将其赋值给content，将其转为json之后赋值给prompt，顺便声明了text为空列表。通过core_run函数来获取大模型响应，如果能够正确解析json数据，则在submit_data列表中加入一个字典，字段的info字段为data_dict即当前响应数据解析json后的数据，索引为当前行号加1（因为行号从0开始）。如果不能正常解析，则加入默认提取结构但是数据为空的字典。

循环结束之后，打印出submit_data的内容，并且写入到submit.json文件中：
```python
submit_data
write_json("submit.json",submit_data)
```