## 一、简介

C 语言支持数组数据结构，它可以存储一个**固定大小的相同类型元素的顺序集合**。数组是用来存储一系列数据，但它往往被认为是一系列相同类型的变量。

所有的数组都是由**连续的内存位置**组成。最低的地址对应第一个元素，最高的地址对应最后一个元素。

![](https://www.runoob.com/wp-content/uploads/2014/09/c-arrays-2021-1-18-3.png)


## 二、声明数组
通过：

`type name[length] = {value1,value2,value3.....}`

声明一个数组。

其中type为数组元素的数据类型，name为数组变量名，length为数组长度，其后的等于号和大括号是可选的，用于对数组进行初始化赋值。

例如：
```
    int age[10];
    age[0]=10;
    age[1]=255;
    printf("%d",age[1]);
```

等同于：
```
    int age[2]={10,255};
    printf("%d,%d",age[1],age[0]);
```

数据的类型可以是任何基础数据类型，但是你不可以再其中储存其他类型的数据。

```
    int age[2]={10,"1"};
    printf("%d,%d",age[1],age[0]);
```

即使他不一定会报错，但是你会得到一个意向不到的值：

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231205/8db822256075f16c0619daa193023e1d.png)

当你的给数组初始化赋值的长度小于给定的数组长度时，后面没有被赋值的索引默认为0：

```
    int age[5]={10,1};
    printf("%d,%d",age[1],age[4]);
```

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231205/c2aec56b806e4d85115a50302a9ceef6.png)

如果你在声明数组时给所有的数组元素初始化值。可以不指定数组的长度，通过sizeof来尝试一下：
```
    int age[]={18,19,20,21,25};
    printf("%d,%llu",age[1],sizeof(age));
    return 0;
```

由于sizeof返回的是数组的长度而不是元素的个数，所以得到的值应该是20：

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231205/77642515d8b0473ebef478a686d37198.png)

每个int的长度是4！

显而易见，当我把int更换成double之后得到的长度是40，由于一共有五个元素且每个双精度浮点数占据8个字节。

如果我想要得到数组占据的元素个数，通过如下方法：
```c
    double age[]={18,19,20,21,25};
    printf("数组的长度是：%llu",sizeof(age)/sizeof(age[1]));
    return 0;
```

通过宏定义自定义一个计算数组元素个数的函数：
```c
    double age[]={18,19,20,21,25};
    char name[]={'p','r','o','k','i','n','g'};
    printf("双精度浮点数组的元素个数是：%llu，char数组的元素个数是：%llu", LENGTH(age), LENGTH(name));
    printf("\n%s",name);
```

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231205/e6439da1b7f209f594ebaff377347d9f.png)


## 三、访问数组元素
