# Task.1 Baseline
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



# Task.2 赛题解析与代码精读
## 一、赛题解析

### 1.1 赛题说明

本次baseline的赛题背景是：
> 在数字化时代，企业积累了大量对话数据，这些数据不仅是交流记录，还隐藏着宝贵的信息。群聊对话分角色要素提取是企业营销和服务的重要策略，通过分析这些数据，企业可以更好地理解客户需求，提供个性化服务，提升客户满意度和商业价值。

赛事任务：
> 从给定的<客服>与<客户>的群聊对话中，提取出指定的字段信息，具体待提取的字段信息见下文。

参赛选手需**基于讯飞星火大模型****Spark Max**完成任务，可使用大模型微调。

### 1.2 任务解析

从赛题来看，基本的任务是通过讯飞星火大模型来实现企业聊天文本分割，实际上这也是一个经典的NLP（自然语言处理）任务，不过基于大模型来完成，相对于传统的NLP任务会具有更高的灵活度以及更少的工作量。

这其中在我的理解是涉及到一个完成基本的任务，也就是指导大模型从文本中提取对话数据，另一方面，由于大模型对数据的处理会存在误差，因此需要调整Prompt来优化回复。

所以从赛题整体来看，我们需要完成了两个任务：
1. 通过API实现基本的文本处理，从文本中提取对话数据
2. 优化模型表现，包括优化Prompt与模型微调等。


赛题要求从对话中提取的字段包括如下大类：
1. 基本信息
2. 咨询类型
3. 意向产品
4. 购买异议点
5. 客户预算
6. 竞品信息
7. 客户是否有意向
8. 客户是否有卡点
9. 客户购买阶段
10. 下一步跟进计划

其中，基本信息包括：
1. 姓名
2. 手机号
3. 邮箱
4. 地区
5. 详细地址
6. 性别
7. 年龄
8. 生日

客户预算包括：
1. 预算是否充足
2. 总体预算金额
3. 预算明细

下一步跟进计划包括：
1. 参与人
2. 时间点
3. 具体事项

同时，存在比较特殊的字段，他是**非单值字段，应当通过列表表示。** **对于无法提取或者为空的字段，使用空值表示。** 另外需要注意的是，对于答案唯一的字段，大模型给出的答复应当是唯一的，即使在微调的时候，这个值也不应该出现变化（这个在Prompt中应该如何设计？）

完整的字段表如下：
![小杜的个人图床](http://src.xiaodu0.com/2024/07/04/b7d1e36fc4ccfd46566e907210c4e3d6.png)


### 1.3 评分指标

文档中给出的评分指标是：
> 测试集的每条数据同样包含共21个字段, 按照各字段难易程度划分总计满分36分。每个提取正确性的判定标准如下:
> 
> 1）对于答案唯一字段，将使用完全匹配的方式计算提取是否正确，提取正确得到相应分数，否则为0分
> 
> 2）对于答案不唯一字段，将综合考虑提取完整性、语义相似度等维度判定提取的匹配分数，最终该字段得分为 “匹配分数 * 该字段难度分数”
> 
> 每条测试数据的最终得分为各字段累计得分。最终测试集上的分数为所有测试数据的平均得分。


参考1.2处的字段分值表，我的思路是首先将分数占比最低，也是最容易拿到的字段先拿下，比如基本信息、客户意向等单值且唯一的字段。
这里通过完全匹配来计算提取是否正确，那么大体的思路就是，要符合完全匹配的规则，即`A===B` 这种情况，在Prompt设计中，要体现出这些字段的单值性、唯一性。

另一个评分指标是对于答案不唯一的字段，在赛题中只有两个：**预算明细和下一步跟进计划的具体事项。** 对于这类字段，一方面要保证匹配完整性，即能够尽可能多的匹配到字段相关的内容，同时，避免过多的匹配导致无相关的内容混入；另一方面，由于大模型在提取内容的时候，可能会对内容进行二次加工，容易产生语义偏差，在这里同样需要设计保证原文完整性的prompt。


## 二、Baseline研读

### 2.1 基本任务

在taks.1中我们的任务是30分钟速通Baseline，运行模型获取结果并且提交评分，在task.2中，我们需要做的基本任务是在熟悉了Baseline的流程之后，精读baseline，即baseline实现了什么？他是怎么实现的，以及baseline中给出的示例代码的理解。

首先，**baseline是针对赛题提出的一种利用大模型技术解决企业对话分场景提取内容的问题。**

其次，BaseLine没有涉及太多的底层技术，对于如何分割文本，如何从文本中提取出对应的信息，以及将文本转义输出都是大模型需要做的工作，而为了实现这一任务，我们需要做的就是给大模型合理的Prompt来指引大模型做出正确的答复。


### 2.2 代码分析
这一部分最重要的是理解baseline中给出的代码业务逻辑，以及各个部分的技术细节，以便对代码进行二次开发来获取更好的回复。

首先直接贴一下代码：
````Python
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import json
from tqdm import tqdm

#星火认知大模型Spark3.5 Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = ''
SPARKAI_API_SECRET = ''
SPARKAI_API_KEY = ''
#星火认知大模型Spark3.5 Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'

# prompt 设计
PROMPT_EXTRACT = """
你将获得一段群聊对话记录。你的任务是根据给定的表单格式从对话记录中提取结构化信息。在提取信息时，请确保它与类型信息完全匹配，不要添加任何没有出现在下面模式中的属性。

表单格式如下：
info: Array<Dict(
    "基本信息-姓名": string | "",  // 客户的姓名。
    "基本信息-手机号码": string | "",  // 客户的手机号码。
    "基本信息-邮箱": string | "",  // 客户的电子邮箱地址。
    "基本信息-地区": string | "",  // 客户所在的地区或城市。
    "基本信息-详细地址": string | "",  // 客户的详细地址。
    "基本信息-性别": string | "",  // 客户的性别。
    "基本信息-年龄": string | "",  // 客户的年龄。
    "基本信息-生日": string | "",  // 客户的生日。
    "咨询类型": string[] | [],  // 客户的咨询类型，如询价、答疑等。
    "意向产品": string[] | [],  // 客户感兴趣的产品。
    "购买异议点": string[] | [],  // 客户在购买过程中提出的异议或问题。
    "客户预算-预算是否充足": string | "",  // 客户的预算是否充足。示例：充足, 不充足
    "客户预算-总体预算金额": string | "",  // 客户的总体预算金额。
    "客户预算-预算明细": string | "",  // 客户预算的具体明细。
    "竞品信息": string | "",  // 竞争对手的信息。
    "客户是否有意向": string | "",  // 客户是否有购买意向。示例：有意向, 无意向
    "客户是否有卡点": string | "",  // 客户在购买过程中是否遇到阻碍或卡点。示例：有卡点, 无卡点
    "客户购买阶段": string | "",  // 客户当前的购买阶段，如合同中、方案交流等。
    "下一步跟进计划-参与人": string[] | [],  // 下一步跟进计划中涉及的人员（客服人员）。
    "下一步跟进计划-时间点": string | "",  // 下一步跟进的时间点。
    "下一步跟进计划-具体事项": string | ""  // 下一步需要进行的具体事项。
)>

请分析以下群聊对话记录，并根据上述格式提取信息：

**对话记录：**
```
{content}
```

请将提取的信息以JSON格式输出。
不要添加任何澄清信息。
输出必须遵循上面的模式。
不要添加任何没有出现在模式中的附加字段。
不要随意删除字段。

**输出：**
```
[{{
    "基本信息-姓名": "姓名",
    "基本信息-手机号码": "手机号码",
    "基本信息-邮箱": "邮箱",
    "基本信息-地区": "地区",
    "基本信息-详细地址": "详细地址",
    "基本信息-性别": "性别",
    "基本信息-年龄": "年龄",
    "基本信息-生日": "生日",
    "咨询类型": ["咨询类型"],
    "意向产品": ["意向产品"],
    "购买异议点": ["购买异议点"],
    "客户预算-预算是否充足": "充足或不充足",
    "客户预算-总体预算金额": "总体预算金额",
    "客户预算-预算明细": "预算明细",
    "竞品信息": "竞品信息",
    "客户是否有意向": "有意向或无意向",
    "客户是否有卡点": "有卡点或无卡点",
    "客户购买阶段": "购买阶段",
    "下一步跟进计划-参与人": ["跟进计划参与人"],
    "下一步跟进计划-时间点": "跟进计划时间点",
    "下一步跟进计划-具体事项": "跟进计划具体事项"
}}, ...]
```
"""

def read_json(json_file_path):
    """读取json文件"""
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return data


def write_json(json_file_path, data):
    """写入json文件"""
    with open(json_file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_completions(text):
    messages = [ChatMessage(
        role="user",
        content=text
    )]
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    return a.generations[0][0].text
    

def convert_all_json_in_text_to_dict(text):
    """提取LLM输出文本中的json字符串"""
    dicts, stack = [], []
    for i in range(len(text)):
        if text[i] == '{':
            stack.append(i)
        elif text[i] == '}':
            begin = stack.pop()
            if not stack:
                dicts.append(json.loads(text[begin:i+1]))
    return dicts
    
    
class JsonFormatError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def check_and_complete_json_format(data):
    required_keys = {
        "基本信息-姓名": str,
        "基本信息-手机号码": str,
        "基本信息-邮箱": str,
        "基本信息-地区": str,
        "基本信息-详细地址": str,
        "基本信息-性别": str,
        "基本信息-年龄": str,
        "基本信息-生日": str,
        "咨询类型": list,
        "意向产品": list,
        "购买异议点": list,
        "客户预算-预算是否充足": str,
        "客户预算-总体预算金额": str,
        "客户预算-预算明细": str,
        "竞品信息": str,
        "客户是否有意向": str,
        "客户是否有卡点": str,
        "客户购买阶段": str,
        "下一步跟进计划-参与人": list,
        "下一步跟进计划-时间点": str,
        "下一步跟进计划-具体事项": str
    }

    if not isinstance(data, list):
        raise JsonFormatError("Data is not a list")

    for item in data:
        if not isinstance(item, dict):
            raise JsonFormatError("Item is not a dictionary")
        for key, value_type in required_keys.items():
            if key not in item:
                item[key] = [] if value_type == list else ""
            if not isinstance(item[key], value_type):
                raise JsonFormatError(f"Key '{key}' is not of type {value_type.__name__}")
            if value_type == list and not all(isinstance(i, str) for i in item[key]):
                raise JsonFormatError(f"Key '{key}' does not contain all strings in the list")
                
                
if __name__ == "__main__":
    retry_count = 5 # 重试次数
    result = []
    error_data = []
    
    
    # 读取数据
    train_data = read_json("dataset/train.json")
    test_data = read_json("dataset/test_data.json")
    
    for index, data in tqdm(enumerate(test_data)):
        index += 1
        is_success = False
        for i in range(retry_count):
            try:
                res = get_completions(PROMPT_EXTRACT.format(content=data["chat_text"]))
                infos = convert_all_json_in_text_to_dict(res)
                infos = check_and_complete_json_format(infos)
                result.append({
                    "infos": infos,
                    "index": index
                })
                is_success = True
                break
            except Exception as e:
                print("index:", index, ", error:", e)
                continue
        if not is_success:
            data["index"] = index
            error_data.append(data)
    write_json("output.json", result)
````


首先通读一下代码，这段代码核心部分是一个函数名为`get_completions()`的函数，用于从给大语言模型发送指定的消息并且获取大模型的响应，作为返回值返回。

当然在此之前进行必要的配置导入，包括LLM模型的类，回调处理的类，定义ChatMessage结构的类以及json类。

随后，定义用于函数间共享的全局变量， 包括星火认知大模型调用秘钥信息，星火认知大模型Spark3.5 Max的domain值以及星火认知大模型Spark3.5 Max的URL值和最重要的prompt字符串。

由于整个业务的实现是以json来储存和读取数据的，因此定义了`read_json()`方法用于读取训练数据和测试数据，同时定义了`write_json()`用于写入结果数据。

又因为大模型总是不能直接输出python直接可读取的json格式，故使用函数`convert_all_json_in_text_to_dict()`对json数据进行提取，同时大模型偶尔会出现缺少字段的情况，故使用`check_and_complete_json_format`函数对大模型抽取的结果进行**字段格式的检查**以及**缺少的字段进行补全。**

在完成预定义所需要用到的函数之后，编写主程序，在主程序中定义了对于未能成果获取结果的数据的最大尝试次数、用于储存处理结果的列表、用于储存未能成功获取结果的文本的error_data列表。

随后，通过`read_json()`读取训练集和测试集，进入一个大循环，通过`enumerate()`将测试数据集构建为索引序列，并通过`tqdm()`进行遍历来展示进度条，在循环体内又嵌套一次循环，用于在失败时重试，通过`retry_count`来构造一个序列限制循环次数，当达到最大的重试次数时如果仍然没有成功，则将当前chat_info放入`error_data`中随后再处理。


在notebook中随后的部分是对错误的文本再次进行统一的尝试：
```python
if error_data:

    retry_count = 10 # 重试次数

    error_data_temp = []

    while True:

        if error_data_temp:

            error_data = error_data_temp

            error_data_temp = []

        for data in tqdm(error_data):

            is_success = False

            for i in range(retry_count):

                try:

                    res = get_completions(PROMPT_EXTRACT.format(content=data["chat_text"]))


                    infos = convert_all_json_in_text_to_dict(res)

                    infos = check_and_complete_json_format(infos)

                    result.append({

                        "infos": infos,

                        "index": data["index"]

                    })

                    is_success = True

                    break

                except Exception as e:

                    print("index:", index, ", error:", e)

                    continue

            if not is_success:

                error_data_temp.append(data)

        if not error_data_temp:

            break

    result = sorted(result, key=lambda x: x["index"])
# 保存结果
write_json("output.json", result)
```

在这段中首先判断是否有未成功的获取响应的文本，如果有的话，则定义最大尝试次数以及临时存放未成功获取数据的数组接着进入一个死循环：
```
if error_data_temp:

            error_data = error_data_temp

            error_data_temp = []
```

如果临时错误文本的变量不为空，则将其赋值给`error_data`，随后清空临时变量。
接着遍历未能成功获取响应的数据，首先标记`is_succeed=False`，表明暂无处理成功，随后再循环指定次数获取大模型回复，如果成功获取到响应则处理json数据，提取LLM输出文本中的json字符串，然后将其格式化为所需的格式，插入到result列表中，如果出现错误则打印错误信息并且跳到下一次循环，如果临时储存未成功响应的test的列表已经为空，则结束循环。最后排序结果，写入到output.json文件。

# Task.3 进阶BaseLine与代码精读

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


# 扩展：Encoder与Decode架构

大模型（如Transformer、GPT、BERT等）中的Encode与Decode架构是自然语言处理（NLP）和生成任务中常用的框架。

Encoder-Decoder架构的核心逻辑是：**将现实问题转化为数学问题，通过求解数学问题来得到现实世界的解决方案。**

![小杜的个人图床](http://src.xiaodu0.com/2024/07/09/0e0575ea0cee5d0c69a1b2d5af031e1a.png)

这其中的两个主要部分：
1. Encoder：将现实问题转为数学问题
2. Decoder：求解数学问题，并将数学问题转化为现实世界中的解决方案。

![小杜的个人图床](http://src.xiaodu0.com/2024/07/09/67d9c21b2094817ffe544d3b623aa318.png)


## 1.Encoder

Encoder即编码器，其主要作用是对输入信息转换成固定长度的表示，通常是**上下文向量或者隐状态。**

![小杜的个人图床](http://src.xiaodu0.com/2024/07/09/657daa0b28e402216333a66c7df62f21.png)


- 编码器的作用是**将输入序列转换成一个固定长度的上下文向量**。
- 通常使用**循环神经网络（RNN）或者其变体（LSTM、GRU）实现**
- 在每个时间步、编码器会读取输入序列的一个元素，并更新其隐藏状态。
- 编码完成后，最终的隐藏状态或者隐藏状态的某种变换被作用于上下文变量。



## 2.Decoder

**即Seq2Seq(Sequence-to-sequence)输入一个序列，输出另一个序列**
- **Seq2Seq（序列到序列）：** 强调模型的**目的**——将输入序列转换为输出序列。
- **Encoder-Decoder（编码器-解码器）：** 强调模型的**实现方法**——提供实现这一目的的具体方法或架构。
![小杜的个人图床](http://src.xiaodu0.com/2024/07/09/9f28e5a2f173ff02ddd023bdbd4e3b9e.png)
- 解码器的任务是从上下文向量中生成输出序列。
- 它也通常使用循环神经网络（RNN）来实现。
- 在每个时间步，解码器会基于上一个时间步的输出、当前的隐藏状态和上下文向量来生成当前时间步的输出。

## 3.Encoder与Decoder的应用

**Encoder-Decoder的典型应用是机器翻译。**
在Encoder-Decoder执行的过程中，编码器将源语言的句子编码成上下文向量，解码器则从该向量中生成目标语言的翻译。

具体来说，机器翻译的Encoder-Decoder包含六个步骤：
1. 源语言输入：将源语言的句子转换为词向量序列，作为编码器的输入
2. 编码器：通过循环神经网络处理源语言词向量，输出包含句子全部信息的上下文向量。
3. 上下文向量：作为解码器的初始输入，他固定长度地编码了源语言句子的整体含义
4. 解码器：基于上下文向量，逐步生成目标语言的词序列，形成翻译结果
5. 目标语言输出：解码器生成的词序列构成最终翻译的目标语言句子
6. 训练与优化：通过比较模型生成的翻译与真实目标的句子，优化模型参数以提高翻译准确性。

**另一份经典的Encoder-Decoder应用是语言识别任务。**
语言识别任务中，编码器将音频信号转为特征表示，解码器则从这些特征中生成文本转录。
语音识别任务中的Encoder-Decoder的六个步骤：
1. 音频信号输入：将原始的音频信号进行预处理，准备送入编码器进行特征提取
2. 编码器处理：编码器接受预处理后的音频，逐帧提取声学特征，转换为高维特征向量序列。
3. 特征表示：解码器输出的特征向量捕捉了音频中的关键信息，为解码器提供输入。
4. 解码器生成：解码器根据特征向量序列和语言模型，逐步预测并生成对应的文本转录。
5. 文本转录输出：解码器完成预测，输出最终的文本转录结果。
6. 训练与优化：- 训练与优化：通过比较生成的文本转录与真实标签，优化模型参数以提高识别准确率。