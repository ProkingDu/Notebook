## 一、布局的基本概念

### 定义

Flexible Box 模型，通常被称为 flexbox，是一种一维的布局模型。它给 flexbox 的子元素之间提供了强大的空间分布和对齐能力。

### 为什么说flex是一个一维的布局？

将网页视作一个平面，flex布局只能在一次处理一个纬度上的布局，即一行或者一列。
与之对比的是
**CSS Grid Layout**布局，是一类二维的布局，可以一次处理行列上的布局。

## 二、flex的两根轴线

flex布局下最重要的概念是轴线和起终线（起始线和终点线）。首先需要理解轴线的概念。

轴线分为**主轴和交叉轴**，所有flex布局有关的属性都与这两根轴线有关。

### 主轴

主轴实际上就是元素的延伸方向，在flex布局下，元素内所有的子元素将沿着主轴的方向延伸。

主轴通过 ``flex-direction`` 定义，有如下四个属性值：
1. row
2. row-reverse
3. column
4. column-reverse

flex-direction译为“弯曲方向”实际上也就是元素排列的方向。

#### row

当flex-firection被设定为row时，表示主轴线是水平排序的，这时候轴线呈现行的样式。（轴线是不可见的，只是一个布局的概念。）

当轴线呈现水平方向时，请记住flex布局下的元素是顺着主轴的方向排序的。所以此时弹性盒子的子元素呈现水平排列的`inline`样式。

![](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox/basics1.png)

#### row-reverse

reverse表示反转，颠倒。

row-reverse即反转的主轴线，会置换主轴的起点和终点。默认的主轴线是从左到右延伸的，但是当reverse之后，主轴线从右往左延伸，相当于元素会**以垂直中线进行反转**。简单理解，就是元素在水平方向上从右往左排序。

#### row与row-reverse

无论是row还是row-reverse，二者都表示主轴线沿着inline方向延展。此时布局内元素水平排列，相当于display:inline-block（但不等同于此，因为元素不会被限制在inline-block）

简单的例子:
```
<div id="content">
<div class="box" style="background-color:red">
A
</div>
<div class="box" style="background-color:blue">
 B
</div>
<div class="box" style="background-color:green">
C
</div>
</div>
```


```
<style>
    #content{
    width:100vw;
    height:500px;
    display:flex;
    /* 表示使用flex布局 */
    flex-direction:row;
    }
    .box{
    width:100px;
    height:100px;
    margin:5px
    }
</style>
```



最终样式：

![image-20230913124914140](C:\Users\28110\AppData\Roaming\Typora\typora-user-images\image-20230913124914140.png)



如果将上方的其他代码不动，而更改`row` 为`row-reverse`则：

![1](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694581006-image.png)

此时主轴线翻转起点和终点，起点在最右端，终点在最左端，元素从起点开始排序，也就是从右往左排序。



#### column





