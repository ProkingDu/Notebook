# Javascrit异步编程

## 一、异步与同步



### 1.同步编程

提到异步编程的概念首先需要理解同步编程。

实际上我们编写的按照流程处理的代码大多是同步的，同步，也就是代码是按顺序逐条执行的。

浏览器会等待代码的解析和工作，在上一行完成后才会执行下一行。这样做是很有必要的，因为每一行新的代码都是建立在前面代码的基础之上的。

但是这样也会突出一个问题：当前面的代码执行时间过长的时候，会造成后续代码的堵塞，浏览器会等待一个代码块完成执行再执行下面的代码。

典型的例子是函数的执行。
这是一个糟糕的例子：

```javascript
function generate(){
 arr=new Array();
 for(i=0;i<1000000;i++){
     if(i%2==0){
         arr.push(i)
     }else if(i%2==1 || i%2!=0){
          arr.unshift(i);
     }
   }
     console.log(arr);
}
     console.log("finished");
```

当然，这时候只是定义了函数，他还没有被执行，所有在执行这段代码后，他仍然会立马打印finished。
如果在倒数第二行加上：`generate();`
这时候控制台似乎没有响应，实际上是生成这样一个100万个元素的数组需要太长时间了，由于代码是从上至下执行的，必须在函数执行完才会打印finished。
另一个典型的例子是XMLHttpRequest的同步请求：
这又是一段糟糕的代码：

```javascript
     xhr=new XMLHttpRequest();
     xhr.open("GET","http://www.xiaodu0.com",false);
     xhr.send();
     console.log(xhr.responseText);
```

看上去没什么问题，但是如果服务器响应的时间过长，或者服务器出现问题都会导致下面的代码需要等待不可预料的时间才能执行到。

所以同步编程就是代码按照顺序执行，只有上面的代码执行完毕才会执行下一段代码。

### 2. 异步编程

MDN对异步编程的简单描述：

* 通过调用一个函数来启动一个长期运行的操作
* 让函数开始操作并立即返回，这样我们的程序就可以保持对其他事件做出反应的能力
* 当操作最终完成时，通知我们操作的结果。

异步编程，就是执行一个比较耗时的操作，不影响下面的代码执行，而是将作为事务处理，并且在完成后进行相应的回调操作。

### 3. 事件处理程序

> 事件处理程序实际上就是异步编程的一种形式：你提供的函数（事件处理程序）将在事件发生时被调用（而不是立即被调用）。如果“事件”是“异步操作已经完成”，那么你就可以看到事件如何被用来通知调用者异步函数调用的结果的。

典型的例子就是XMLHttpRequest接口，通过发送一个异步请求，并且请求在后台进行处理，当请求完成后调用对应的回调函数（由开发者定义）来完成最终的操作。

事件处理程序实际上就是一个开发者定义的函数，这个函数会被对应的事件调用，例如当一个异步请求完成时调用某个函数来完成业务，这个函数就是事件处理程序，调用函数的过程称为回调。

### 4. 回调

> 事件处理程序是一种特殊类型的回调函数。而回调函数则是一个被传递到另一个函数中的会在适当的时候被调用的函数。回调函数曾经是 JavaScript 中实现异步函数的主要方式。

然而，当回调函数本身需要调用其他同样接受回调函数的函数时，基于回调的代码会变得难以理解。当你需要执行一些分解成一系列异步函数的操作时，这将变得十分常见。

例如，当回调函数还需要调用一个回调函数的时候，当这种情况变多，就会产生很多函数的定义，如果需要对其中的某一个函数的业务进行更改，或者处理他的错误，就需要对每一级回调函数进行处理。

这种难办的回调结构被称为“回调地狱”或者“厄运金字塔”。

由此，现代大多的API都不使用回调，而是通过promise来完成异步操作。

## 二、Promise的基本使用

> Promise 是现代 JavaScript 中异步编程的基础，是一个由异步函数返回的可以向我们指示当前操作所处的状态的对象。在 Promise 返回给调用者的时候，操作往往还没有完成，但 Promise 对象可以让我们操作最终完成时对其进行处理（无论成功还是失败）。

在基于 Promise 的 API 中，异步函数会启动操作并返回 Promise 对象，然后就可以通过将回调函数附加到Promise对象上，当Promise状态改变时，会执行对应的回调函数；

### 1.使用`fetch()`API
> 全局的 fetch() 方法用于发起获取资源的请求。它返回一个 promise，这个 promise 会在请求响应后被 resolve，并传回 Response 对象。

看一个示例：
```javascript
       let pro=fetch("http://promise.cn/test.php",{mode:"cors"})
       console.log(pro);
       pro.then((res)=>{
        console.log(pro);
        console.log(res);
       });
       console.log("已发送请求")
```
通过fetch发起一个异步请求，fetch返回一个promise对象，通过这个promise对象可以扩展到回调函数。
以上代码执行后会首先打印初始的promise对象，因为此时fetch()还没有得到来自url的响应，回调函数不会被调用，初始的peomise对象：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231026/3dadee847f52d22324929d8c23009258.png)
{Pending}代表此时的promise对象是待定状态，即还没有得到响应，响应还未成功也没有失败。
之后，当请求响应之后，pro.then()发挥作用，它会打印出这时候的promise对象：
```javascript
Promise {<fulfilled>: Response}
[[Prototype]]: Promise
[[PromiseState]]: "fulfilled"
[[PromiseResult]]: Response
```
这时候promise对象的状态变成了fulfilled，即已经成功得到响应。
并且回调函数会接收到一切Response对象，包含当前请求响应的信息。

### 2.链式使用promise
在promise执行回调函数时会传递一个Response对象，如果想要获取到Response对象包括的返回内容，需要对Response对象再次使用一次异步操作，如果服务端返回的数据是Json格式的，则调用response对象的json()方法来再次得到一个Promise对象并且异步获得响应内容，如果返回的数据是字符串，则通过text()方法来替换jso()方法。
**注意：Response 对象被设置为stream格式因此他只能被读取一次，即只能对他执行一次读取的方法（并非读取他的属性）如果你需要多次读取，通过clone()方法克隆一个response对象！**
例如，读取返回的json数据：
```javascript
       let pro=fetch("http://promise.cn/test.php")
       pro.then((response)=>{
        let pro2=response.text();
        pro2.then(function(res){
            console.log(JSON.parse(res));
        });
       });
       console.log("已发送请求");
```
服务端:
```
header("Access-Control-Allow-Origin:*");
echo json_encode(["status"=>200,"msg"=> "success"]);
```
控制台输出：
```
header("Access-Control-Allow-Origin:*");
echo json_encode(["status"=>200,"msg"=> "success"]);
```

由于你无法确定后端返回的数据是json还是字符串，所以标准化的接口开发后端应当在响应头返回json数据时声明：
```http
Content-Type:application/json;charset=utf-8
```
有时候后端会省略charser=utf-8。
此时可以通过response对象的header属性来获得对应的header对象，通过header对象获得响应头的Content-Type来决定使用json()还是text()方法。

> 一个 Headers 对象具有关联的标头列表，它最初为空，由零个或多个键值对组成。你可以使用类似于 append() 这样的方法添加（参见示例）到这个对象中。在该接口的所有方法中，标头名称由不区分大小写的字节序列匹配。

可以通过header对象的get()方法来读取响应头中Content-Type的内容。

通过上面的描述，编写一个简单的fetch API模板：
```javascript
     let url="http://promise.cn/test.php";
    // 发起一个promise请求
    let pro=fetch(url);
    pro.then((response)=>{
        // 异步回调
        let header=response.headers;
        // 响应头对象
        let type=header.get("Content-Type");
        if(type === "text/html" || type === "text/html;charset=UTF-8"){
            resPromise=response.text();
        }else if(type === "application/json" || type === "application/json;charset=UTF-8"){
            resPromise=response.text();
        }else{
            resPromise=response.text();
        }

        // 读取响应消息
        resPromise.then(function(e){
            console.log(e);
            // code here
        });
    });
```


实际上应该注意，这个模板仍然是在每个回调函数中进行回调，和之前提到的回调地狱似乎没有区别，所以我们应该注意到：通过json或者text读取promise仍然返回的是一个promise对象，所以可以直接在第一个promise的回调函数中返回新的Promise然后在此函数后进行链式调用Promise，所以可以（也应该）将上面的代码改成这样：
```javascript
let url="http://promise.cn/test.php";
    // 发起一个promise请求
    let pro=fetch(url);
    console.log(pro)
    pro.then((response)=>{
        // 异步回调
        let header=response.headers;
        // 响应头对象
        let type=header.get("Content-Type");
        if(type === "text/html" || type === "text/html;charset=UTF-8"){
            return response.text();
        }else if(type === "application/json" || type === "application/json;charset=UTF-8"){
            return response.text();
        }else{
            return response.text();
        }
    })
    .then(function(e){
        // 读取响应消息
        console.log(e)
    });
```

当前严格来说上面的例子还缺少一个流程：判断响应是否成功，如果不成功应该中断接下来的程序执行，并且抛出错误：
```javascript
let url="http://promise.cn/test.php";
    // 发起一个promise请求
    let pro=fetch(url,{mode:"no-cors"});
    console.log(pro)
    pro.then((response)=>{
        if(!response.ok){
            throw new Error(`HTTP响应码错误：${response.status}`);
        }
        // 异步回调
        let header=response.headers;
        // 响应头对象
        let type=header.get("Content-Type");
        if(type === "text/html" || type === "text/html;charset=UTF-8"){
            return response.text();
        }else if(type === "application/json" || type === "application/json;charset=UTF-8"){
            return response.text();
        }else{
            return response.text();
        }
    })
    .then(function(e){
        // 读取响应消息
        console.log(e)
    });
```

`response.ok` 包含一个布尔值，其表示请求的响应状态，如果响应存在问题则返回false。
`response.status` 包含当前响应的状态码。

### 3.错误处理
Promise提供了`catch()`方法来捕获错误并且交给开发者解决错误。
传统的异步编程方式例如XMLHttpRequest需要在每个回调函数中进行错误处理，而Promise只需要在链式回调中加入catch()即可。
```
// 错误处理
    let f=fetch("http://promise.cn/tejkl.php");
    f.then(function(a){
        console.log(a);
        return a.json;
    }).catch(function(e){
        console.log(e);
    });
```
如果将catch注册到Promise链式调用的末尾，那么任何回调产生错误都会被catch捕获到。

### 4.Promise的状态
Promise一共有三种状态，分别是：
* pending 待定状态，此时Promise刚刚被产生，还没有得到响应。
* fulfilled 已兑现状态，此时Promise已经得到正确的响应并且没有产生错误，对应的这时候then()会被调用。
* rejuected 已拒绝状态，这时候意味着操作失败。当一个 Promise 失败时，它的 catch() 处理函数被调用。

注意，这里的“成功”或“失败”的含义取决于所使用的 API：例如，fetch() 认为服务器返回一个错误（如404 Not Found）时请求成功，但如果网络错误阻止请求被发送，则认为请求失败,即如果服务器响应了 但是返回了一个错误的状态码，这时候仍然是已兑现的状态。

有时我们用 已敲定（settled） 这个词来同时表示 已兑现（fulfilled） 和 已拒绝（rejected） 两种情况。

如果一个 Promise 处于已决议（resolved）状态，或者它被“锁定”以跟随另一个 Promise 的状态，那么它就是 已兑现（fulfilled）。

### 5.合并多个Promise

有两种常用的方法来合并多个Promise。
#### (1).promise.all()
Promise.all()接受一个Promise组成的数组，当且仅当数组内的Promise对象全部为已兑现状态，promise才会调用接下来的then方法，如果有一个fetch是被拒绝的，那么就会调用catch()并返回相应的错误。

示例：
```javascript
pro1=fetch("http://www.xiaodu0.com",{mode:"cors"});
pro2=fetch("http://promise.cn/test.php",{mode:"cors"});
Promise.all([pro1,pro2]).then(
    function(e){
        for(x of e){
          console.log(x.url+" status："+x.status)
        }
    }
).catch(function(e){
    console.log(e);
});
```

如果发起一个错误的请求：
```javascript
pro1=fetch("http://www.xiaodu0.com",{mode:"cors"});
pro2=fetch("error://promise.cn/test.php",{mode:"cors"});
Promise.all([pro1,pro2]).then(
    function(e){
        for(x of e){
          console.log(x.url+"  status："+x.status)
        }
    }
).catch(function(e){
    console.log("请求失败，错误在:"+e);
});
```

则会输出错误的请求的错误信息。

 #### (2).promise.any()
 > Promise.any() 静态方法将一个 Promise 可迭代对象作为输入，并返回一个 Promise。当输入的任何一个 Promise 兑现时，这个返回的 Promise 将会兑现，并返回第一个兑现的值。当所有输入 Promise 都被拒绝（包括传递了空的可迭代对象）时，它会以一个包含拒绝原因数组的 AggregateError 拒绝。

 与Promise.all()相反，Promise.any只要有一个promise的状态是已兑现就会响应，而只有所有promise 都是已拒绝的时候才会调用catch();

 看一个示例：
 ```
 let proa=fetch("http://promise.cn/source2.php",{mode:"cors"});
let prob=fetch("http://promise.cn/source1.php",{mode:"cors"});
let proc=fetch("http://nopromise.cn/source.php",{mode:"cors"});
Promise.any([proa,prob,proc]).then(
    function(e){
        console.log(e.url+" 请求成功。");
    }
).catch((e)=>{
    for (x of e){
       console.log(x.url+" 请求失败，原因"+x); 
    }
});
 ```

 我在source.php 返回了404，但是Promise仍然在proa响应的时候打印了请求成功，因为即使是404 promise仍然得到了服务器的响应，所以是已敲定状态，而当any()时，只要有一个Promise响应成功了，就不在等待其他的响应如果我将这三个地址都改成无法连接的地址：
 ```javascript
 let proa=fetch("http://nopromise.cn/source2.php",{mode:"cors"});
let prob=fetch("http://nopromise.cn/source1.php",{mode:"cors"});
let proc=fetch("http://nopromise.cn/source.php",{mode:"cors"});
Promise.any([proa,prob,proc]).then(
    function(e){
        console.log(e.url+" 请求成功。");
    }
).catch((e)=>{
    for (x of e){
       console.log(x.url+" 请求失败，原因"+x); 
    }
});
 ```
 Promise.any()会调用catch()并且给出：
> AggregateError: All promises were rejected


### 6.使用async与await
通async与await可以像编写同步代码一样编写异步函数。
首先在函数定义前使用async关键字，然后在函数内调用的返回promise的函数之前使用await，函数就会等待fetch()执行完成再返回内容，并且函数的返回值是一个Promise对象。
假设我需要从服务端获取一些用户的数据，并且通过async与await实现异步操作：
```javascript
async function getUser(){
    try{
        let res=await fetch("http://promise.cn/user.php",{mode:"cors"});
        if(!res.ok){
            throw new Error("请求失败，HTTP响应："+res.status);
        }
        let json=await res.json();
        console.log("用户数据获取成功！");
        console.log(json);
    }
    catch (error){
        console.log("失败："+error);
    }
}

getUser();
```
**在函数内调用返回值为Promise的对象一定要使用await**
值得注意的是：
**由于Promise只有在服务器拒绝的时候才调用catch，而如果服务器响应了请求，但是状态码不是200让仍然会调用then，所以我们可以在then中通过response.ok来判断响应是否正确，如果不正确则抛出错误，这时候promise的catch仍然能够捕获到错误**
上面的例子输出：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231028/6160952c40fedf578677ebe699b15ecd.png)

如果你在定义的异步函数中返回await的值，它仍然是会返回一个Promise对象，而非和函数内一样返回的是异步处理之后的值。
例如 上面的代码中的``let json=await res.json()`` 虽然在函数内他是异步的json，但是如果你在函数中`return json` 在之后得到的值仍然是一个Promise对象，其实就是，函数的执行是异步的，但是函数的返回是同步的，当你执行：
```
let user=getUser();
console.log(user);
```
时，控制台会立即打印一个pending状态的Promise。

所以我们可以取得定义的异步函数的返回值继续进行promise的操作。
如果上面的例子我想要在函数之后进行将用户数据输出在页面中：
```javascript
async function getUser(){
    try{
        let res=await fetch("http://promise.cn/user.php",{mode:"cors"});
        if(!res.ok){
            throw new Error("请求失败，HTTP响应："+res.status);
        }
        let json=await res.json();
        return json;
    }
    catch (error){
        console.log("失败："+error);
    }
}
let data=getUser();
data.then(function(e){
    for(x of e){
        document.write(x.id+"：");
        for(y in x){
            document.write(`${y}:${x[y]} &nbsp;&nbsp;&nbsp;`);
        }
        document.write("<br>");
    }
})
```

当然这种方法实际上并不是最合适的，但是实现目的的路不止一条，我们可以选择最容易的那条。
运行结果：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231028/966dc05fdb6e0415c81656ef4dd92e17.png)