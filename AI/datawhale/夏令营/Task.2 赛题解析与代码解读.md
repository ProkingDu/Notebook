
# 一、赛题解析

## 1.1 赛题说明

本次baseline的赛题背景是：
> 在数字化时代，企业积累了大量对话数据，这些数据不仅是交流记录，还隐藏着宝贵的信息。群聊对话分角色要素提取是企业营销和服务的重要策略，通过分析这些数据，企业可以更好地理解客户需求，提供个性化服务，提升客户满意度和商业价值。

赛事任务：
> 从给定的<客服>与<客户>的群聊对话中，提取出指定的字段信息，具体待提取的字段信息见下文。

参赛选手需**基于讯飞星火大模型****Spark Max**完成任务，可使用大模型微调。

## 1.2 任务解析

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


## 1.3 评分指标

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


# 二、Baseline研读

## 2.1 基本任务

在taks.1中我们的任务是30分钟速通Baseline，运行模型获取结果并且提交评分，在task.2中，我们需要做的基本任务是在熟悉了Baseline的流程之后，精读baseline，即baseline实现了什么？他是怎么实现的，以及baseline中给出的示例代码的理解。

首先，**baseline是针对赛题提出的一种利用大模型技术解决企业对话分场景提取内容的问题。**

其次，BaseLine没有涉及太多的底层技术，对于如何分割文本，如何从文本中提取出对应的信息，以及将文本转义输出都是大模型需要做的工作，而为了实现这一任务，我们需要做的就是给大模型合理的Prompt来指引大模型做出正确的答复。


## 2.2 代码分析
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

