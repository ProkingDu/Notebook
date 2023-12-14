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
