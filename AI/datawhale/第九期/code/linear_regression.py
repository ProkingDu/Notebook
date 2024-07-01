import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# 设定随机数种子以便结果可复现
torch.manual_seed(0)

# 生成模拟数据
np.random.seed(0)
x_train = np.random.rand(100, 1) * 10  # 100个样本，特征值在0到10之间
y_train = 2 * x_train + 3 + np.random.randn(100, 1) * 0.3  # 通过自变量产生的标签值

# 将numpy数组转换为PyTorch张量
x_train_tensor = torch.from_numpy(x_train).float()
y_train_tensor = torch.from_numpy(y_train).float()


# 定义线性回归模型
class LinearRegression(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, x): # 前向传播
        out = self.linear(x)
        return out



# 初始化模型
input_dim = 1    # 线性回归算法的输入输出维度都是1
output_dim = 1
model = LinearRegression(input_dim, output_dim)

criterion = nn.MSELoss()    # 计算均方误差的损失函数
learning_rate = 0.01   # 学习率
# 创建SGD优化器用于自动更新参数，其中model.parameters包含模型中所有可训练参数的迭代器，lr是学习率的缩写，指定参数更新的步长。
optimizer = optim.SGD(model.parameters(), lr=learning_rate)

# 训练模型
num_epochs = 100   # 指定参数更新次数
for epoch in range(num_epochs):
    # 前向传播
    outputs = model(x_train_tensor)
    # 通过输出和标签值计算损失值
    loss = criterion(outputs, y_train_tensor)

    # 反向传播和优化
    optimizer.zero_grad()  # 清零梯度缓存
    loss.backward()  # 反向传播，计算梯度
    optimizer.step()  # 使用梯度下降更新权重

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}')



# 获取模型的参数
print('Model parameters:')
for name, param in model.named_parameters():
    print(f"    Name: {name}, Value: {param.data.numpy()}")