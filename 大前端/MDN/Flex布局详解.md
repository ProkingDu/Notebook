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
        flex-wrap:nowrap;
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

## 四、Flex容器

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

> flex-wrap: 指定flex元素是单行显示还是多行显示，同时可以控制元素的堆叠顺序。
> 可能得值：
> * nowrap 默认值。不允许flex元素换行，即单行显示，当元素过多会导致溢出。
> * wrap 元素多行显示，当flex容器内的元素过多会自动换行显示
> * wrap-reverse 与wrap等效，但是会逆向排序。

$\color{#ff0000}{Notice:flex-wrap应用于flex容器}$

同时会表现出如下特性：
* 默认的flex元素会呈现线性排列，并且把自己的大小作为主轴上的大小。
* 元素的数量超出了容器，那么他们会溢出而不是换行。因为默认的flex-wrap是nowrap，即元素不会换行。
* 当一个元素的高度超过其他元素的高度，则此元素会把flex容器撑开，其他的元素会沿着交叉轴的方向拉伸至和最高的元素高度相同。

以上方的基本模型为示例，取消容器的padidng，注释点他的轴线，并且加上border，为其中一个元素填充内容以让他的高度变大，最终呈现如下效果：
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694775683-image-1024x276.png)

如果你为flex元素指定高度，某一个高度缩小，不会影响到其他元素的高度。

对flex-wrap测试：
1. 当flex-wrap为nowrap：


![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694779589-image-1024x341.png)

1. 当felx-wrap为wrap：

![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694779667-image-1024x371.png)

1. 当flex-wrap为wrap-reverse:

![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694779744-image-1024x358.png)

## 五、Flex的简写属性

可以将flex-direction与flex-wrap简写为flex-flow，其中指定第一个值为flex-direction，第二个字为flex-wrap。

例如：指定Flex容器主轴为row，且不允许换行：
```
flex-flow:row nowrap;
```

## 六、Flex元素上的属性

在介绍Flex元素属性之前，需要先了解关于Flex容器可用空间的概念。

顾名思义，可用空间就是除去元素已经占据的空间之外，在容器中剩余的空间，实际上也是一种盒子模型。

例如如下Flex容器，容器宽度为1000px,其中每个元素的默认宽度的为22px，第一个元指定了`width:200px`,所以该容器内可用空间为1000-200-22*4=712px。

![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694871111-image-1024x62.png)

**如果没有给元素设定尺寸，flex-basis 的值采用元素内容的尺寸。这就解释了：我们给只要给 Flex 元素的父元素声明 display: flex ，所有子元素就会排成一行，且自动分配小大以充分展示元素的内容。**


常用的Flex元素属性有以下三个：

* flex-basis 即元素所占据的初始空间，类似width，但是比width优先级要高。
* flex-grow flex会以basis为基础，向主轴终止线方向延伸占据剩余可用空间。
* flex-shrink 与flex-grow相反，指定元素收缩。

### 1. flex-basis
MDN:

**CSS 属性 flex-basis 指定了 flex 元素在主轴方向上的初始大小。如果不使用 box-sizing 改变盒模型的话，那么这个属性就决定了 flex 元素的内容盒（content-box）的尺寸。**

>box-size:决定浏览器如何计算元素的内容宽高。
> * content-box 默认值。如果设定一个元素的宽高为100px，则这个宽高是针对于元素内容区域的宽高，如果为元素额外设定边框和内边距，都会在最后被计算为元素的总宽高。
> * box-border 与content-box相反，当设定元素宽高时会被表现为元素的内容区域+填充和边框，即实际的元素内容区域=元素总大小-边框-填充。
> * $\color{#ff0000}{元素的外边距（Margin不会被计算）}$

flex-basis的属性值可以是指定的像素值（px），也可以是相对于其父元素的百分比。他的默认属性值是auto，即根据元素排列自动调整。

示例：一个简单的两列列表
```css
.ul{
            width:60%;
            margin-left:20%;
            display: flex;
            flex-wrap: wrap;
        }
        .list{
            flex-basis: 50%;
            white-space: nowrap;
            overflow: clip;
            text-overflow: ellipsis;
            padding: 5px;
            box-sizing: border-box;
        /*    由于加上填充会使元素换行，所以给定元素box-sizing:border-box*/
        }
```
```html
<ul class="ul">
        <li class="list">我吃早饭了</li>
        <li class="list">我吃午饭了</li>
        <li class="list">我去学习了</li>
        <li class="list">我去打球了</li>
        <li class="list">我吃晚饭了</li>
        <li class="list">我吃晚饭之后去操场溜达了一圈，然后跑了两圈摔了三跤</li>
    </ul>
```
结果：
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694942387-image-1024x191.png)

如果指定flex-basis的值加起来大于容器宽度，且容器felx-wrap为nowrap，则子元素会被压缩而不会撑开父元素：

![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694942387-image-1024x191.png)

### 2.flex-grow

flex-grow指定元素的占据空间的增长系数， 根据元素的flex-basis为基础，沿着主轴线的方向进行延展。如果有其他元素也被允许延展，那么他们会各自占据可用空间的一部分。

如下示例，给五个子元素设置flex-basis为50px。且box-sizing为border-box，为A和B的flex-grow分别设定为1和2：
````css
 .container{
            width:600px;
            padding:5px;
            display: flex;
            flex-wrap: nowrap;
            border:1px solid #666;
        }
        .box{
            padding: 10px;
            background: #91e7e7;
            /*margin: 5px;*/
            border-radius: 3px;
            flex-basis:50px;
            box-sizing: border-box;
        }
````
```html
<div class="container">
    <div class="box" style="flex-grow: 1">A</div>
    <div class="box" style="flex-grow: 2">B</div>
    <div class="box">C</div>
    <div class="box">D</div>
    <div class="box">E</div>
</div>
```

结果：
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694955409-image.png)

由于容器的总宽度为600px，默认的Flex-basis为50px，则除去CDE剩余的空间为450px，A、B的flex-grow分别为1、2，即将剩下的450px分为三等分，A占据三分之一，B占据三分之二，所以的到A的宽度约为150px，B的宽度约为300px。

### 3. grow-shrink
flex-grow属性是处理 flex 元素在主轴上增加空间的问题，相反flex-shrink属性是处理 flex 元素收缩的问题。如果我们的容器中没有足够排列 flex 元素的空间，那么可以把 flex 元素flex-shrink属性设置为正整数来缩小它所占空间到flex-basis以下。与flex-grow属性一样，可以赋予不同的值来控制 flex 元素收缩的程度 —— 给flex-shrink属性赋予更大的数值可以比赋予小数值的同级元素收缩程度更大。

### 4.flex属性的简写

实际上对于上述三种属性很少会同时使用，而是使用简写属性flex来同时定义flex-grow、flex-shrink、flex-basis。
```css
flex:flex-grow flex-shrink flex-basis;
```

### 5.flex属性的预定值
flex属性具有如下自定义形式：
* flex:initial 将元素重置为flexbox的初始值，相当与flex:0 1 auto，由于flex-grow为0，所以元素不会超过felx-basis，flex-shrink为1，元素可以被缩小来防止溢出，而flex-basis为aut，相当于content-box。
* flex-auto 等同于flex:1 1 auto，与flex-initial基本相同，但是指定了flex-grow为1，所以元素既可以拉伸也可以收缩。
* flex:none 相当于flex:0 0 auto，元素不可伸缩，但是会按照flex-basis:auto进行布局。

## 七、元素的对齐和空间分配

### 1.align-items

`align-items`使元素在交叉轴方向对齐。实际上，他可以用于flexbox和Grid Layout两种布局。这里只指出其在Flexbox的属性值。

在Flex布局中，align-items默认值是stretch，使元素的高度填充容器的高度，这也就是为什么默认情况下，Flex元素会被拉伸到填满容器，严格来说，应该是容器被元素撑开并拉伸子元素。

看一个简单的例子：
css:
```
.box{
    display: flex;
    }
    .box *{
    background: red;
    margin:5px;
    padding:10px
    }
```

html:

```
 <div class="box">
    <div class="item">A</div>
    <div class="item" style="height:200px;">B</div>
    </div>
```

[![pP4tRjx.jpg](https://z1.ax1x.com/2023/09/18/pP4tRjx.jpg)](https://imgse.com/i/pP4tRjx)

实际上A所在的盒子并没有被设定高度，但是他被拉伸到了和父元素一样的200px，而父元素的高度，又来自于其最高子元素的高度，所以说stretch是子元素将父元素撑开并拉伸子元素。

**align-items有如下适用于flex的属性：**

|属性值|说明|
|:----:|:------|
|stretch|默认值。当容器flex-direction:row时，使最高的子元素撑开容器并且拉伸其他子元素至相同高度。当column时，除非你指定宽度，否则他的宽度会拉满，高度默认由内容决定。|
|flex-start|row:元素沿着交叉轴起始线展开，宽度高度默认由内容决定。|
|flex-end|row:元素沿着交叉轴终点线展开，宽高默认都由内容决定。|
|center|元素沿着交叉轴中线展开，如果是row相当于垂直居中，如果是column相当于水平居中，宽高默认都有内容决定。|

*对于上方的默认情况，指不通过width、height、flex-basis等来指定元素大小的情况。*

对所有情况做出示例：
```
<style>
        .flex-box{
            border: 1px solid #666;
            display: flex;
        }        
        .demo1{
            flex-direction: row;
            align-items: stratch;
        }
        .flex-box .f{
            margin-left:5px;
            border-radius: 5px;
            padding: 5px;
        }
        .flex-box .f:nth-child(1){
            background-color: antiquewhite;
        }
        .flex-box .f:nth-child(2){
            background-color: rgb(255, 134, 134);
        }
        .flex-box .f:nth-child(3){
            background-color: rgb(138, 208, 215);
        }
        .flex-box .f:nth-child(4){
            background-color: rgb(139, 222, 91);
        }
        .flex-box .f:nth-child(5){
            background-color: rgb(232, 190, 65);
        }
        .flex-box .f:nth-child(6){
            background-color: rgb(252, 0, 67);
        }
        .demo2{
            flex-direction: column;
        }
        
    </style>
    <div class="flex-demo">
        <h3>默认的stratch演示：</h3>
        <div class="flex-box demo1">
            <div class="f">No.1</div>
            <div class="f">No.2</div>
            <div class="f">No.3</div>
            <div class="f">this is a long mark.;it will decide the height of container</div>
            <div class="f">this is the last mark.</div>
        </div>
        <h3>当flex-direction为column时，stratch：</h3>
        <div class="flex-box demo2">
            <div class="f">No.1</div>
            <div class="f">No.2</div>
            <div class="f">No.3</div>
            <div class="f">this is a long mark.in row direction,this will not decide the height of container,and will not influence the height of other marks.</div>
            <div class="f">this is the last mark.</div>
        </div>
        <h3>当flex-direction为row时，flex-start：</h3>
        <div class="flex-box" style="flex-direction: row;align-items: flex-start;">
            <div class="f">No.1</div>
            <div class="f">No.2</div>
            <div class="f">No.3</div>
            <div class="f">this is a long mark.in flex-start,it will not open out its father mark,and other marks will at the top of container</div>
            <div class="f">this is the last mark.</div>
        </div>
        <h3>当flex-direction为column时，flex-start：</h3>
        <div class="flex-box" style="flex-direction: column;align-items: flex-start;">
            <div class="f">No.1</div>
            <div class="f">No.2</div>
            <div class="f">No.3</div>
            <div class="f">this is a long mark.in column and flex-start,it also will not open out its father mark,in default,all the marks will full of the width of container.</div>
            <div class="f">this is the last mark.</div>
        </div>
        <h3>当flex-direction为row时，flex-end：</h3>
        <div class="flex-box" style="flex-direction: row;align-items: flex-end;">
            <div class="f">No.1</div>
            <div class="f">No.2</div>
            <div class="f">No.3</div>
            <div class="f">this long mark will not open out the container and all the marks's size will decide by their content.the best important,the will align with the end of container's crossed-axis,it same as at the bottom of container</div>
            <div class="f">this is the last mark.</div>
        </div>
        <h3>当flex-direction为column时，flex-end：</h3>
        <div class="flex-box" style="flex-direction:column;align-items: flex-end;">
            <div class="f">No.1</div>
            <div class="f">No.2</div>
            <div class="f">No.3</div>
            <div class="f">this long mark will not open out the container and all the marks's size will decide by their content.the best important,the will align with the end of container's crossed-axis,it same as at the right of container</div>
            <div class="f">this is the last mark.</div>
        </div>
        <h3>当flex-direction为row时，center：</h3>
        <div class="flex-box" style="flex-direction:row;align-items: center;">
            <div class="f">No.1</div>
            <div class="f">No.2</div>
            <div class="f">No.3</div>
            <div class="f">this max mark also can not influence other marks's size,but the max size of container is decided by it. and other marks wil in the middle of column direction.</div>
            <div class="f">this is the last mark.</div>
        </div>
        <h3>当flex-direction为column时，center：</h3>
        <div class="flex-box" style="flex-direction:column;align-items: center;">
            <div class="f">No.1</div>
            <div class="f">No.2</div>
            <div class="f">No.3</div>
            <div class="f">all the column's characters is same as row.just a difference: smaller marks will in the center of a line.</div>
            <div class="f">this is the last mark.</div>
        </div>
    </div>
```

结果：
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1695043387-image-582x1024.png)
![](http://www.xiaodu0.com/wp-content/uploads/2023/09/1695043442-image-777x1024.png)

$\color{#ff0000}{实际上图片上有一处不合适，在align-itmes不为stretch时未指定容器尺寸时，最大的元素仍然撑开了容器，不过没有影响其他的元素。但是当指定了容器尺寸时，较大的子元素会溢出父元素。}$

### 2.justify-content
align-items是指定元素在容器交叉轴的对其方向，而justify-content是对应元素在主轴线的对其方向，主轴线即为flex-direction定义的方向。
他的默认值是flex-start即元素沿着主轴线的起始线方向展开，相应的flex-end就是从主轴线的终点线展开，相当于从右到左。
在MDN给出：
> CSS justify-content 属性定义浏览器如何沿着弹性容器的主轴和网格容器的行向轴分配内容元素之间和周围的空间。

所以实际上justify-content不应该被简单的理解为对齐，而是元素如何分布。

justify-content有如下属性：
|属性值|说明|
|:----:|----|
|start|指定元素与行首对齐，同时所有后续元素与前一个元素对齐,等效于flex-start|
|end|指定元素元素与行尾对齐，同时所有前面的元素与后一个元素对齐，等效于flex-end|
|**flex-start**|**指定元素沿着主轴线的起始线展开，仅用于flex布局，否则此元素等效于start**|
|flex-end|**指定元素由主轴线的终止线开始排列，如果不是flex布局， 相当于end**|
|left|伸缩元素一个挨一个在对齐容器得左边缘，如果属性的轴与内联轴不平行，则 left 的行为类似于 start。|
|right|元素以容器右边缘为基准，一个挨着一个对齐，如果属性轴与内联轴不平行，则 right 的行为类似于 end。|
|**space-between**|**所有flex元素顺着主轴起始线展开，且分布为第一个元素在起始线位置，最后一个元素在终止线位置，其余中间的各个元素距离相等。**|
|**space-around**|**所有元素均匀分布，且每个元素之间的距离相等，第一个元素到起始线的距离，最后一个元素到终止线的距离是各个元素之间距离的一半。**|
|**space-evenly**|**所有元素沿着主轴均匀分布，且第一个元素与起始线的巨鹿，最后一个元素与终止线的距离和各个元素之间的距离完全相等。**|
|stretch|如果元素沿主轴的组合尺寸小于对齐容器的尺寸，任何尺寸设置为 auto 的元素都会等比例地增加其尺寸（而不是按比例增加），同时仍然遵守由 max-height/max-width（或相应功能）施加的约束，以便沿主轴完全填充对齐容器的组合尺寸。|
|safe|如果元素溢出容器，则元素将按照start进行对齐。|
|unsafe|即使元素溢出容器也按照所需的方式对对齐。|

**其中标粗的部分是flex布局常用的属性值**

*Notice:虽然弹性盒子支持 stretch 属性，但将其应用于弹性盒子时，由于拉伸是由 flex 属性控制的，所以 stretch 的行为与 start 相同。*

