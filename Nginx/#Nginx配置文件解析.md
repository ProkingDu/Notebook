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
### 1.worker_processes
worker_process表示nginx启动时启动多少个worker进程，与机器的CPU内核有关。

### 2.work_connections
worker_connections指定每个工作进程最多接受的连接数、

### 3.include       mime.types
引入http的mime-types配置文件，配置文件位于：
```
/usr/local/nginx/conf/mime.types
```
mime.type定义请求的不同文件后缀在http响应头中对应的Content-type