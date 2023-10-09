
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
                                ``
                                `
