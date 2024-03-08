在uniapp跨页面传数据，主要通过`sessionStorage`和`localStorage`实现。

实际上这两种方法都是基于window对象的标准api。

此前我曾经尝试使用cookie储存数据：
```
Vue.prototype.addCookie = function (name,value){

	if(Boolean(document.cookie)==false || document.cookie=="" || document.cookie==null || document.cookie == 'null'){
		let data={};
		this.$set(data,name,value);
		let d = new Date();
		d.setTime(d.getTime()+(1*24*60*60*1000));
		let expires = "expires="+d.toGMTString();
		document.cookie=JSON.stringify(data)+";"+expires;
		return true;
	}
	let data=JSON.parse(document.cookie.split(";")[0]);
	this.$set(data,name,value);
	let d = new Date();
	d.setTime(d.getTime()+(1*24*60*60*1000));
	let expires = "expires="+d.toGMTString();
	document.cookie=JSON.stringify(data)+";"+expires;
}
```

但是使用Cookie在页面间传递数据是一种低级且不明智的选择，因为浏览器对客户端cookie的支持性不是很强，通过cookie来储存数据需要封装大量复杂的代码，且不便于操作。

当然在很多方面cookie的优势很大，但是就我现在做的业务而言使用更加良好的windowAPI是更好的选择。

## 概述
Web Storage API 提供了存储机制，通过该机制，浏览器可以安全地存储键值对，比使用 cookie 更加直观。

存储对象是简单的键值存储，类似于对象，但是它们在页面加载时保持完整。键和值始终是字符串（请注意，与对象一样，整数键将自动转换为字符串）。

所以注意，如果需要在Storage中储存复合类型的数据，必须将其转为JSON字符串来储存（由于键值对都要是字符串）

localStorage与localStorage都是window下的对象（更确切的说，在支持的浏览器中 Window 对象实现了 WindowLocalStorage 和 WindowSessionStorage 对象并挂在其 localStorage 和 sessionStorage 属性下），二者的功能相同，都是为每一个给定的源（given origin）维持一个独立的存储区域。

在这个储存区域没有被释放之前，你都可以随时访问通过这两个对象来获得你所储存的键值对。

关于释放，则是localStorage与sessionStorage最直接的不同，localStorage将资源一直储存在浏览器内存区域中，除非用户手动将他清除，否则他会一直存在。而sessionStorage则只存在于当前会话，一旦窗口的生命周期结束了（退出浏览器和关闭窗口），sessionStorage都会被清除。


无论是localStorage还是sessionStorage他们所返回的都是一个Storage对象，但是他们都是独立存在的，相互不受影响。

## 可用性

支持 localStorage 的浏览器将在窗口对象上具有一个名为 localStorage 的属性。但是，仅断言该属性存在可能会引发异常。如果 localStorage 确实存在，则仍然不能保证 localStorage 实际可用，因为各种浏览器都提供了禁用 localStorage 的设置。因此，浏览器可能支持 localStorage，但不适用于页面上的脚本。

例如，私有浏览模式下的 Safari 浏览器为我们提供了一个空的 l ocalStorage 对象，其配额为零，实际上使它无法使用。相反，我们可能会收到合法的 QuotaExceededError，这意味着我们已经用完了所有可用的存储空间，但实际上存储空间可用。我们的功能检测应考虑这些情况。

检测Storage是否受支持：

```javascript
function storageAvailable(type) {
  var storage;
  try {
    storage = window[type];
    var x = "__storage_test__";
    storage.setItem(x, x);
    storage.removeItem(x);
    return true;
  } catch (e) {
    return e;
  }
}
```

以上示例通过try尝试实例化给定的storage类型，如果能够成功执行添加键值对和删除键值对则返回true,否则返回不能使用storage的原因。


## 使用Storage添加和更新键值对



使用storage将键值对写入本地储存：

```javascript
localStorage.setItem(key,value);
sessionStorage.setItem(key,value);
```

注意key和value都应当是字符串类型的数据。

例如在不同的页面传递数据，用户在A页面输入手机号和验证码，在B页面需要得到A页面输入的手机号和验证码，使用Storage来储存是非常良好的方法。

由于键值对需要是字符串的形式，所以要将手机号和验证码保存为一个对象并且通过JSON的格式储存：

```js
localStorage.setItem("data",JSON.stringify({phone:13333333333,code:999999}));
sessionStorage.setItem("data",JSON.stringify({phone:13333333333,code:999999}));
```

localStorage和sessionStorage择一即可。

如果添加的键已经存在则会更新他的值。

## 取得键值对数据

在B页面取得数据：
```js
let data=window.sessionStorage.getItem("data");
data=JSON.parse(data);
```

取得数据使用`getItem()`方法，参数为键名，返回对应的值。

## 删除键值对数据

通过`removeItem()`来删除键值对，参数为要删除的键名。

或者通过`clear`来清楚当前域名下的所有键值对数据，这个方法不需要参数，而是将Storage储存的所有键值对都删除。

例如：
```js
sessionStorage.removeItem("username");   //删除键为username的数据
sessionStorage.clear();    //清除所有数据
```

## 取出键名

通过`key()`方法可以返回指定位置的键名，参数为索引位置。

如果对应位置不存在一个键值对则返回null，否则返回此位置下的键名。

同时你还可以通过`Storage.length`来取得当前storage的一共储存了多少键值对。

所以可以封装一一个列出所有储存的键的方法：
```js
function getAllKeys(type){
    let storage=window[type];
    let len=storage.length;
    let keys=new Array();
    for(let i=0;i<len;i++){
        keys.push(storage.key(i));
    }
    return keys;
}
```

![小杜的个人图床](http://src.xiaodu0.com/2023/12/24/17d5790ab382b51ab82c55b70a74e4ec.png)

