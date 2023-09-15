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

**整个Flex布局轴模型示意：**
```
.demo{
        margin-top: 50px;
        margin-left: 100px;;
        width: 500px;
        display: flex;
        flex-direction: row;
        /* border:1px solid #666; */
        padding: 30px;
        position: relative;
    }
    .demo .box{
        margin: 5px;
    }
    .main-row{
        width: 100%;
        position: absolute;
        height: 1px;
        border-top:1px dotted red;
        top:3px;
        left: 0px;
        color:red;
        font-size:12px
    }
    .jc-row{
        width: 1px;
        border-left:1px dotted #0602fc;
        position: absolute;
        top:0px;
        left: 0px;
        height: 70%;
        padding-top:20px;
        color:blue;
        font-size:10px;
        }
        .main-start{
            width: 10px;
            padding: 2px;;
            height: 70%;
            border-right: 2px solid green;
            font-size: 10px;
            color: green;
            position: absolute;
            top:0px;
            left: -15px;
            text-align: left;
        }
        .main-end{
            width: 10px;
            padding: 2px;;
            height: 90%;
            border-left: 1px solid rgb(255, 9, 169);
            font-size: 10px;
            color: rgb(255, 0, 157);
            position: absolute;
            top:0px;
            right: 0;
            text-align: left;
        }
        .jc-start{
            width: 100%;
            padding: 2px;;
            height: 10px;
            border-bottom: 2px solid rgb(7, 189, 255);
            font-size: 10px;
            color: rgb(0, 208, 255);
            position: absolute;
            top:-15px;
            left: 0px;
            text-align: left;
        }
        .jc-end{
            width: 100%;
            padding: 2px;;
            height: 10px;
            border-top: 2px solid rgb(255, 201, 7);
            font-size: 10px;
            color: rgb(255, 166, 0);
            position: absolute;
            bottom:0px;
            left: 0px;
            text-align: left;
        }
```
```
 <div class="demo">
        <div class="box" style="background-color: #666;">
            One
        </div>
        <div class="box" style="background-color: #999;">
            two
        </div>
        <div class="box" style="background-color: #999;">
            Three
        </div>
        <div class="main-row">
            主轴线
        </div>
        <div class="jc-row">
            交叉轴
        </div>
        <div class="main-start">
            主轴线起始线
        </div>
        <div class="main-end">
            主轴线终点线
        </div>
        <div class="jc-start">
            交叉轴起始线
        </div>
        <div class="jc-end">
            交叉轴终点线
        </div>
    </div>
```

结果：
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694772807-image-1024x278.png)

这是当flex-direction为row时的参考模型，当flex-direction为row-reverse时，主轴线交换起终点：
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694772934-image-1024x278.png)

当flex-direction为column时，主轴线和交叉轴置换:
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694773151-image-1024x451.png)

当column-reverse时，仍然是主轴线起始线和终点线置换，但此时主轴线是从上至下展开：
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694773372-image-1024x409.png)

由此可以对上述内容进行最终总结：
* 在flex布局中，元素顺着主轴线展开，且延展方向为从主轴线的起始线到终点线。
* reverse不会影响主轴线和交叉轴，会置换主轴线的起终点。
* 更改row或column置换主轴线和交叉轴，但不会影响起终点。
* 起始线和终点线就是为了确定元素的排列方向，而不是通俗的从右到左或从左到右。

### 四、Flex容器

如上方图片所示，整个轴和线围成的区域就是Flex容器，在官方定义中，某个盒子设置为`display:flex`即为一个Flex容器，他的所有子元素会按照flex的样式布局。

由此，创建flex容器的方法就是将一个容器元素的display属性设置为`flex`或者`inline-flex`。在这之后flex容器的所有*直系子元素*就会变成flex元素，由于css所有的属性都会默认值，所以这些子元素会有如下表现：
1. 元素排列为一行 (flex-direction 属性的初始值是 row)。
2. 元素从主轴的起始线开始。
3. 元素不会在主维度方向拉伸，但是可以缩小。
4. 元素被拉伸来填充交叉轴大小。
5. `flex-basis` 属性为 *`auto`*。
6. `flex-wrap` 属性为 *`nowrap`*。

> flex-basis:元素在其主轴方向的初始大小，可能的值：
> * width 指定宽度
> * content 基于内容自定调整大小
> * css的全局值

$\color{#ff0000}{Notice：flex-sasis应用于felx元素而不是flex容器}$

> flex-wrap: 指定flex元素的内容是否换行，


同时会表现出如下特性：
* 默认的flex元素会呈现线性排列，并且把自己的大小作为主轴上的大小。
* 元素的数量超出了容器，那么他们会溢出而不是换行。因为默认的flex-wrap是nowrap，即元素不会换行。
* 当一个元素的高度超过其他元素的高度，则此元素会把flex容器撑开，其他的元素会沿着交叉轴的方向拉伸至和最高的元素高度相同。

以上方的基本模型为示例，取消容器的padidng，注释点他的轴线，并且加上border，为其中一个元素填充内容以让他的高度变大，最终呈现如下效果：
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694775683-image-1024x276.png)

如果你为flex元素指定高度，某一个高度缩小，不会影响到其他元素的高度。


