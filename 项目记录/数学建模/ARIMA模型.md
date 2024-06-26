
## ARIMA的应用

ARIMA模型用于对时间序列进行分析和预测，例如对数据趋势的统计展示和对未来时间的预测。

## 平稳性与差分法

### 平稳性

平稳性就是要求经由样本时间序列所得到的拟合曲线，在未来一段时间内仍然有能够顺着现有的形态“惯性”的延续下去。

平稳性则要求时间序列的 **均值**和**方差** 不发生明显变化。应当是不明显的变化，而非不能用有变化。
在使用ARIMA模型时，要首先检验数据的平稳性来确定是否能建模。

### 严平稳与弱平稳

**严平稳**：严平稳表示的分布**不随时间的改变而改变**。
例如：白噪声（正态）。无论怎么取，都是期望为0，方差为1。

**弱平稳**：弱平稳表示期望与相关系数（依赖性不变）
即未来的数据需要依赖过去的数据，所以需要依赖性。(未来某时刻的数据Xt依赖于过去的信息)

### 差分法检验

**差分法检验检验原始数据在t时刻与t-1时刻的数据的差值，将这些差值组成新的序列则形成一阶差分。**

通过差分法可以得出每一个t时刻的数据与t-1时刻的数据的差值，即可以得出整个数据的变化程度。

Python实现：
```
# 一阶差分
import pandas
import matplotlib.pyplot as plt

data = pandas.read_csv("downloads/96723/data1.csv");

diff = data['Amount'].diff()
time = data["Time"]

plt.plot(diff.values)
```

一阶差分后的数据分布：
![小杜的个人图床](http://src.xiaodu0.com/2024/04/06/6f619e292457ebab81396debac22350f.png)

图中在第150000个数据左右出现较大的波动，是因为没有在差分之前对数据进行校验和过滤。

上图使用的数据集是阿里天池中的公开数据集，数据内容是2020年9月1日至9月2日的某商品交易额，是一个标准的时间序列。

原数据的条形图：
![小杜的个人图床](http://src.xiaodu0.com/2024/04/06/bfbc630326cf460e1ab33acbd3d1a537.png)


 在一阶差分的基础上，对一阶差分得到的数据再次进行一次差分即可得到二阶差分，一般来说对于数据的平稳性检验只需要一阶差分和二阶差分两种即可。


## 自回归模型（AR）

自回归模型即通过变量过去时间点的数据来预测未来时间点的数据。

### 特点

- **描述当前值与历史值之间的关系，用变量的历史事件数据对自身进行预测，**
- **自回归模型必须满足平稳性要求**
- ![小杜的个人图床](http://src.xiaodu0.com/2024/04/06/6e8dea75b33cc34bd80ebc1c0e253d76.png)
- ![小杜的个人图床](http://src.xiaodu0.com/2024/04/06/79f81c0e09d22009267094b431ef9fb5.png)

**p阶：指时间序列的间隔，即步长。例如2阶自回归过程即指在时间序列间隔步长为2进行自回归检测。**

例如，一份以分钟为单位的时间序列，3阶自回归即指时间的间隔为3分钟，将第4分钟与第一分钟比较，第7分钟与第4分钟比较，以此类推。

在AR模型中重要的参数是p，参数为P的自回归模型称为P阶自回归模型，记作AR（P）。

由AR模型的定义式可知，**预测值Yt的值是由前面的Yt-1+Yt-p+Yt-2p......Y1项的加权以及随机扰动项（白噪声）决定的**。

其中，**白噪声序列是指序列中的任何两个时点都不具有相关性，没有任何可以供利用的动态规律，也就是说，不能通过历史的数据来对未来进行预测。**

### 建模过程

一般的自回归模型的建模过程是：

1. **对序列进行白噪声检验**，如果序列是白噪声，则建模结束（不适用AR模型），如果不是白噪声，接着进行步骤二
2. **平稳性检验。**如果序列是平稳序列，继续步骤三，否则对序列进行平稳处理，处理完之后再回到步骤一。
3. **参数估计** 。对于平稳序列的建模，进行参数估计（**这里的参数指P，即阶数**），转步骤四。
4. **检验适用性**。得到参数之后对参数进行适用性检验，如果参数适用，则对模型进行拟合，接着对未来数据进行预测，如果参数不适用，则回到步骤三。

### AR模型的判断

对于观测到**序列为非白噪声，且经过平稳性检验为平稳序列**之后，常根据**自相关系数**（Autocurrelation Function,ACF）和**偏自相关系数**(Partial Autocurrelation Function,PACF)进行模型识别。

（***这里的自相关系数貌似应该叫做自相关函数，偏自相关函数也是，网上查了一下说自相关系数是指自身不同时期的相关程度，而偏自相关函数是由自相关系数构成的序列，偏自相关系数函数是自偏自相关系数构成的序列，没太搞明白，有没有数学大佬指点一下。***）

对于一个非白噪声、平稳的时间序列，如果同时满足：

1. **ACF具有拖尾性**（ACF(k)不会在某个k值之后恒等于0，图像中表象为y值不会为0或者在x轴上下波动）
2. **PACF具有截尾性**（PACF(K)会在某个k值之后恒等于0或者在0的上下波动，图像表现为y值为0，或者在x轴上下波动。）
3. 
则可以根据自相关系数ACF和偏自相关系数PACF进行模型识别。

首先计算ACF和PACF，将二者分别绘制为条形图，查看ACF是否有拖尾性和APCF是否有截尾性，然后根据图像表现确定参数P的值。

例如上方商品的时间序列数据，在建模之前要对序列进行白噪声和平稳性检验，然后计算其自相关系数和偏自相关系数，最后检测适用性和模型拟合，在实际操作之前先对相关要用到的知识点记录一下。

### 白噪声检验

**对序列进行白噪声检验通常通过Ljung-Box检验**，即LB检验。

**LB检验是对随机性的检验**，**或者说是对时间序列是否有滞后相关性的检验一种统计检验**

**LB检验则是基于一系列滞后阶数，判断序列总体的相关性或者说随机性是否存在**。


LB检验一般有两个假设，分为**原假设和备择假设**。

原假设（H0）一般为：原本的数据都是独立的，即总体的相关系数为0，能观察到的某些相关仅仅产生于随机抽样的误差，即原假设为序列为白噪声。

备择假设（Ha）一般为：原本的数据不是独立的，即至少存在某个K阶滞后的相关系数使得统计量服从自由度为h的卡方分布。

如果接受原假设则意味着序列是白噪声，如果拒绝原假设则意味着该序列存在相关性。

### 平稳性检验

**平稳性检验一般通过ADF检验进行。**

ADF检验（Augmented Dickey-Fuller test）是一种用于检测时间序列数据是否存在单位根的统计方法，也称为单位根检验。单位根的存在意味着时间序列数据是非平稳的，而平稳性是许多时间序列分析的前提条件。因此，ADF检验在时间序列分析中具有重要地位。

ADF检验就是判断序列是否存在单位根：**如果序列平稳，就不存在单位根**；否则，就会存在单位根。所以，ADF检验的 H0 假设就是存在单位根，**如果得到的显著性检验统计量小于三个置信度（10%，5%，1%），则对应有（90%，95，99%）的把握来拒绝原假设。**



### 自相关函数和偏自相关函数

自相关系数：**当研究一个变量受另一个变量影响时，若同时考虑其他变量的影响，此时分析变量之间的关系强弱程度称为相关系数。**

偏自相关系数：**若研究一个变量受另一个变量影响时，其他的影响变量要视作常数，即暂时不考虑其他因素影响，单独考虑这两个变量的关系程度，此时分析变量之间的关系用的是偏相关系数**。

拖尾与截尾：**拖尾是指序列以指数率单调递减或震荡衰减，而截尾指序列从某个时间点变得非常小。**
![小杜的个人图床](http://src.xiaodu0.com/2024/04/06/e69548e7d88ce94bc5268bbfdc743a59.png)


出现以下情况，通常视为（偏）自相关系数d阶截尾：

1. **在最初的d阶明显大于2倍标准差范围**
2. **之后几乎95%的（偏）自相关系数都落在2倍标准差范围以内**
3. **且由非零自相关系数衰减为在零附近小值波动的过程非常突然**

出现以下情况，通常视为（偏）自相关系数拖尾：

1. **如果有超过5%的样本（偏）自相关系数都落在两倍标准差范围之外**
2. **或者是由显著非0的（偏）自相关系数衰减为小值波动的过程比较缓慢或非常连续**

### Python实现AR模型的判断

在阿里天池实验室的NoteBook中使用上方的商品交易额数据作为时间序列。

#### LB检验

首先通过LB检验确定序列是否为白噪声，LB检验使用`statsmodels`库，因此需要先安装statsmodels:
```python
pip install statsmodels
```


导入用户LB检验的函数：
```python
from statsmodels.stats.diagnostic import accor_ljungbox as lb_test
```

由于数据量过大，对数据进行切片，取前10000条数据：
```python
amount = data["Amount"][0:9999]
```

对前10000条数据进行LB检验，其中参数lags为滞后值：
```python
lb_test(amount,lags=15)
```

结果：
![小杜的个人图床](http://src.xiaodu0.com/2024/04/06/840100e97df2cde625eaddc8c7150bf1.png)

由白噪声的备择假设：原本的数据不是独立的，即至少存在某个K阶滞后的相关系数使得统计量服从自由度为h的卡方分布。

当滞后系数为15时，统计量为25.99...，此时P值为0.03小于0.05因此可以拒绝原假设，序列不是白噪声。

### ADF检验


### 限制

- **自回归模型必须自身的数据进行预测**
- **必须满足具有平稳性（参考：严平稳、弱平稳）**
- **‘必须有自相关性，如果自相关系数小于0.5则不宜采用。**
- **自回归模型只适合预测与自身前期相关的现象**。


## 移动平均模型

- **移动平均模型关注自回归模型中误差项的累加。**
- **移动平均法能够有效的消除预测中的随机波动。**
- ![小杜的个人图床](http://src.xiaodu0.com/2024/04/06/7f349d1f74185797629cf7a72f9a5fe0.png)

