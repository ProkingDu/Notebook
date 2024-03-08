# 10-11手记

### 1.HTTP 返回状态码304 Not Modified

#### 描述

在客户端向服务端发送http请求时，若返回状态码为304 Not Modified 则表明此次请求为条件请求。在请求头中有两个请求参数：If-Modified-Since 和 If-None-Match。

当客户端缓存了目标资源但不确定该缓存资源是否是最新版本的时候, 就会发送一个条件请求。在进行条件请求时,客户端会提供给服务器一个If-Modified-Since请求头,其值为服务器上次返回响应头中Last-Modified值,还会提供一个If-None-Match请求头,值为服务器上次返回的ETag响应头的值。


服务器会读取到这两个请求头中的值,判断出客户端缓存的资源是否是最新的,如果是的话,服务器就会返回HTTP/304 Not Modified响应头, 但没有响应体.客户端收到304响应后,就会从本地缓存中读取对应的资源。 所以：当访问资源出现304访问的情况下其实就是先在本地缓存了访问的资源。
首次访问一个资源的头：

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231011/6d0d6028c9bf2acbb51fd7d4c529d161.png)

第二次访问，此时已经缓存资源：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231011/5a27bd08084b4393f1ea168645347c5b.png)
返回状态码变成了304 Not Modified

同时在请求头中会多出:
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231011/e4c2153d25ce7d15778e5043e0ec9f42.png)

响应头也会产生相应变化，例如Content-type将不会被返回，而是使用本地缓存。
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231011/887dc39924ed16d6b805f321353a8b31.png)

#### 解决方法
只需要在访问链接后面加上随机参数即可。
例如在访问的链接后加上一个？即可重新请求资源，但是每次的参数都必须不一样。


另一种解决方案是禁用浏览器缓存，勾选**停用缓存**：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231011/1c39d28fd793fe9907858a49fe0dae84.png)