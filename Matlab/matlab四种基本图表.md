# matlab四种基本图

## 一、plot绘制线图

### 1.plot(x,y)
plot最简单的形式是Plot(x,y) x决定横坐标,y决定纵坐标。

* 要绘制由线段连接的一组坐标，请将 X 和 Y 指定为相同长度的向量。
* 要在同一组坐标区上绘制多组坐标，请将 X 或 Y 中的至少一个指定为矩阵。

例如：
```
x=[-3,-2,-1,0,1,2,3]
y=[9,4,1,0,1,4,9]
plot(x,y)
```
输出：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/55d824255b60c494f1bd47dd3d135475.png)

### 2.范围取值
通过x:z:y可以取得一个在[x,y]范围内且步长为z的矩阵，用在绘图中非常实用。
例如绘制一个三角函数图像，x的范围为-2π到2π每隔0.05π取值一次使得图像更加圆滑，y轴的数据来自三角函数sin(x)。
如果直接绘制：
```
x=[-2*pi,-pi,0,pi,2*pi]
y=sin(x)
plot(x,y)
```
得出的是一个这样奇奇怪怪的东西：

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/e74a6af222b3fcdec51e33224fec280e.png)

原因是即使y的数据集足够多，但是x只有上面四个数据集，他只在图像标出x对应的几个点的连线，所以这时候看上去就是一个折线。
如果要得到圆滑的曲线三角函数图像，需要使x的点足够多来使这些点能够连接成一个光滑的曲线（实际上就是图像上的点非常密集。）
只需要将x改为：
```
x=-2*pi:0.1*pi:2*pi
```
图像的点会在-2π到2π的范围内每隔0.1π取一次值，这些点的连线看上去就像一个光滑的曲线了。
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/ed3477c954bbb9ab8fe9cf7bff5aaa92.png)

同时可以指定x轴和y轴的范围，请注意plot(x,y)传入的参数是x轴和y轴的数据点，而不是x轴和y轴上标注的点，他们是在函数图像中的点。
指定坐标轴的范围：
```
axis([x1 x2 y1 y2])
```
通过axis传入一个矩阵表示指定x轴和y轴的起终点。
对上面的例子加上：
```
axis(-6 6 -2 2)
```
输出：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/09f360af94a4dedb5f04cc4e3d5a4c3b.png)

**注意：axis必须传入一个矩阵！！！！**

### 3.plot(x1,y1,x2,y2......Xn,Yn)
`plot(x1,y1,x2,y2......Xn,Yn)`用于在一个图上绘制多个线条，通过指定不同的数据集即可。
例如在同一张图像上绘制二次函数的曲线和正余弦曲线。
```
x1=-3:0.05:3
y1=x1.*x1
x2=-pi:0.05*pi:pi
y2=sin(x2)
x3=x2
y3=cos(x3)
plot(x1,y1,x2,y2,x3,y3)
axis([-3 3 -1.5 4])
```

输出：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/c979c1c7047632b602ab8a18ec96c3b1.png)

### 4.绘制矩阵的图像
绘制矩阵的图像只需要传递一个参数即矩阵的值，图像的横坐标为矩阵的行数，有几行就有几个横坐标点，有几列就有几条线条，每一个线条的纵坐标值每一列的值。
例如：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/60d10bb77333214ac3483910e1f0cbc0.png)

### 5.设置图像样式
通过一些实用的参数可以设置图像的样式。

#### (1).grid on
`grid on` 参数用于设置图像网格：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/4db3ca4d2acec3dab0eab209e6b7d395.png)

#### (2).添加标题和轴标签
通过`title()`添加图像标题
通过`xlabel()`添加x轴标签
通过`ylabel()`添加y轴标签

示例：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/618ec3d3ae131a5315d7d12843670892.png)

#### (3).指定线条样式

```
plot(X1,Y1,LineSpec1,...,Xn,Yn,LineSpecn)
```
可为每个 x-y 对组指定特定的线型、标记和颜色，可以对某些 x-y 对组指定 LineSpec，而对其他对组省略它。

例如，plot(X1,Y1,"o",X2,Y2) 对第一个 x-y 对组指定标记，但没有对第二个对组指定标记。

示例：指定二次函数为虚线，正弦函数为点线，余弦函数不指定:
```
plot(x1,y1,"--",x2,y2,":",x3,y3)
```

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/6c1a7f9da69f7635d2c8b2c8339357c8.png)

LineSpec还可以指定线条标记和线条颜色：
```
plot(x1,y1,"r--o",x2,y2,"g:x",x3,y3)
```
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/2ab4238afc9c11d4195d155610d07924.png)

参数列表：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/ca613a3ac1552b5b618676a241be8fab.png)

#### (3).指定线条宽度
通过`LineWidth`指定线条宽：
```
plot(x1,y1,"r--o","LineWidth",1,x2,y2,"g:x",x3,y3)
```

## 二、条形图
通过`bar()`创建水平条形图
通过`barh()`创建垂直条形图

### 1.bar(y)
`bar(y)` 创建一个条形图，y 中的每个元素对应一个条形。

要绘制单个条形序列，请将 y 指定为长度为 m 的向量。这些条形沿 x 轴从 1 到 m 依次放置。

要绘制多个条形序列，请将 y 指定为矩阵，每个序列对应一列。

示例：
```
y=[1,3,5,7,9
    2,4,6,8,10
    ]
bar(y)
```

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/3cd0b0adde2af1938dab33a25b0f9b54.png)

### 2.bar(x,y)
bar(x,y) 在 x 指定的位置绘制条形。
```

x=[2021,2022,2023]
y=[200,150,100]
bar(x,y)
```

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/55ed3483c7e329d51d98b180e668ddc9.png)

### 3.bar(__,width)
`bar(___,width)` 设置条形的相对宽度以控制组中各个条形的间隔。将 width 指定为标量值。可将此选项与上述语法中的任何输入参数组合一起使用。

```
x=[2020,2021,2022,2023]
y=[18,21,16,30]
bar(x,y,0.5)
```

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/6ba5e329c142a68575841a2da5c6cb91.png)

### 4.bar(___,style)
`bar(___,style)` 指定条形组的样式。例如，使用 'stacked' 将每个组显示为一个多种颜色的条形。

```
x=[18 19 20 21 22]
y=[10 15 20 35 50
    20 50 60 80 40
    100 200 300 400 500 600
    ]
bar(x,y,"stacked")
```
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/c5466085c61509703580855bae3872dd.png)

参数：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/9f90522488cfc89f7906b3bbeeba5193.png)

### 5.bar(___,color)
`bar(___,color)` 设置所有条形的颜色。例如，使用 'r' 表示红色条形。

```
y = [75 91 105 123.5 131 150 179 203 226 249 281.5];
bar(y,'r')
```
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/385dd47a3160cb873b71c89e2482c583.png)

barh()与bar的参数完全一致，就不一一演示了。

## 三、极坐标图
通过`polarplot(theta,radi)`来绘制极坐标图
* theta 弧度
* radi 半径

```
t=0:0.01:2*pi
r=abs(sin(7*t).*cos(10*t))
polarplot(t,r)
```

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/c90e547b7ebc029a6c4123aaca0c4b6e.png)

## 四、散点图
通过`scatter(x,y)`绘制散点图
可以使用`randn(r,c)`生成符合正态分布的矩阵，其中r是行数，c是列数。
例如：
```
x=randn(100,100)
y=randn(100,100)
scatter(x,y)
```

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231024/38491ce1370b4cd7946f2b647f7ba9c6.png)