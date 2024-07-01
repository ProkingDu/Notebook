import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

X_train = torch.randn(100,5)
Y_train = torch.randint(0, 2, (100,))  # 对应的二进制标签

# 定义逻辑回归模型
class LogisticRegressionModel(nn.Module):
    def __init__(self,input_dim=5):
        super(LogisticRegressionModel,self).__init__()
#         线性回归模型
        self.linear=nn.Linear(input_dim,1)
    # 前向传播
    def forward(self,x):
        y_predicted = torch.sigmoid(self.linear(x))
        return y_predicted.squeeze()  # 移除最后一维，变为一维张量


# 初始化模型
model = LogisticRegressionModel(X_train.shape[1])

# 定义损失函数和优化器
criterion = nn.BCELoss()
learning_rate = 0.01
optimizer = optim.SGD(model.parameters(),lr=learning_rate) # 定义优化函数

# 加载数据集
train_dataset = TensorDataset(X_train,Y_train.float().unsqueeze(1))
train_loader = DataLoader(dataset=train_dataset,batch_size=32,shuffle=True)

# 训练模型
num_epochs = 100
for epoch in range(num_epochs):
    for i,(input,label) in enumerate(train_loader):
        # 前向传播
        output = model(input)
        loss = criterion(output,label)

        # 反向传播和优化
        optimizer.zero_grad() # 清除梯度
        loss.backward()  # 反向传播计算梯度
        optimizer.step()  # 更新权重
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}')