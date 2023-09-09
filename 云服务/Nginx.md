# Nginx 反向代理与负载均衡
## 一、安装nginx
### 1.软件包
Nginx依赖如下：
* pcre
* zlib
* openssl
* Nginx

> NGINX通过pcre进行正则表达式匹配，所以需要在LInux安装pcre库，使用zlib对文件进行gzip压缩，并且如果需要Nginx支持https就需要openssl

#### 安装pcre
下载软件包：

```Linux
wget http://downloads.sourceforge.net/project/pcre/pcre/8.37/pcre-8.37.tar.gz
```
下载完成之后解压文件 通过：
``
tar -zxvf 目标文件名 -C 目标目录
``

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
[zlib rpm包](https://mirrors.aliyun.com/centos/8.5.2111/BaseOS/x86_64/kickstart/Packages/zlib-1.2.11-17.el8.i686.rpm?spm=a2c6h.13651111.0.0.61bd2f70G1qsTE&file=zlib-1.2.11-17.el8.i686.rpm)

1) 下载zlib
```
curl -o zlib.rpm https://mirrors.aliyun.com/centos/8.5.2111/BaseOS/x86_64/kickstart/Packages/zlib-1.2.11-17.el8.i686.rpm?spm=a2c6h.13651111.0.0.61bd2f70G1qsTE&file=zlib-1.2.11-17.el8.i686.rpm
```

2) 安装zlib
```
rpm -i zlib.rpm --force --nodeps
```
因为可能由于缺少依赖导致zlib安装失败 所以使用 `--force --nodeps` 忽略依赖强制安装。

#### 安装nginx
`yum install nginx`

***

### 2.启动nginx
通过yum安装nginx之后需要找到nginx的安装目录：

``whereis nginx``

结果：
```
nginx: /usr/sbin/nginx /usr/lib64/nginx /etc/nginx /usr/share/nginx /usr/share/man/man3/nginx.3pm.gz /usr/share/man/man8/nginx.8.gz
```

第一个目录是nginx可执行文件的目录。

```cd /usr/sbin```

启动nginx：`nginx`

启动之后查看进程：`ps -ef | grep nginx`

![nginx进程](http://www.xiaodu0.com/wp-content/uploads/2023/09/1694255583-image-1024x115.png)


接下来即可输入IP访问首页（不需指定端口因为默认端口为80）  
<br>

### 3.Nginx的常用命令

**注意：在使用nginx命令之前必须将当前目录切换到nginx可执行目录下。**

1)  查看版本：`nginx -v`
```
[root@ecs-4a4c sbin]# nginx -v
nginx version: nginx/1.20.1
```
2) 关闭nginx `nginx -s stop`
3) 重新加载nginx：`nginx -s reload`
***
<br>

### 4.Nginx配置文件

   Nginx的配置文件主
