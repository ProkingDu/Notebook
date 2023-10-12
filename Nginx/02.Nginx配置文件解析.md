# Nginx最小配置文件解析

## 一、Nginx的最小配置文件
Nginx安装后默认的配置文件，去除注释内容之后的配置文件就是最小配置文件。
如下所示：
```Nginx

worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;

    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;


        location / {
            root   html;
            index  index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
    
    server {
       listen       8000;
       server_name  test;

       location / {
           root   html1;
           index  index.html index.htm;
       }
    }

}

```
核心配置：
### (一)、http模块
#### 1.worker_processes
worker_process表示nginx启动时启动多少个worker进程，与机器的CPU内核有关。

#### 2.work_connections
worker_connections指定每个工作进程最多接受的连接数、

#### 3.include       mime.types
引入http的mime-types配置文件，配置文件位于：
```
/usr/local/nginx/conf/mime.types
```
mime.type定义请求的不同文件后缀在http响应头中对应的Content-type，浏览器根据这个Content-Type来决定如何对请求的资源操作。
例如当Content-Type为text/html，浏览器会在窗口中解析文件中的html代码，如果是image/png则表示当前资源是一个png格式的图像，浏览器会打开此图像。
如果是其他浏览器无法打开的资源，它就会对其进行下载。
<br>
而这些文件后缀对应如何返回Content-type，就取决于mime.types配置文件。
在mime.types(部分)中：
```
    text/html                                        html htm shtml;
    text/css                                         css;
    text/xml                                         xml;
    image/gif                                        gif;
    image/jpeg                                       jpeg jpg;
    application/javascript                           js;
    application/atom+xml                             atom;
    application/rss+xml                              rss;
```

默认的部分配置文件如下，前面对应的就是返回的Content-type，后面是返回这个响应的文件名。
可以对它进行改动,例如更改html为image/png，则用户端访问html资源都会被浏览器解析成png图像并打开，显然这是无法正常打开的。
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231011/63d8ce08b905a2775e58d7f30a71f69a.png)

如果是没有定义mime.type的资源，会被默认当做二进制流处理，例如创建一个空的test.xiaodu并访问，响应内容：
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231011/0f8ddaae9b0df11d1b00e057f979c439.png)
对于Content-Type为二进制的文件，浏览器会对其进行下载。

再测试一下，将html文件的mime.type改成applicataion/octet-stream
![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231011/7c0a7f6c9f24417a508595d7d7db8440.png)

返回二进制流，浏览器会直接洗下载html而不是解析到窗口显示。

#### 4.default-type
default-type即在mime.type中没有对应配置时，默认的返回的Content-Type，他的默认值是`application/octet-stream`。


#### 5.sendfile
sendfile指定Nignx如何向客户端发送资源，sendfile为on(默认值),则nginx通过请求操作系统的网络接口直接向用户发送资源，如果是off，则Nginx通过IO读取文件之后，将副本发送给用户。
一般情况下sendfile为on时响应速度更快，且直接通过系统发送资源不会触发文件锁，如果sendfile为off，则Nginx会对请求的文件进行读取，然后将文件写入到缓冲区发送，可能会由于文件锁导致一系列问题的产生。

#### 6.keepalive_timeout
keepalive_timeout指定连接的超时时间，分别对应客户端和代理端，暂时不做详细讲解，在反向代理部分比较重要。

### （二）、server模块
**server模块可以看作虚拟主机（vitual host）即vhost，在Nginx配置文件中可以指定多个server模块，每个server模块代表一个虚拟主机。**
#### 1.listen
指定当前主机监听的端口，通过端口可以区分不同的主机，对应不同的根目录，同时也可以在server_name中指定域名而不区分端口来区分不同主机。

#### 2.server_name
定义了当前虚拟主机的域名或者主机地址，默认的虚拟主机是localhost，在本地的host文件中将localhost指定了127.0.0.1因此localhost可以被解析，同样的可以定义其他的主机名并在host文件中指定主机名对应的地址。

#### 3.location
location指定虚拟主机的地址，在用户端即访问的URI，在服务端即当前虚拟主机的根目录。
##### （1）.root

      指定站点的运行目录

#####  （2）.index
    指定当前主机的默认首页文件。

#### 4.error_page
指定错误文件的路径
