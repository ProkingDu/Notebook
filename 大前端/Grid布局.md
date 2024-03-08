## 概述
CSS 网格是一个用于 web 的二维布局系统。利用网格，你可以把内容按照行与列的格式进行排版。另外，网格还能非常轻松地实现一些复杂的布局。

网格是由一系列水平及垂直的线构成的一种布局模式。根据网格，我们能够将设计元素进行排列，帮助我们设计一系列具有固定位置以及宽度的元素的页面，使我们的网站页面更加统一。

一个网格通常具有许多的列（column）与行（row），以及行与行、列与列之间的间隙，这个间隙一般被称为沟槽（gutter）。

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231126/dedd031fb7bad92cdf698d1757f38309.png)

## 创建网格布局
对于某个容器指定`display:grid`即指定此元素下的内容排列为网格布局。
就像这样：
html
```
<div class="container">
        <div class="one">
            一
        </div>
        <div class="two">
            二
        </div>
        <div class="three">
            三
        </div>
        <div class="four">
            四
        </div>
    </div>
```

css
```
 .container{
            display: grid;
}
```

在指定网格布局之后元素仍然是按照默认的文档流排列，因为目前没有对网格划分行列。

## 为网格划分行列

通过grid-template-colums和grid-template-rows划分行列的布局称为显式的网格布局。

### 通过`grid-template-columns`划分列
通过`grid-template-columns`属性为网格布局指定列的长度。
可能得值：
一切width属性支持的值，且存在grid布局特有的值：
* fr单位：按照fr指定的比例分配剩余的空间，当外层用一个 minmax() 表示时，它将是一个自动最小值（即 minmax(auto, <flex>)）。
* minmax(min,max)方法：定义网格范围应在[min,max]区间内。

例如，以下网格将容器第一列划分为100px，第二列为30%，第三列和第四列按照2:5的比例划分剩下的空间：
```
 .container{
            display: grid;
            grid-template-columns:100px 30% 2fr 5fr;
        }
```
在浏览器中表现为：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231126/93e62140d2d0b78bc1fb4c4ab9b397ca.png)

网格布局的容器中的子元素会按照grid-template-column指定的列数量排序，倘若只指定了三列的宽度，但是有五个子元素，则多出的元素会被移动到下一行。

### 通过`grid-template-rows`划分行

grid-template-rows 该属性是基于 网格行 的维度，去定义网格线的名称和网格轨道的尺寸大小。

就像这样：
```html
<div class="container">
        <div class="row">1</div>
        <div class="row">2</div>
        <div class="row">3</div>
        <div class="row">4</div>
        <div class="row">5</div>
    </div>
```

```css
 .container{
            display: grid;
            grid-template-rows: 1fr 2fr 2fr 2fr 3fr;
            height: 500px;
        }
        .row{
            background-color: red;
            border: 1px solid #666;
            text-align: center;
        }
```

得到的内容：
![小杜的个人图床](http://src.xiaodu0.com/2023/12/17/f6d2f34cfd294cd4c6753dc366314af2.png)

`grid-template-rows`规定了在显式网格布局中各行的值。
他的值与grid-template-columns可能得值相同。

### 使用repeat
repeat()用于减少声明多个网格布局所需要编写的相同代码。
```css
repeat(num,size)
```

* num 重复声明的数量
* size 行/列的长度

声明一个9*9且单元格宽高都为50px的网格：
```css
.container1{
            display: grid;
            grid-template-rows:repeat(9,50px);
            grid-template-columns:repeat(9,50px);
        }
        .coll::after{
            content: "coller";
        }
        .coll{
            background-color: aquamarine;
            text-align: center;
            border:0.5px inset #999
        }
```

结果：
![小杜的个人图床](http://src.xiaodu0.com/2023/12/17/7ee6414fef7092fe03804745732d6c39.png)


## 隐式网格布局与显式网格布局

当仅使用`grid-template-columns`创建网格布局的列时，布局的行会自动声明为适应的行，这个没有被手动声明的行就是隐式的行。

如果你在定义的网格外放置内容，或者由于内容太多，需要更多的网格轨道，那么网格就会在隐式网格中创建行和列。默认情况下，这些轨道会自动调整大小，因此它们的大小取决于轨道内的内容。

你还可以使用 `grid-auto-rows` 和 `grid-auto-columns` 属性为在隐式网格中创建的轨道定义设定大小。

以上表示，当布局中的元素多于预设时，这个多余的元素会根据`grid-auto-rows`和`grid-auto-colums`来决定样式。

例如，对以上的9*9布局扩展为12*12但是仍然只指定9个行列，要求多出的元素宽高都是100px:
```css
.container1{
     display: grid;
     grid-template-rows:repeat(9,50px) auto;
     grid-template-columns:repeat(9,50px);
     grid-auto-rows:50px;
     grid-auto-columns:50px;
}
```

![小杜的个人图床](http://src.xiaodu0.com/2023/12/17/eca0aa5940cdca657a739c06200d2b75.png)

未达到预期：因为当指定列的数量时每一行超出的列都会被放置在下一行 所以应当在显式的声明最后指定auto。

## 轨道大小和minmax

在设置显式网格或定义自动创建的行或列的大小时，我们可能希望给轨迹一个最小尺寸，但也要确保它们能扩展以适应添加的任何内容。例如，我可能希望我的行永远不会缩小到 100 像素以下，但如果我的内容高度扩展到 300 像素，那么我希望行也能扩展到这个高度。

网格布局提供了 `minmax()` 函数来解决这个问题。

CSS函数 `minmax()` 定义了一个长宽范围的闭区间，它与CSS 网格布局一起使用。

此函数包含两个参数，最小值 和 最大值.

每个参数分别是<length>、<percentage>、<flex>的一种，或者是max-content、min-content、或auto之一。

如果 最大值 < 最小值，则最大值被忽略并且 minmax(最小值, 最大值) 被看成最小值。<flex> 值作为最大值时设置网格轨道的弹性系数；作为最小值时无效。

## 网格线

### 关于网格线
默认下我们创建的网格布局定义的是网格轨道而非网格线，网格线即交叉在每个网格轨道中的交叉线。

网格布局会为我们创建编号的网格线来让我们来定位每一个网格元素。例如下面这个三列两行的网格中，就拥有四条纵向的网格线。

![小杜的个人图床](http://src.xiaodu0.com/2023/12/17/8508ea72aeee20556adabbb8e25a39c7.png)

网格线的编号顺序取决于文章的书写模式。在从左至右书写的语言中，编号为 1 的网格线位于最左边。在从右至左书写的语言中，编号为 1 的网格线位于最右边。网格线也可以被命名。

### 基于网格线放置项目
先前的所有项目都是在网格布局确定下，自动排列单元格项目，通过网格线的概念引出基于网格线布局项目。

比如，我想要将某个单元格放置在网格布局中的某行某列，通过网格线来实现定位是一个绝佳的方法。

网格线布局有如下四个属性：
* `grid-row-start` 指定元素开始的行标线
* `grid-row-end` 指定元素结束的行标线
* `grid-column-start` 指定元素开始的列标线
* `grid-column-end` 指定元素结束的列标线

示例：
```html
    <div class="container3">
        <div class="coll3"></div>
        <div class="coll3"></div>
        <div class="coll3"></div>
        <div class="coll3"></div>
        <div class="coll3"></div>
        <div class="coll3"></div>
        <div class="coll3"></div>
        <div class="coll3"></div>
        <div class="coll3"></div>
        <div class="coll3 special"></div>
    </div>
```

```css
.container3{
            display: grid;
            grid-template-columns: repeat(3,50px);
            grid-template-rows: repeat(3,50px);
            grid-auto-rows:30px;
        }
        .coll3{
            background-color:blueviolet;
            border:1px solid brown;
        }
        .special{
            z-index: 2;
            background-color: red !important;
            grid-column-start: 1;
            grid-column-end: 2;
            grid-row-start: 1;
            grid-row-end: 4;
        }
```

结果：
![小杜的个人图床](http://src.xiaodu0.com/2023/12/17/b4794ab888b19a05cb95268e14c47803.png)

**注意：网格线开始的位置是1，结束的位置是网格轨道+1**

## 网格单元

网格单元（grid cell）是网格项中最小的单位，从概念上来讲其实它和表格的一个单元格很像。现在再看回我们前面的一个例子，一旦一个网格元素被定义在一个父级元素当中，那么它的子级元素将会排列在每个事先定义好的网格单元中。

上面的所有示例中的单元格都是一个网格单元。

## 网格区域

项目可以按行或列跨越一个或多个单元格，这样就形成了一个网格区域（grid area）。网格区域必须是矩形的（例如不能创建 L 形区域）。

网格区域即通过网格线定义的单独定位的单元格区域，上一个示例的紫色单元格附近的红色区域就是一个网格区域。

## 网格间距
网格单元格之间的横向间距（gutter）或纵向间距（alley）可以使用 `column-gap` 和 `row-gap` 属性或简写 `gap` 来创建。
例如在9*9的网格布局中指定网格间距为5px：
```css
gap:5px;
```
![小杜的个人图床](http://src.xiaodu0.com/2023/12/17/bd55192dcdf9d1840111364ca2c30c87.png)

## 单元格层级
如果通过网格线定位或者嵌套单元格，可能会导致两个单元格在同一个位置，而我们需要决定哪个单元格显示在上方，应当通过`z-index`属性来定义元素层级。

`z-index`属性接受一个整数值，数值越大则元素层级越大，层级较大的元素会优先在上层显示。、

`z-index`不仅可以用在网格布局中，在全局都可以使用，例如两个部分重叠的元素，将其中一个元素显示在上方:
```html
<div class="one">
        我在下面
    </div>
    <div class="two">
        我在上面
    </div>
```
```css
        .one{
            width: 500px;
            height: 300px;
            z-index: 11;
            background-color: red;
        }
        .two{
            width: 500px;
            height: 300px;
            background-color: rgba(0, 0, 236, 0.7);
            position: relative;
            bottom: 100px;
            z-index: 5;
            color:white;
        }
```
效果：
![小杜的个人图床](http://src.xiaodu0.com/2023/12/17/7efd470b694133b5833ab4520ed3dc3e.png)