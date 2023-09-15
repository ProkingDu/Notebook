　　# flex布局基础

## 一、布局的基本概念

### 定义

Flexible Box 模型，通常被称为 flexbox，是一种一维的布局模型。它给 flexbox 的子元素之间提供了强大的空间分布和对齐能力。

### 为什么说flex是一个一维的布局？

将网页视作一个平面，flex布局只能在一次处理一个纬度上的布局，即 一行或者一列。
与之对比的是
**CSS Grid Layout**布局，是一类二维的布局，可以一次处理行列上的布局。

## 二、flex的两根轴线

flex布局下最重要的概念是轴线和起终线（起始线和终点线）。首先需 要理解轴线的概念。

轴线分为**主轴和交叉轴**，所有flex布局有关的属性都与这两根轴线 有关。

### （一）主轴

主轴实际上就是元素的延伸方向，在flex布局下，元素内所有的子元素 将沿着主轴的方向延伸。

主轴通过 ``flex-direction`` 定义，有如下四个属性值：
1. row
2. row-reverse
3. column
4. column-reverse

flex-direction译为“弯曲方向”实际上也就是元素排列的方向。

#### 1. row

当flex-firection被设定为row时，表示主轴线是水平排序的，这时候轴线呈现行的样式。（轴线是不可见的，只是一个布局的概念。）

当轴线呈现水平方向时，请记住flex布局下的元素是顺着主轴的方向排 序的。所以此时弹性盒子的子元素呈现水平排列的`inline`样式。

![](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox/basics1.png)

#### 2. row-reverse

reverse表示反转，颠倒。

row-reverse即反转的主轴线，会置换主轴的起点和终点。默认的主轴线是从左到右延伸的，但是当reverse之后，主轴线从右往左延伸，相当于元素会**以垂直中线进行反转**。简单理解，就是元素在水平方向上从 右往左排序。

#### 3. row与row-reverse

无论是row还是row-reverse，二者都表示主轴线沿着inline方向延展。 此时布局内元素水平排列，相当于display:inline-block（但不等同于 此，因为元素不会被限制在inline-block）

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

此时主轴线翻转起点和终点，起点在最右端，终点在最左端，元素从起 点开始排序，也就是从右往左排序。



#### 4. column
column表示列，与row相反，在flex布局中，通过column定义使元素呈现列排序，此时元素的表现是类似block的形式，也就是说，flex布局中的主轴线是一条**垂直**的线，然后子元素会顺着这条垂直的线展开。


#### 5. colum-reverse
与row-reverse类似，column-reverse表示列的翻转，原先column时主轴线是从上至下展开，而当colum被翻转时，主轴线仍然是垂直的，但是他是从下至上翻转的。所以子元素是从上至下排列的。

#### 6. 示例与对比

简单的示例：

css：

```css
    .container{
        width: auto;
        display: flex;
        height: auto;
        flex-direction: column;
    }
    .box{
        line-height: 100px;
    }
```

HTML：

```
    <div class="container">
        <div class="box" style="background-color: red;">
            第一行
        </div>
        <div class="box" style="background-color: blue;">
            第二行
        </div>
        <div class="box" style="background-color: green;">
            第三行
        </div>
    </div>
```

效果：
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694696968-image-1024x362.png)

同理，如果将`flex-direction`设置为`column-reverse`则：
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694697231-image-1024x274.png)
子元素的排序会被颠倒。

#### 7. 总结
在抽象的主轴线概念中，最重要的属性是flex-direction，他的四个值 分别是：水平主轴线的`rwo`、`row-reverse`和垂直主轴线的`column` 、`column-reverse`

**子元素会随着主轴线的延展方向排列，如果主轴线是 *水平的* 则子 元素也会随着主轴线水平排列， 且呈现水平的inline的样式。<br>如果主轴线是 *垂直的* 则子元素会随着主轴线垂直排列，且子元素呈现block的样式。**

### （二）交叉轴

交叉轴同样是一个抽象的概念，它垂直于主轴。
也就是说，当主轴是`row`、`row-reverse`时，交叉轴是垂直展开的。
即：
![](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox/basics3.png)

反之，当主轴是`column`、`column-reverse`时，交叉轴是水瓶展开的 。
即：
![](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox/basics4.png)

理解了主轴的概念，交叉轴的内容只有这么多，它仅仅是垂直于主轴的 一根轴而已。

主轴和交叉轴构成了类似 *世界坐标系* 的定位机制

## 三、起始线和终点线

Flex将不在会对书写模式提供假设，以前的CSS认为，书写模式是水平的，从右往左的。

但是在Flex中，内容的延伸方向是由flex-direction决定的，他可以是 从左往右，也可以是从右往左，所以这就需要引入起始线和终点线的概 念。

可以从MDN给出的示例得知，文本的书写不再使用从左往右描述，而是使用起始线和终点线描述，

例如，当`flex-direction:row`时，文本元素是水平排列的，那么主轴 的起始线是在左边，终点线是在右边，这样构成了一个盒子的范围。

如下图所示：

![](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox/basics5.png)

但这不是绝对的，如果是阿拉伯文，他会被自动转换为方向是起始线在 右，终点线在左。

![](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox/basics6.png)

而在交叉轴，因为这两种语言都是水平书写模式，所以交叉轴的起始线 在顶部，终点线在底部。

### 四、Flex容器