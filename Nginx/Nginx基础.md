# Nginx 基础

## 一、安装nginx

### 1.软件包

Nginx依赖如下：

*   pcre
*   zlib
*   openssl
*   Nginx

> NGINX通过pcre进行正则表达式匹配，所以需要在LInux安装pcre库，使用zlib对文件进行gzip压缩，并且如果需要Nginx支持https就需要openssl

#### 安装pcre

下载软件包：

```Linux
wget http://downloads.sourceforge.net/project/pcre/pcre/8.37/pcre-8.37.tar.gz
```

下载完成之后解压文件 通过：
`tar -zxvf 目标文件名 -C 目标目录`

执行解压命令：
`tar -zxvf 	 -C usr/pcre`

执行`./configure`进行编译

执行`make && make install` 进行安装

#### 安装openssl

下载OpenSSL的地址:
[openssl](http://distfiles.macports.org/openssl/)

1）解压文件， 回到 openssl目录下，

2）./configure 完成后，

3）执行命令： make && make install

#### 安装zlib

通过阿里云镜像站下载：
[zlib rpm包](https://mirrors.aliyun.com/centos/8.5.2111/BaseOS/x86_64/kickstart/Packages/zlib-1.2.11-17.el8.i686.rpm?spm=a2c6h.13651111.0.0.61bd2f70G1qsTE\&file=zlib-1.2.11-17.el8.i686.rpm)

1.  下载zlib

    curl -o zlib.rpm <https://mirrors.aliyun.com/centos/8.5.2111/BaseOS/x86_64/kickstart/Packages/zlib-1.2.11-17.el8.i686.rpm?spm=a2c6h.13651111.0.0.61bd2f70G1qsTE&file=zlib-1.2.11-17.el8.i686.rpm>

2.  安装zlib

    rpm -i zlib.rpm --force --nodeps

因为可能由于缺少依赖导致zlib安装失败 所以使用 `--force --nodeps` 忽略依赖强制安装。

#### 安装nginx

`yum install nginx`

### 2.启动nginx

通过yum安装nginx之后需要找到nginx的安装目录：

`whereis nginx`

结果：

    nginx: /usr/sbin/nginx /usr/lib64/nginx /etc/nginx /usr/share/nginx /usr/share/man/man3/nginx.3pm.gz /usr/share/man/man8/nginx.8.gz

第一个目录是nginx可执行文件的目录。

`cd /usr/sbin`

启动nginx：`nginx`

启动之后查看进程：`ps -ef | grep nginx`

![nginx进程](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694255583-image-1024x115.png)

接下来即可输入IP访问首页（不需指定端口因为默认端口为80）\ <br>

### 3.Nginx的常用命令

**注意：在使用nginx命令之前必须将当前目录切换到nginx可执行目录下。**

1.  查看版本：`nginx -v`

```Linux
[root@ecs-4a4c sbin]# nginx -v
nginx version: nginx/1.20.1
```

1.  关闭nginx `nginx -s stop`
2.  重新加载nginx：`nginx -s reload`
3.  优雅地退出：`nginx -s quit` 退出前完成所有的链接。

***

<br>

### 4.Nginx配置文件

#### (11).查看Nginx配置文件

​	不同方式安装的nginx目录可能都不同，因此需要通过命令来查找nginx文件，这里使用yum方式安装nginx，默认nginx的配置文件nginx.conf是在/etc/nginx/nginx.conf。

​	如果不知道nginx的配置文件 可以通过`nginx -t`命令来检索Nginx配置文件是否正常，同时获得nginx配置文件的位置。

​	![image-20230910004136045](C:\Users\28110\AppData\Roaming\Typora\typora-user-images\image-20230910004136045.png)

#### b.Nginx配置文件的组成

Nginx的配置文件有三个主要部分：

*   全局块
*   events部分
*   http部分

去掉Nginx安装之后的默认注释部分，默认的Nginx配置为：

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
    }

##### 全局块

其中Events上方的内容是全局的核心配置部分，例如上方worker\_processes 表示最大并发处理数，我在阿里云镜像中下载的Nginx默认使用的是auto表示自动决定。

同时还有其他的配置项：

    user nginx
    # 指定运行Nginx的用户，默认为Nginx。
    error_log /var/log/nginx/error.log;
    #错误日志存放路径
    pid /run/nginx.pid;
    # pid 存放路径
    ......

##### events块

events 块涉及的指令**主要影响 Nginx 服务器与用户的网络连接，常用的设置包括是否开启对多 work process 下的网络连接进行序列化，是否 允许同时接收多个网络连接，选取哪种事件驱动模型来处理连接请求，每个 word process 可以同时支持的最大连接数等。**
上述例子就表示每个 work process 支持的最大连接数为 1024.
这部分的配置对 Nginx 的性能影响较大，在实际中应该灵活配置。

##### http块

http块是实现web业务的主要配置文件，其中包括http全局块和server块。

http块包括：http全局块配置的指令包括文件引入、MIME-TYPE 定义、日志自定义、连接超时时间、单链接请求数上限等。

server块：和虚拟主机有密切关系，虚拟主机从用户角度看，和一台独立的硬件主机是完全一样的，该技术的产生是为了 节省互联网服务器硬件成本。

同时在Server块中又可以包含多server全局块和多个location块，location块的主要作用是基于 Nginx 服务器接收到的请求字符串（例如 server\_name/uri-string），对虚拟主机名称 （也可以是IP 别名）之外的字符串（例如 前面的 /uri-string）进行匹配，对特定的请求进行处理。 地址定向、数据缓 存和应答控制等功能，还有许多第三方模块的配置也在这里进行。

##### 总结

Nginx的配置文件结构：

```
Nginx
	└─Ngixn全局块
    ├─Events块
    │  └─...主要的Event配置
    ├─http块
    │  ├─http全局块
    │  └─Server块
    │      ├─location块
    │      └─server全局块
   
```

##### 补充&#x20;

对于开启nginx后无法访问的情况，应当考虑防火墙是否关闭。

关闭防火墙：

```ssh
systemctl stop firewalld.service
```

阻止防火墙开机自启动：

    systemctl disable firewalld.service

放行端口：

    firewall -cmd --zone=public --add-port=80/tcp --permanent

重启防火墙：

    firewall -cmd --reload

### 5. 创建系统服务

默认安装后nginx没有注册到系统服务，也没有添加启动项，这时候重启服务器nginx不能自动启动。

1.  创建系统服务配置文件

    vi /usr/lib/systemd/system/nginx.service

2.写入文件内容

    [Unit]
    Description=The nginx HTTP and reverse proxy server
    After=network-online.target remote-fs.target nss-lookup.target
    Wants=network-online.target


    [Service]
    Type=forking
    PIDFile=/run/nginx.pid
    # Nginx will fail to start if /run/nginx.pid already exists but has the wrong
    # SELinux context. This might happen when running `nginx -t` from the cmdline.
    # https://bugzilla.redhat.com/show_bug.cgi?id=1268621
    ExecStartPre=/usr/bin/rm -f /run/nginx.pid
    ExecStartPre=/usr/sbin/nginx -t
    ExecStart=/usr/sbin/nginx
    ExecReload=/usr/sbin/nginx -s reload
    KillSignal=SIGQUIT
    TimeoutStopSec=5
    KillMode=process
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target

注册系统服务之后就可以通过系统命令来启动nginx，首先重启系统服务：

    systemctl daemon-reload

然后通过系统服务启动nginx：

    systemctl start nginx

查看是否启动成功：

    systemctl status nginx

出现如下图所示即为启动成功，通过浏览器访问IP查看能否访问，正常。

![](http://pic.xiaodu0.com//assets/uploads/20230926/59378e1920d6155b8d01f48c899e07d0.png)

设置开机自启动：

    systemctl enable nginx.service

# Nginx 基础

## 一、安装nginx

### 1.软件包

Nginx依赖如下：

*   pcre
*   zlib
*   openssl
*   Nginx

> NGINX通过pcre进行正则表达式匹配，所以需要在LInux安装pcre库，使用zlib对文件进行gzip压缩，并且如果需要Nginx支持https就需要openssl

#### 安装pcre

下载软件包：

```Linux
wget http://downloads.sourceforge.net/project/pcre/pcre/8.37/pcre-8.37.tar.gz
```

下载完成之后解压文件 通过：
`tar -zxvf 目标文件名 -C 目标目录`

执行解压命令：
`tar -zxvf 	 -C usr/pcre`

执行`./configure`进行编译

执行`make && make install` 进行安装

#### 安装openssl

下载OpenSSL的地址:
[openssl](http://distfiles.macports.org/openssl/)

1）解压文件， 回到 openssl目录下，

2）./configure 完成后，

3）执行命令： make && make install

#### 安装zlib

通过阿里云镜像站下载：
[zlib rpm包](https://mirrors.aliyun.com/centos/8.5.2111/BaseOS/x86_64/kickstart/Packages/zlib-1.2.11-17.el8.i686.rpm?spm=a2c6h.13651111.0.0.61bd2f70G1qsTE\&file=zlib-1.2.11-17.el8.i686.rpm)

1.  下载zlib

    curl -o zlib.rpm <https://mirrors.aliyun.com/centos/8.5.2111/BaseOS/x86_64/kickstart/Packages/zlib-1.2.11-17.el8.i686.rpm?spm=a2c6h.13651111.0.0.61bd2f70G1qsTE&file=zlib-1.2.11-17.el8.i686.rpm>

2.  安装zlib

    rpm -i zlib.rpm --force --nodeps

因为可能由于缺少依赖导致zlib安装失败 所以使用 `--force --nodeps` 忽略依赖强制安装。

#### 安装nginx

`yum install nginx`

### 2.启动nginx

通过yum安装nginx之后需要找到nginx的安装目录：

`whereis nginx`

结果：

    nginx: /usr/sbin/nginx /usr/lib64/nginx /etc/nginx /usr/share/nginx /usr/share/man/man3/nginx.3pm.gz /usr/share/man/man8/nginx.8.gz

第一个目录是nginx可执行文件的目录。

`cd /usr/sbin`

启动nginx：`nginx`

启动之后查看进程：`ps -ef | grep nginx`

![nginx进程](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694255583-image-1024x115.png)

接下来即可输入IP访问首页（不需指定端口因为默认端口为80）\ <br>

### 3.Nginx的常用命令

**注意：在使用nginx命令之前必须将当前目录切换到nginx可执行目录下。**

1.  查看版本：`nginx -v`

```Linux
[root@ecs-4a4c sbin]# nginx -v
nginx version: nginx/1.20.1
```

1.  关闭nginx `nginx -s stop`
2.  重新加载nginx：`nginx -s reload`
3.  优雅地退出：`nginx -s quit` 退出前完成所有的链接。

***

<br>

### 4.Nginx配置文件

#### (11).查看Nginx配置文件

​	不同方式安装的nginx目录可能都不同，因此需要通过命令来查找nginx文件，这里使用yum方式安装nginx，默认nginx的配置文件nginx.conf是在/etc/nginx/nginx.conf。

​	如果不知道nginx的配置文件 可以通过`nginx -t`命令来检索Nginx配置文件是否正常，同时获得nginx配置文件的位置。

​	![image-20230910004136045](C:\Users\28110\AppData\Roaming\Typora\typora-user-images\image-20230910004136045.png)

#### b.Nginx配置文件的组成

Nginx的配置文件有三个主要部分：

*   全局块
*   events部分
*   http部分

去掉Nginx安装之后的默认注释部分，默认的Nginx配置为：

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
    }

##### 全局块

其中Events上方的内容是全局的核心配置部分，例如上方worker\_processes 表示最大并发处理数，我在阿里云镜像中下载的Nginx默认使用的是auto表示自动决定。

同时还有其他的配置项：

    user nginx
    # 指定运行Nginx的用户，默认为Nginx。
    error_log /var/log/nginx/error.log;
    #错误日志存放路径
    pid /run/nginx.pid;
    # pid 存放路径
    ......

##### events块

events 块涉及的指令**主要影响 Nginx 服务器与用户的网络连接，常用的设置包括是否开启对多 work process 下的网络连接进行序列化，是否 允许同时接收多个网络连接，选取哪种事件驱动模型来处理连接请求，每个 word process 可以同时支持的最大连接数等。**
上述例子就表示每个 work process 支持的最大连接数为 1024.
这部分的配置对 Nginx 的性能影响较大，在实际中应该灵活配置。

##### http块

http块是实现web业务的主要配置文件，其中包括http全局块和server块。

http块包括：http全局块配置的指令包括文件引入、MIME-TYPE 定义、日志自定义、连接超时时间、单链接请求数上限等。

server块：和虚拟主机有密切关系，虚拟主机从用户角度看，和一台独立的硬件主机是完全一样的，该技术的产生是为了 节省互联网服务器硬件成本。

同时在Server块中又可以包含多server全局块和多个location块，location块的主要作用是基于 Nginx 服务器接收到的请求字符串（例如 server\_name/uri-string），对虚拟主机名称 （也可以是IP 别名）之外的字符串（例如 前面的 /uri-string）进行匹配，对特定的请求进行处理。 地址定向、数据缓 存和应答控制等功能，还有许多第三方模块的配置也在这里进行。

##### 总结

Nginx的配置文件结构：

```
Nginx
	└─Ngixn全局块
    ├─Events块
    │  └─...主要的Event配置
    ├─http块
    │  ├─http全局块
    │  └─Server块
    │      ├─location块
    │      └─server全局块
   
```

##### 补充&#x20;

对于开启nginx后无法访问的情况，应当考虑防火墙是否关闭。

关闭防火墙：

```ssh
systemctl stop firewalld.service
```

阻止防火墙开机自启动：

    systemctl disable firewalld.service

放行端口：

    firewall -cmd --zone=public --add-port=80/tcp --permanent

重启防火墙：

    firewall -cmd --reload

### 5. 创建系统服务

默认安装后nginx没有注册到系统服务，也没有添加启动项，这时候重启服务器nginx不能自动启动。

1.  创建系统服务配置文件

    vi /usr/lib/systemd/system/nginx.service

2.写入文件内容

    [Unit]
    Description=The nginx HTTP and reverse proxy server
    After=network-online.target remote-fs.target nss-lookup.target
    Wants=network-online.target


    [Service]
    Type=forking
    PIDFile=/run/nginx.pid
    # Nginx will fail to start if /run/nginx.pid already exists but has the wrong
    # SELinux context. This might happen when running `nginx -t` from the cmdline.
    # https://bugzilla.redhat.com/show_bug.cgi?id=1268621
    ExecStartPre=/usr/bin/rm -f /run/nginx.pid
    ExecStartPre=/usr/sbin/nginx -t
    ExecStart=/usr/sbin/nginx
    ExecReload=/usr/sbin/nginx -s reload
    KillSignal=SIGQUIT
    TimeoutStopSec=5
    KillMode=process
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target

注册系统服务之后就可以通过系统命令来启动nginx，首先重启系统服务：

    systemctl daemon-reload

然后通过系统服务启动nginx：

    systemctl start nginx

查看是否启动成功：

    systemctl status nginx

出现如下图所示即为启动成功，通过浏览器访问IP查看能否访问，正常。

![](http://pic.xiaodu0.com//assets/uploads/20230926/59378e1920d6155b8d01f48c899e07d0.png)

设置开机自启动：

    systemctl enable nginx.service

