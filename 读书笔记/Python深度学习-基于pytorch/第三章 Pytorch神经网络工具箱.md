
## 一、神经网络的核心组件

神经网络看起来很复杂，但是他的核心部分或者组件并不多，在定义这些基本组件之后就基本确定了一个神经网络。
这些核心组件如下：
1. 层：层是神经网络的基本结构，他的作用是将输入张量转为输出张亮。
2. 模型：由层构成的网络
3. 损失函数：参数学习的目标函数，通过最小化损失函数来学习各种参数
4. 优化器：如果使损失函数最小时，就会涉及到优化器。

他们的关系如图所示：
![小杜的个人图床](http://src.xiaodu0.com/2024/05/29/d35aa4811ebed5df23fecd6d798a22eb.jpg)


多个层连接在一起构成了一个模型或者网络，输入数据通过这个模型转为预测值。预测值与真实值共同构成损失函数的输入，损失函数输出损失值，该损失值用于衡量预测值与目标结果的匹配或者相似程度。优化器利用损失值更新权重参数，目标是使损失函数值越来越小。这是一个循环过程，点那个损失值达到一个阈值或者循环次数达到指定次数时，循环结束。

## 二、构建神经网络的主要工具

构建神经网络的主要工具如图所示：
![小杜的个人图床](http://src.xiaodu0.com/2024/05/29/62c4a702ef3460e21d07e60ffcc79046.jpg)

使用Pytorch构建模型的方法有三种：
1. 继承nn.Module基类构建模型
2. 使用nn.sequential按层顺序构建模型
3. 继承nn.Module基类构建模型，之后再使用相关的容器模型，例如（nn.sequential、nn.ModuleList、nn.ModuleDict等）进行封装。
他们各有优劣，其中nn.Module最常用，nn.sequential比较简单，最后一种非常灵活，但是复杂一些。

### 2.1继承nn.Module基类构建模型

通过这种方式构建模型，有两个基本步骤：
1. 继承nn.Module 在__init__方法中实例化父类，并把需要用到的层放在其中。
2. 定义forward方法实现模型的正向传播

依赖模块：
```python
import torch
from torch import nn 
from torch.nn import torch.functional as F
```

代码示例：
```python
class MyModel(nn.Module):  
    # 定义构造方法，参数列表与用到的层所需的参数一致。  
    def __init__(self,in_dim,n_hidden_1,n_hidden_2,out_dim):  
        # 实例化父类构造方法  
        super(MyModel,self).__init__()  
        # 加载层  
        self.flatten = nn.Flatten()  
        self.linear1 = nn.Linear(in_dim,n_hidden_1)  
        self.bn1=nn.BatchNorm1d(n_hidden_1)  
        self.linear2 = nn.Linear(in_dim,n_hidden_1)  
        self.bn2 = nn.BatchNorm1d(n_hidden_2)  
        self.out = nn.Linear(n_hidden_2,out_dim)  
  
    # 定义正向传播方法,接收一个输入张量x  
    def forward(self,x):  
        x=self.flatten(x) # 展开为向量  
        x=self.linear1(x)  # 全连接层  
        x=self.bn1(x) # 批量均一化  
        x= F.relu(x)  # 损失函数  
        x=self.bn2(x)  
        x=F.relu(x)  
        x=self.out(x)  
        x=F.softmax(x,dim=1)  # 激活函数  
        return x
```

上述代码构建的网络模型如下图所示：
![小杜的个人图床](http://src.xiaodu0.com/2024/05/29/02bcfee0636b9d37ae81d1314c494b98.jpg)

其中接受一个28\*28的图像，并将图像展开为向量，定义两个layer，每个layer包括一个全连接层，一个批量归一化层，激活函数都是Relu，输出层的激活函数为softmax。

接下来实例化一个模型查看模型结构：
```python
in_dim,n_hidden_1,n_hidden_2,out_dim = 28*28,3090,100,10  
mymodel = MyModel(in_dim,n_hidden_1,n_hidden_2,out_dim)  
print(mymodel)
```

控制台输出：
```python
MyModel(
  (flatten): Flatten(start_dim=1, end_dim=-1)
  (linear1): Linear(in_features=784, out_features=3090, bias=True)
  (bn1): BatchNorm1d(3090, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (linear2): Linear(in_features=784, out_features=3090, bias=True)
  (bn2): BatchNorm1d(100, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (out): Linear(in_features=100, out_features=10, bias=True)
)
```



### 1.2 通过nn.sequential 构建模型

构建如1.1中相同的网络，通过nn.sequential无需重写forward()函数，因为在其内部已经定义了正向传播函数。

但是 **由于nn.sequential中的函数是按照先后顺序定义的，所以必须保证前一层的输出是后一层的输入。**

代码：
```python
import torch  
from torch import nn  
from torch.nn import functional as F  
  
  
in_dim,n_hidden_1,n_hidden_2,out_dim = 28*28,3090,100,10  
  
mymodule = nn.Sequential(  
    nn.Flatten(),  
    nn.Linear(in_dim,n_hidden_1),  
    nn.BatchNorm1d(n_hidden_1),  
    nn.ReLU(),  
    nn.Linear(in_dim,n_hidden_1),  
    nn.BatchNorm1d(n_hidden_1),  
    nn.ReLU(),  
    nn.Softmax(dim=1)  
)  
  
print(mymodule)
```


控制台输出：
```python
Sequential(
  (0): Flatten(start_dim=1, end_dim=-1)
  (1): Linear(in_features=784, out_features=3090, bias=True)
  (2): BatchNorm1d(3090, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (3): ReLU()
  (4): Linear(in_features=784, out_features=3090, bias=True)
  (5): BatchNorm1d(3090, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (6): ReLU()
  (7): Softmax(dim=1)
)
```

上述只是其中一种方法，另一种方法是通过`add_module()`方法来添加模型，并且通过此方法可以为每个模型命名。

`add_module(module_name,module)`的参数：
- module_name  定义模型别名
- module 具体的模型

代码示例：
```python
mymodule1 = nn.Sequential()  
mymodule1.add_module("展开张亮",nn.Flatten())  
mymodule1.add_module("全连接层1",nn.Linear(in_dim,n_hidden_1))  
mymodule1.add_module("批量归一化1",nn.BatchNorm1d(n_hidden_1))  
mymodule1.add_module("损失函数",nn.ReLU())  
mymodule1.add_module("全连接层2",nn.Linear(in_dim,n_hidden_2))  
mymodule1.add_module("批量归一化2",nn.BatchNorm1d(n_hidden_2))  
mymodule1.add_module("损失函数2",nn.ReLU())  
mymodule1.add_module("激活函数",nn.Softmax(dim=1))  
print(mymodule1)
```

控制台输出

```python
Sequential(
  (展开张亮): Flatten(start_dim=1, end_dim=-1)
  (全连接层1): Linear(in_features=784, out_features=3090, bias=True)
  (批量归一化1): BatchNorm1d(3090, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (损失函数): ReLU()
  (全连接层2): Linear(in_features=784, out_features=100, bias=True)
  (批量归一化2): BatchNorm1d(100, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (损失函数2): ReLU()
  (激活函数): Softmax(dim=1)
)
```

使用collections 模块下的 `OrderedDict` 类也可以构建具有命名顺序的模型：
```python
import torch
from torch import nn
from collections import OrderedDict
mymodule2 = nn.Sequential(OrderedDict([  
("展开张亮",nn.Flatten()),  
("全连接层1",nn.Linear(in_dim,n_hidden_1)),  
("批量归一化1",nn.BatchNorm1d(n_hidden_1)),  
("损失函数",nn.ReLU()),  
("全连接层2",nn.Linear(in_dim,n_hidden_2)),  
("批量归一化2",nn.BatchNorm1d(n_hidden_2)),  
("损失函数2",nn.ReLU()),  
("激活函数",nn.Softmax(dim=1))  
]))  
print(mymodule2)
```

运行结果：
```python
Sequential(
  (展开张亮): Flatten(start_dim=1, end_dim=-1)
  (全连接层1): Linear(in_features=784, out_features=3090, bias=True)
  (批量归一化1): BatchNorm1d(3090, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (损失函数): ReLU()
  (全连接层2): Linear(in_features=784, out_features=100, bias=True)
  (批量归一化2): BatchNorm1d(100, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (损失函数2): ReLU()
  (激活函数): Softmax(dim=1)
)
```

### 1.3 通过nn.Module基类结合应用模型容器来构建模型

当模型的结构比较复杂时，可以应用模型容器对模型的部分结构进行封装来增强模型的可读性，或者减少代码量。

例如，当构建的模型有多个层，每个层中用到了不同的模块时，通过模型容器将这些模块封装成一个层，然后将这个层组合在一起构建模型。

例如：
```python
from torch import nn  
from torch.nn import functional as F  
from collections import OrderedDict

class Model_lay(nn.Module):  
    def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):  
        super(Model_lay, self).__init__()  
        self.flatten = nn.Flatten()  
        self.layer1 = nn.Sequential(nn.Linear(in_dim, n_hidden_1),  
                                    nn.BatchNorm1d(n_hidden_1))  
        self.layer2 = nn.Sequential(nn.Linear(in_dim, n_hidden_1),  
                                    nn.BatchNorm1d(n_hidden_1))  
        self.out = nn.Sequential(nn.Linear(n_hidden_2,out_dim))  
  
    def forward(self,x):  
        x = self.flatten(x)  
        x = F.relu(self.layer1(x))  
        x = F.relu(self.layer2(x))  
        x = F.softmax(self.out(x))  
  
in_dim,n_hidden_1,n_hidden_2,out_dim = 28*28,3090,100,10  
model_lay = Model_lay(in_dim,n_hidden_1,n_hidden_2,out_dim)  
print(model_lay)
```

运行结果：
```python
Model_lay(
  (flatten): Flatten(start_dim=1, end_dim=-1)
  (layer1): Sequential(
    (0): Linear(in_features=784, out_features=3090, bias=True)
    (1): BatchNorm1d(3090, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  )
  (layer2): Sequential(
    (0): Linear(in_features=784, out_features=3090, bias=True)
    (1): BatchNorm1d(3090, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  )
  (out): Sequential(
    (0): Linear(in_features=100, out_features=10, bias=True)
  )
)
```

## 三、自定义网络模块

通过上面的实例对构建神经网络的主要工具有所了解，包括：
1. 通过nn.Module基类构建模型
2. 通过nn.Sequential()构建模型
3. 通过nn.Module()基类构建模型结合容器来将模块封装为层

其中包括如下工具：
1. add_module(module_name,module) 向nn.Sequential对象添加模块
2. OrderedDict()  有序的模块容器，构建具有键值对的模块组合
3. ModuleList()  类似列表的模型容器
4. nn.ModuleDict()  类似字典的模型容器

提及到的模块：
1. nn.Flatten()  用于将输入的多维数据展平成一维。
2. nn.Linear(in_dim,n_hidden) 定义一个全连接层，接收in_dim大小的输入即向量的维度，并将其映射到n_hidden大小的输出空间。
3. nn.BatchNorm1d(n_hidden) 定义一个批量归一化层，输入标准为一个全连接层的输出，即隐藏层的输出，对隐藏层的输出进行标准化，以确保数据分布的稳定性，批量归一化有助于加速模型训练，防止梯度消失或梯度爆炸，并提高模型的泛化能力。
4. nn.functional.relu(x) 接受一个张量x作为输入，对其应用RELU激活函数，产生激活后的输出张量。
5. nn.functional.softmax() 接受一个张量作为输入，并应用softmax()函数，将输出转为概率分布。

接下来尝试利用nn工具来构建一个经典的神经网络模型：ResNet18（深度残差网络）

### 3.1 问题引入

在深度学习中，网络的“深度”（即层数）通常与模型的能力成正比。然而，随着网络深度的增加，一些问题也随之出现，最突出的是梯度消失/爆炸问题。这使得深层网络难以训练。

传统的深度神经网络试图学习目标函数 ( H(x) )，但是在ResNet中，每个网络层实际上学习的是一个残差函数 ( F(x) = H(x) - x )。然后，这个残差结果与输入 ( x ) 相加，形成 ( H(x) = F(x) + x )。**这一机制使得网络更容易学习身份映射，进而缓解了梯度消失问题。**
### 3.2 深度学习与梯度消失

梯度消失问题发生在神经网络的反向传播过程中，具体表现为网络中某些权重的梯度**接近或变为零**。这**导致这些权重几乎不会更新，从而阻碍了网络的训练。**

导致梯度消失的现象主要有三个原因：

1. ***激活函数***
使用Sigmoid或者Tanh等饱和激活函数时，其导数在两端极小，这很容易导致梯度消失。

思考：**导数的意义是变量的变化率，而梯度指向函数值增加最快的方向。而当导数在两端极小时，函数值增加接近于0，这时候就产生了梯度消失的问题。**



2. ***初始化方法***

权重初始化不当也可能导致梯度消失。例如，如果初始化权重过小，那么激活函数的输出和梯度都可能非常小。

3. ***网络深度***

网络越深，梯度在反向传播过程中经过的层就越多，导致梯度消失问题更加严重。

解决梯度消失有三种主要方案：
- **使用ReLU激活函数**：ReLU（Rectified Linear Unit）激活函数能够缓解梯度消失。
- **合适的权重初始化**：如He初始化或Glorot初始化。
- **使用短接结构（Skip Connections）**：这是ResNet解决梯度消失问题的核心机制。


### 3.3 残差块基础

**残差块（Residual Blocks）是深度残差网络中的基本构建单元。** 通过使用残差块，ResNet有效地解决了梯度消失问题，并能训练极深的网络。


残差块由如下基本结构组成：

- 卷积层：用于特征提取，在残差块中一般使用3\*3的卷积层。
- 批量归一化（Batch Normalization）：用于加速训练和改善模型泛化。
- 激活函数：通常使用ReLU。
- 短接连接（Skip Connection）：直接连接输入和输出。

![小杜的个人图床](http://src.xiaodu0.com/2024/06/02/18ffa854181cf10b05daca71f160a4a4.jpg)

由此基本结构，可以通过nn工具来构建一个基础残差块（图a）：
```python
from torch import nn  
from torch.nn import functional as F  
  
  
class ResidualBlock(nn.Module):  
    def __init__(self, in_channel, out_channel, stride):  
        super(ResidualBlock, self).__init__()  
        # 定义3x3卷积层  
        self.conv1 = nn.Conv2d(in_channel, out_channel, kernel_size=3, stride=stride)  
        # 定义批量归一化层，将上一次的输出归一化  
        self.bn1 = nn.BatchNorm1d(out_channel)  
        # 第二个3*3卷积层  
        self.conv2 = nn.Conv2d(out_channel, out_channel, kernel_size=3, stride=stride)  
        # 第二个批量归一化层  
        self.bn2 = nn.BatchNorm1d(out_channel)  
  
    # 正向传播函数  
    def forward(self, x):  
        # 卷积  
        output = self.conv1(x)  
        # 批量归一化  
        output = self.bn1(output)  
        # 激活函数  
        output = F.relu(output)  
  
        # 第二次卷积和批量归一化以及激活函数  
        res = x + F.relu(self.bn2(self.conv2(output)))  
        return res
```


在图b所示的网络结构中，加入了在进行最后的激活函数处理时通过一个1x1的卷积层处理，目的是使输入与输出形状一致，通过1x1的卷积层调整通道和分辨率。

图b的残差块代码实现：
```python
class ResidualDownBlock(nn.Module):  
    def __init__(self,in_channels,out_channels,stride):  
        super(ResidualDownBlock,self).__init__()  
        # 定义3x3卷积层  
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride[0],padding=1)  
        # 定义批量归一化层，将上一次的输出归一化  
        self.bn1 = nn.BatchNorm1d(out_channels)  
        # 第二个3*3卷积层  
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=stride[0],padding=1)  
        # 第二个批量归一化层  
        self.bn2 = nn.BatchNorm1d(out_channels)  
  
        # 调整通道和分辨率  
        self.extra = nn.Sequential(  
            nn.Conv2d(in_channels,out_channels,kernel_size=1,stride=stride[0],padding=0),  
            nn.BatchNorm2d(out_channels)  
        )  
  
    def forward(self,x):  
        # 原始数据处理  
        extra_x = self.extra(x)  
  
        # 第一次卷积  
        output = self.conv1(x)  
        # 批量归一化  
        output = self.bn1(output)  
        # 激活函数  
        output = F.relu(output)  
  
        # 第二次卷积和批量归一化以及激活函数  
        res = extra_x + F.relu(self.bn2(self.conv2(output)))  
        return res
```

### 3.4 Resnet18网络

一个标准的ResNet模型由多个残差块组成，通常开始于一个普通的卷积层和池化层，用于进行初步的特征提取。接下来是一系列的残差块，最后是全局平均池化层和全连接层。

**架构组成：**
- 初始卷积层：用于初步特征提取。
- 残差块组（Residual Blocks Group）：包含多个残差块。
- 全局平均池化（Global Average Pooling）：减小维度。
- 全连接层：用于分类或其他任务。

Resnet18结构图：

![小杜的个人图床](http://src.xiaodu0.com/2024/06/02/6d0ba2e437878e55528e78a0ca949c68.png)
#### 3.4.1. 初始卷积层

在进入深度残差网络的主体结构之前，第一层通常是一个初始卷积层。这个卷积层的主要任务是**对输入图像进行一定程度的空间下采样（Spatial Downsampling）和特征抽取。**

![小杜的个人图床](http://src.xiaodu0.com/2024/06/02/e407e85324c6ac03022b2dbb533343b3.png)

**功能和作用**

1. **空间下采样（Spatial Downsampling）**: 初始卷积层通常具有较大的卷积核和步长（stride），用于减少后续层需要处理的空间维度，从而降低计算复杂度。
2. **特征抽取**: 初始卷积层能够抓取图像的基础特征，如边缘、纹理等，为后续的特征抽取工作打下基础。

在ResNet-18和ResNet-34中，这一初始卷积层通常由一个`7x7`大小的卷积核、步长（stride）为`2`和填充（padding）为`3`组成。这个层后面通常还会跟随一个批量归一化（Batch Normalization）层和ReLU激活函数。

对应的代码：
```python
self.initConv = nn.Conv2d(3,64,kernel_size=7,padding=3,stride=2)  
self.initBn = nn.BatchNorm2d(64)  
self.initRelu = nn.ReLU(inplace=True)
```

这里使用7x7的卷积核是因为，一个大的卷积核可以在相同数量的参数下，提供更大的感受野（Receptive Field），从而更有效地捕获图像的全局信息。

初始卷积层在整个ResNet架构中扮演着非常重要的角色。它不仅完成了对输入图像的基础特征抽取，还通过空间下采样减轻了后续计算的负担。这些设计细节共同使得ResNet能在保持高性能的同时，具有更低的计算复杂度。

#### 3.4.2 残差模块组

在定义初始的卷积层之后，随后的架构是残差模块组，这一模块中包含多个残差块。这些残差块组成了ResNet架构中的主体，负责高级特征的抽取和传递。

**功能和作用**：

1. **特征抽取**: 每个残差块组负责从其前一组中提取的特征中提取更高级的特征。
2. **非线性性能增强**: 通过残差链接，每个残差块组能够学习输入与输出之间的复杂非线性映射。
3. **避免梯度消失和爆炸**: 残差块组内的Skip Connection（跳过连接）能够更好地传递梯度，有助于训练更深的网络。

根据残差网络结构图来构建这里的残差模块组：
- 第一组可能包括2个残差块，用64个输出通道。
- 第二组可能包括2个残差块，用128个输出通道。
- 第三组可能包括2个残差块，用256个输出通道。
- 第四组可能包括2个残差块，用512个输出通道。

代码：
```python
# 构建残差模块组  
self.layer1 = nn.Sequential(  
    ResidualBlock(64,64,1),  
    ResidualBlock(64,64,1)  
) # 第一组  
self.layer2 = nn.Sequential(  
    ResidualDownBlock(64,128,(2,1)),  
    # 先使用含有1x1卷积层的块来调整通道，从64到128  
    ResidualBlock(128,128,1)  
) # 第二组  
self.layer3 = nn.Sequential(  
    ResidualDownBlock(128,256,(2,1)),  
    ResidualBlock(256,256,1)  
) # 第三组  
self.layer3 = nn.Sequential(  
    ResidualDownBlock(256, 512, (2, 1)),  
    ResidualBlock(512, 512)
)
```

在代码中除layer1之外， 后面的每一层都首先通过之前定义的含有1x1卷积层的残差块网络首先处理，这是为了会减小特征图的尺寸（即进行下采样），而增加输出通道数。这样做可以保证模型的计算效率，同时能抓住更多层次的特征。

**残差块组是ResNet架构中最核心的部分，通过逐层抽取更高级的特征并通过残差连接优化梯度流动，这些设计使得ResNet模型能够有效并且准确地进行图像分类以及其他计算机视觉任务。**


#### 3.4.3 全局平均池化

在进行了四层的残差块组进行特征抽取和非线性映射之后，ResNet通常使用全局平均池化层（Global Average Pooling，简称GAP）作为网络的最后一个卷积层。与传统的全连接层相比，全局平均池化有几个显著优点。


1. **降维**: 全局平均池化层将每个特征图（Feature Map）缩减为一个单一的数值，从而显著减小模型参数和计算量。
2. **防止过拟合**: 由于其简单性和少量的参数，全局平均池化有助于防止模型过拟合。
3. **改善泛化能力**: 简化的网络结构能更好地泛化到未见过的数据。

全局平均池化层简单地计算每个特征图的平均值。假设有一个形状为`(batch_size, num_channels, height, width)`的特征图，全局平均池化将输出一个形状为`(batch_size, num_channels)`的张量。

```python
# 全局平均池化  
self.avg_pool = nn.AdaptiveAvgPool2d((1,1))
```

#### 3.4.4 全连接层

在全局平均池化（GAP）之后，ResNet架构通常包含一个或多个全连接层（Fully Connected Layer）。全连接层在ResNet中的主要目的是为了进行分类或者回归任务。

1. **分类或回归**: 全连接层的主要任务是根据前层特征进行分类或回归。
2. **增加模型复杂度**: 相比GAP，全连接层可以增加模型的复杂度，从而拟合更复杂的函数。
3. **特征整合**: 全连接层能够整合前面各层的信息，输出一个固定大小的特征向量。

全连接层通常接收全局平均池化层输出的平坦化（flattened）向量，并通过一系列线性变换与激活函数生成输出。例如，在分类问题中，全连接层通常输出一个与类别数相等的节点。

**全连接层之后通常会接一个激活函数，如ReLU或者Softmax，以引入非线性。有时也会使用Dropout层来防止过拟合，尤其是在全连接层的节点数较多时。**

例如，将输出的512维向量转化为10维向量：

```python
self.fc = nn.Linear(512,10)
```

#### 3.4.5 模型构建

基于上述的模型结构和代码，构建出完成的Resnet18模型：
```python
import torch  
from torch import nn  
from torch.nn import functional as F  
  
  
class ResidualBlock(nn.Module):  
    def __init__(self, in_channel, out_channel, stride):  
        super(ResidualBlock, self).__init__()  
        # 定义3x3卷积层  
        self.conv1 = nn.Conv2d(in_channel, out_channel, kernel_size=3, stride=stride, padding=1)  
        # 定义批量归一化层，将上一次的输出归一化  
        self.bn1 = nn.BatchNorm2d(out_channel)  
        # 第二个3*3卷积层  
        self.conv2 = nn.Conv2d(out_channel, out_channel, kernel_size=3, stride=1, padding=1)  
        # 第二个批量归一化层  
        self.bn2 = nn.BatchNorm2d(out_channel)  
  
    # 正向传播函数  
    def forward(self, x):  
        # 卷积  
        output = self.conv1(x)  
        # 批量归一化  
        output = self.bn1(output)  
        # 激活函数  
        output = F.relu(output)  
  
        # 第二次卷积和批量归一化以及激活函数  
        res = x + F.relu(self.bn2(self.conv2(output)))  
        return res  
  
  
class ResidualDownBlock(nn.Module):  
    def __init__(self, in_channels, out_channels, stride):  
        super(ResidualDownBlock, self).__init__()  
        # 定义3x3卷积层  
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride[0], padding=1)  
        # 定义批量归一化层，将上一次的输出归一化  
        self.bn1 = nn.BatchNorm2d(out_channels)  
        # 第二个3*3卷积层  
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1)  
        # 第二个批量归一化层  
        self.bn2 = nn.BatchNorm2d(out_channels)  
  
        # 调整通道和分辨率  
        self.extra = nn.Sequential(  
            nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride[0], padding=0),  
            nn.BatchNorm2d(out_channels)  
        )  
  
    def forward(self, x):  
        # 原始数据处理  
        extra_x = self.extra(x)  
  
        # 第一次卷积  
        output = self.conv1(x)  
        # 批量归一化  
        output = self.bn1(output)  
        # 激活函数  
        output = F.relu(output)  
  
        # 第二次卷积和批量归一化以及激活函数  
        res = F.relu(extra_x + self.bn2(self.conv2(output)))  
        return res  
  
  
# Resnet18网络  
  
class Resnet18(nn.Module):  
    def __init__(self):  
        super(Resnet18, self).__init__()  
        # 定义初始卷积网络  
        self.initConv = nn.Conv2d(3, 64, kernel_size=7, padding=3, stride=2)  
        # 定义初始归一化  
        self.initBn = nn.BatchNorm2d(64)  
        # 定义初始激活函数  
        self.initRelu = nn.ReLU(inplace=True)  
        # 构建残差模块组  
        self.layer1 = nn.Sequential(  
            ResidualBlock(64, 64, 1),  
            ResidualBlock(64, 64, 1)  
        )  # 第一组  
        self.layer2 = nn.Sequential(  
            ResidualDownBlock(64, 128, (2, 1)),  
            # 先使用含有1x1卷积层的块来调整通道，从64到128  
            ResidualBlock(128, 128, 1)  
        )  # 第二组  
        self.layer3 = nn.Sequential(  
            ResidualDownBlock(128, 256, (2, 1)),  
            ResidualBlock(256, 256, 1)  
        )  # 第三组  
        self.layer4 = nn.Sequential(  
            ResidualDownBlock(256, 512, (2, 1)),  
            ResidualBlock(512, 512, 1)  
        )  # 第四组  
  
        # 全局平均池化  
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))  
  
        # 全连接层  
        self.fc = nn.Linear(512, 10)  
  
    def forward(self, x):  
        # 初始卷积层  
        out = self.initConv(x)  
        # 第一个残差块  
        out = self.layer1(out)  
        # 第二个残差块  
        out = self.layer2(out)  
        # 第三个残差块  
        out = self.layer3(out)  
        # 第四个残差块  
        out = self.layer4(out)  
        # 平均池化  
        out = self.avg_pool(out)  
        # 重塑  
        out = out.reshape(x.shape[0], -1)  
        # 全连接层  
        out = self.fc(out)  
  
        return out
```

#### 3.4.6 模型测试

首先进行简单的构建模拟数据进行测试：
```python
# 创建一个模拟输入  
x = torch.randn(64, 3, 32, 32)  
  
# 实例化模型  
model = Resnet18()  
  
# 前向传播  
output = model(x)  
  
# 输出形状应为(64, 10)，因为我们有64个样本和10个类别  
print(output.shape)  # 输出：torch.Size([64, 10])
```

输出：
```
torch.Size([64, 10])
```

表明模型构建成功。

#### 3.4.7 模型评估

```python
model.eval()  
  
correct = 0  
total = 0  
with torch.no_grad():  
    for data in testloader:  
        images, labels = data  
        images, labels = images.cuda(), labels.cuda()  
        outputs = model(images)  
        _, predicted = torch.max(outputs.data, 1)  
        total += labels.size(0)  
        correct += (predicted == labels).sum().item()  
  
print(f'Accuracy of the network on the 10000 test images: {100 * correct / total}%')
```

运行结果：
![小杜的个人图床](http://src.xiaodu0.com/2024/06/02/65535ba08cf8daf8a0fd17c0df6a84f2.png)



----------------------------


## 四、训练模型

构建模型之后需要训练模型，，Pytorch训练模型主要包括如下内容：
- 加载和预处理数据集：使用Pytorch的数据处理工具来加载和预处理数据
- 定义损失函数：可以通过自定义方法或者Pytorch内置的损失函数定义损失函数，
- 定义优化方法：Pytorch常用的优化方法都封装在optim.Optimizer中，其设计很灵活，可以扩展为自定义的优化方法。所有优化的方法都是继承了基类`optim.Optimizer`，并实现了自己的优化步骤
- 反向传播：反向传播的主要目标是通过迭代更新网络的权重和偏置，逐步减小预测输出与实际目标之间的误差。
- 参数更新：通过更新网络的权重和偏置参数来最小化损失函数。

其中涉及的工具：

1. 循环训练模型：

```python 
model.train()
```

调用`train`方法会把所有的module设置为训练模式。
2. 梯度清零：

```python
optimizer.zero_grad()
```

在默认情况下梯度是累加的，需要手工把梯度初始化或者清零，调用`optimizer.zero_grad()`方法即可。

3. 求损失值

```python
y_prev = model(x)
loss = loss_fun(y_prev,y_true)
```
这里的y_prev是输入数据x在模型中前向传播的结果，即y的预测值，loss是损失值，通过损失函数loss_func产生，y_true是真实标签，通过将预测值与真实标签对比得到损失值。

4. 自动求导，实现梯度的反向传播

```python
loss.backward()
```

对损失值进行反向求导，计算损失值相对于模型参数的梯度。

5. 更新参数
```python
optimizer.step()
```

更新参数使用的优化器来更新模型参数以减少损失。

6. 循环测试或者验证模型

```python
model.eval()
```

`model.eval()`方法将所有的training属性设置为False，即将模型设置为评估模式的方法，主要用于评估或者推理阶段禁用某些特定层的行为，以确保模型在训练和推力器间的行为一致。

7. 在不跟踪梯度的模式下计算损失值、预测值等：
```python
with torch.no_grad():
```


*Note:About the `model.train()` and `model.eval()`*
> 如果模型中有**批量归一化（Batch Normalization,BH）层**和dropout层，需要在训练时添加 `model.train()`，在测试时添加 `model.eval()`。其中 `model.train()` 是保证BN层用每一批数据的均值和方差，而 `model.eval()` 是保证BN层用全部训练数据的均值和方法；而对于dropout层，model.train() 是随机选取一部分网络连接来训练更新参数，而model.eval() 则是用所有网络连接。



## 五、实现神经网络实例

本实例使用Pytorch 1.5+版本，GPU或者CPU，源数据集为MNIST。主要步骤如下：
- 利用Pytorch 内置函数mnist下载数据
- 利用torchvision对数据进行预处理、调用torch.utils建立一个数据迭代器。
- 可视化源数据
- 利用nn工具箱构建神经网络模型
- 实例化模型，并定义损失函数及优化器
- 训练模型
- 可视化结果。

神经网络结构如下图所示：

