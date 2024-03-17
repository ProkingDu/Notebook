
## Docker的应用场景

### 配置简化

Docker可以大大的简化项目部署和迁移以及配置的过程，通过将应用的所有配置写入 `DockerFile`创建好镜像之后就可以在不同的平台快速部署应用，实现了一次打包，多次部署。

### 代码流水线管理

应用从开发管理到测试环境和生产环境往往需要经过复杂的流程，通过Docker可以实现 **线上线下一致的环境**，从而使开发人员和测试人员只需要关注项目代码即可，使代码的流水线管理非常简单和安全。

### 快速部署

在虚拟机之前，引入新的硬件资源需要很长的时间，而通过Docker将应用封装为镜像之后，只需要启动容器进程而非操作系统即可快速部署应用。这一个过程往往只需要几分钟的时间。

### 应用隔离

资源隔离对于提供共享hosting的公司是一个强需求。如果通过传统的虚拟机方式，虽然隔离的非常彻底，但是部署的密度就降低了，容易增加运维成本。

Docker容器充分的利用了Linux内核提供的namespace资源隔离，结合Cgroups，可以方便的设置每个容器的资源配合，并且针对不同级别的客户提供不同的资源配额。

> Cgroups全程Control Groups，是Linux内核提供的物理资源隔离机制，通过Cgroups可以实现对Linux系统下的进程或者进程资源的限制、隔离和统计功能。
> 参见： https://zhuanlan.zhihu.com/p/81668069?utm_id=0


### 服务器资源整合

正如VM对服务器的资源整合，Docker的应用隔离能力也使得Docker可以对服务器的资源进行整合，并且由于 **Docker没有额外的操作系统占用** ，并且可以 **在不同的实例之间共享没有分配的内容** ，所以Docker可以提供比VM更好的服务器资源整合方案，通过Docker可以有效的提高服务器的资源利用率。

### 多版本混合部署

由于产品的不断更新迭代，在服务器上部署不同的版本的应用或者不同的应用是一个常见的问题，对于这些不同的版本或者不同的应用，在一台服务器上同时部署往往会产生文件路径或者端口冲突的问题。

通过Docker可以很好的解决这个问题，由于Docker的每个容器的文件系统都是相对独立的，所以不必担心路径冲突的问题，而对于端口占用的问题，只需要在容器实例启动的时候选择不同的端口即可。

### 版本升级回滚

对应用程序的升级更新往往不止更新源程序，经常还会对应用的依赖项升级，传统的应用管理方式对版本进行回滚针对依赖的回滚是一个棘手的问题，但是通过Docker即可非常方便的管理。

在对应用升级时，只需要创建一个新的镜像，升级时先停用旧的容器，启动新的容器，如果需要版本回滚，即停用新的容器，切换回旧的容器即可。


### 内部开发环境

在容器技术出现之前，开发人员往往使用一个或者多个虚拟机开进行开发测试，实际上开发测试环境的资源占用非常小，大多数的资源都被虚拟机本身的进程占用了。

Docker没有额外的CPU和资源占用，因此使用Docker相比虚拟机能够更加节省开发测试的资源成本。并且Docker可以很方便的在内部进行共享，因此在提升规范性上也有很大的帮助。


## Docker的简介


### 关于Docker

Docker是一个开源的 **应用容器引擎** ，让开发者可以打包他们的应用以及依赖包到一个可抑制的容器中，然后发布到任何流行的Linux机器上，也可以实现虚拟化。容器完全使用沙盒机制，相互之间 **不会存在任何接口** 。**几乎没有性能开销**，可以很容易的在机器和数据中心运行。最重要的是，他们 **不依赖于任何语言**、**框架或者包装系统**。

Docker是dotCloud公司开源的一个基于LXC的高级容器引擎，源码托管在Github上，基于go语言并且遵从Apache2.0协议开源。

### Docker容器技术与虚拟机的区别


首先是相同点，不管是Docker容器技术还是虚拟机，都是虚拟化技术，

不同点在于，虚拟机技术需要通过Hypervisor来虚拟化硬件资源，并且在不同的虚拟机基于主机操作系统来建立虚拟机操作系统，再在虚拟机系统上运行实例。

而Docker则是直接在主机操作系统上通过Docker引擎即容器引擎来创建不同的容器运行实例，这里容器并不会占用额外的物理资源。

虚拟机结构：
![小杜的个人图床](http://src.xiaodu0.com/2024/03/11/c5b5271defe97edc20733e2237905bc1.png)

Docker的结构：
![小杜的个人图床](http://src.xiaodu0.com/2024/03/11/1f7e2cd9696122aa6b9c5c0935faa02e.png)


**docker相较于VM的优点**：  
1、比VM小、快，Docker容器的尺寸减小相比于整个虚拟机大大简化了分布  
到云和分发时间的开销。Docker启动一个容器实例时间仅仅需要几秒钟。

2、Docker是一个开放的平台，构建、发布和运行分布式应用程序。

3、开发人员不需要关系具体是哪个Linux操作系统

4、Google、微软（azure）、亚马逊、IBM等都支持docker。

5、Docker支持Unix/Linux操作系统，也支持Windows和Mac。

### Docker的局限性

Docker用于应用程序时是最有用的，但并不包含数据。日志、数据库等通常放在Docker容器外。一个容器的镜像通常都很小，不用和存储大量数据，存储可以通过外部挂载等方式使用，比如：NFS、ipsan、MFS等 ，或者docker命令 ，-v映射磁盘分区。
总之，docker只用于计算，存储交给别人。


## Docker的基本概念

Docker最重要的三个概念是：**容器**、**镜像**、**仓库**

### 镜像

我们都知道，操作系统分为 `内核` 和 用户空间。对于 Linux 而言，内核启动后，会挂载 `root` 文件系统为其提供用户空间支持。而 Docker 镜像（Image），就相当于是一个 root 文件系统。比如官方镜像 `ubuntu:18.04` 就包含了完整的一套 Ubuntu 18.04 最小系统的 root 文件系统。

Docker 镜像 是一个特殊的文件系统，除了提供容器运行时所需的程序、库、资源、配置等文件外，还包含了一些为运行时准备的一些配置参数（如匿名卷、环境变量、用户等）。镜像 `不包含` 任何动态数据，其内容在构建之后也不会被改变。



由于镜像是一个包含操作系统的完整文件系统，所以他往往是庞大的，因此在镜像设计时充分采用了 `Union FS` 的技术，将其储存为分层的文件架构。所以严格来说镜像并不是类似ISO那样的打包文件，而是由一组文件系统组成的，或者说是由多组文件系统分层组成的。


镜像构建时，会一层层构建，前一层是后一层的基础。每一层构建完就不会再发生改变，后一层上的任何改变只发生在自己这一层。比如，删除前一层文件的操作，实际不是真的删除前一层的文件，而是仅在当前层标记为该文件已删除。在最终容器运行的时候，虽然不会看到这个文件，但是实际上该文件会一直跟随镜像。因此，在构建镜像的时候，需要额外小心，每一层尽量只包含该层需要添加的东西，任何额外的东西应该在该层构建结束前清理掉。


### 容器

镜像和容器的关系，就像面向对象开发中的类和对象的关系一样，镜像是一个静态的概念，镜像被创建后不再被修改（除非重新创建镜像）。而容器就是镜像的实例，容器是一个动态的运行时的概念。

容器可以被创建、销毁、启动、停止、暂停。

容器的实质是一个进程，但是与直接运行在宿主环境上的进程不同，容器进程运行时有自己独立的 **命名空间** 。因此容器可以有自己的 **`root`文件系统**、**独立的网络配置**、**进程空间**、甚至用户ID空间。

容器内的进程是运行在一个隔离的环境里，使用起来，就好像是在一个独立于宿主的系统下操作一样。这种特性使得容器封装的应用比直接在宿主运行更加安全。也因为这种隔离的特性，很多人初学 Docker 时常常会混淆容器和虚拟机。

容器与镜像一样都是 **分层储存** 的，每一个容器运行时，是以镜像为基础创建一个新的储存层，这个为镜像运行时的读写而做准备的储存层称为 **容器储存层**

需要注意的是：

**容器储存层的生命周期与容器的生命周期一致。** 当容器被创建时，容器储存层也被创建，当容器被销毁时，容器储存层也被销毁，其中的信息也会丢失。

应此 **不应该向容器储存层写入任何数据**，按照Docker最佳实践的要求，容器储存层应当保持 **无状态化**。对于文件的读写应当使用数据卷或者绑定宿主目录，通过数据卷和宿主目录对文件进行读写，在这些位置的读写会 **跳过容器存储层** ，直接对宿主（或网络存储）发生读写，其性能和稳定性更高。

数据卷是 **独立与容器而存在的**。当容器被销毁时，数据卷的信息不会被删除。

### 仓库

当镜像构建完之后，很容易就可以在宿主机上运行。但是如果需要再其他主机运行，就需要一个 **集中储存分发镜像的服务**。

**Docker** **Registry** 就提供了这种服务，在一个Docker Registry中，可以包含多个仓库（Repository），每个仓库有不同的标签（Tag），每个标签对应一个镜像。

通常每个仓库中包含 **镜像的不同版本**，使用标签对他们进行划分各个版本，通过 `<Repository>:<Tag>`的形式访问具体标签对应的镜像，如果不指定Tag，则以 `latest` 为默认值。

以Centos为例，如果需要访问Centos7.9的镜像：
`Centos:7.9`

如果忽略了标签，则是访问Centos最新版本的镜像，等同于：**Centos:latest**

仓库名经常以 *两段式命名* 的形式出现，例如：
```
ProkingDu/Picbed
```

他们是由公开的Docker Registry的用户名和仓库名组成的。

### Docker Registry 公开服务

Docker Registry 公开服务是开放给用户使用、允许用户管理镜像的 Registry 服务。一般这类公开服务允许用户免费上传、下载公开的镜像，并可能提供收费服务供用户管理私有镜像。

最常使用的 Registry 公开服务是官方的 **Docker Hub**，这也是默认的 Registry，并拥有大量的高质量的 官方镜像。除此以外，还有 **Red Hat** 的 *Quay.io*；**Google** 的 *Google Container Registry*，**Kubernetes** 的镜像使用的就是这个服务；代码托管平台 **GitHub** 推出的 *ghcr.io*。


由于某些原因，在国内访问这些服务可能会比较慢。国内的一些云服务商提供了针对 **Docker** **Hub** 的镜像服务（**Registry** **Mirror**），这些镜像服务被称为 **加速器**。常见的有 **阿里云加速器**、**DaoCloud** 加速器 等。使用加速器会直接从国内的地址下载 **Docker** **Hub** 的镜像，比直接从 **Docker** **Hub** 下载速度会提高很多。

国内也有一些云服务商提供类似于 **Docker** **Hub** 的公开服务。比如 **网易云镜像服务**、**DaoCloud** **镜像市场**、**阿里云镜像库** 等。




### 私有Docker Registory

除了使用公开服务外，用户还可以在本地搭建私有 Docker Registry。Docker 官方提供了 Docker Registry 镜像，可以直接使用做为私有 Registry 服务。

开源的 **Docker** **Registry** 镜像只提供了 **Docker** **Registry** **API** 的服务端实现，足以支持 docker 命令，不影响使用。但不包含图形界面，以及镜像维护、用户管理、访问控制等高级功能。

除了官方的 Docker Registry 外，还有第三方软件实现了 Docker Registry API，甚至提供了用户界面以及一些高级功能。比如，**Harbor** 和 **Sonatype** **Nexus**。


## 安装Docker

测试环境为Vmware Workstation 下的ubuntu 虚拟机。


### 卸载旧版本

在安装最新版本的Docker之前，首先卸载旧的Docker版本（确保没有重要的数据）。

```bash
sudo apt-get remove docker \ docker.io \ docker-engine
```


### 安装依赖及软件包


由于apt源使用https进行传输，因此在新机器上安装Docker之前要先升级apt并且安装用于https传输的软甲包和证书。

```bash
sudo apt-get update

sudo apt-get install apt-transport-https \ ca-certificates \ curl \ gnupg \ lsb-release
```

上述安装的软件包分别是：

1. apt-transport-https   用于安装ubuntu对https的支持
2.  ca-certificates 用于验证SSL/TLS 证书的根证书的集合
3.  curl 最常用的网络请求工具
4. gnupg  **GNU Privacy Guard** Linux平台流行的加密工具
5. lsb-release  Linux版本信息工具

执行更新和安装指令发现非常慢，更换apt软件源：

```bash
cp /etc/apt/sources.list /etc/apt/sources.list.bak #备份源
sudo vi /etc/apt/sources.list
i
"deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe 
"
:wq

sudo apt-get update # 更新源

sudo apt-get install apt-transport-https \ ca-certificates \ curl \ gnupg \ lsb-release
# 安装软件包
```

这里总是出现各种各样的问题，比如下载速度过慢（已经尝试更换镜像源）和无法定位到软件包，后面换一台云服务器操作。

这里我使用的是安装了CentOs操作系统的云服务器所以对以上的apt-get操作全部换成yum。

首先卸载旧版本：
``` bash
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```

Bash:
```bash
No Match for argument: docker
No Match for argument: docker-client
No Match for argument: docker-client-latest
No Match for argument: docker-common
No Match for argument: docker-latest
No Match for argument: docker-latest-logrotate
No Match for argument: docker-logrotate
No Match for argument: docker-selinux
No Match for argument: docker-engine-selinux
No Match for argument: docker-engine
No Packages marked for removal
```

此系统未安装过任何旧版的Docker.

安装依赖包：
```bash
sudo yum install -y yum-utils
```

![小杜的个人图床](http://src.xiaodu0.com/2024/03/17/04b7c68effb7d6f8b725c546eb3b5de4.png)



更换软件镜像源：

```bash
sudo yum-config-manager \
    --add-repo \
    https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

sudo sed -i 's/download.docker.com/mirrors.aliyun.com\/docker-ce/g' /etc/yum.repos.d/docker-ce.repo
```



安装Docker-ce:

```bash
sudo yum install docker-ce docker-ce-cli containerd.io
```

![小杜的个人图床](http://src.xiaodu0.com/2024/03/17/4ce28722a25cefb8042b794b908e3aed.png)


软件包解释：
1.  docker-ce Docker的社区版软件
2.  docker-ce-cli  它提供了与Docker守护进程进行交互的命令行接口，可以用于管理和操作Docker容器、镜像、网络等。
3. containerd.io    从docker中分离出的底层的工业级的容器运行时。
### 关于Docker与docker和Docker的各种版本

在上方安装的过程中都要首先卸载docker再安装Docker，实际上这两个`docker`不是一个东西。

在容器化技术出现之前，Linux已经存在一个名为docker的窗口停靠栏程序，类似macos的底部停靠栏。

我们暂时以不同的首字母大小写区分，docker代表较早的GUI程序，Docker代表容器化技术。

由于Docker发布时的官网是docker.io，所以在ubuntu上Docker的软件名是docker.io，而在Centos上则是docker.io。

虽然软件名更改了，但是操作的指令都是docker，因此在安装Docker之前，要确保没有安装docker,如果有的话就要先卸载。

这时候的安装命令：
```
# ubnutu
apt-get install docker.io

# centos
yum install docker-io
```


后来随着Dcokre的发展，docker-io又被改名为 `docker-engine`，且在ubuntu的centos平台上的名称都一致。

```
apt-get install docker-engine

yum install docker-engine
```

随着Docker技术越来越流行，在征得原作者同意以后，docker被改名为`wm-docker`，此后Docker正式的使用`docker`命令。因此在新版的Linux系列操作系统重，如果你安装了wmdocker也不必卸载他， 但是为了保证不出错误，我们习惯上还是会在安装Docekr之前检测是否安装了旧版的docker。


目前与我们最相关的就是docker-ce和docker-ee

这两者最大的区别就是docker-ce是个人使用和学习的版本，docker-ee是商业版本。

在安装Docker的时候，就不必再考虑docker-io、docker-engine、docker这些旧版本了，只需要根据用途选择docker-ee和docker-ce即可。

在Ubuntu平台比较特殊，docker.io版本仍然在一直更新维护。


### centos8额外设置

由于 CentOS8 防火墙使用了 `nftables`，但 Docker 尚未支持 `nftables`， 我们可以使用如下设置使用 `iptables`：

更改 `/etc/firewalld/firewalld.conf`

复制

```bash 
# FirewallBackend=nftables
FirewallBackend=iptables
```

或者执行如下命令：

```bash 
$ firewall-cmd --permanent --zone=trusted --add-interface=docker0

$ firewall-cmd --reload

```



### 使用安装脚本

docker提供了简化的安装脚本以便快速安装部署Docker：
```bash 
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh --mirror Aliyun
```

执行这个命令后，脚本就会自动的将一切准备工作做好，并且把 Docker 的稳定(stable)版本安装在系统中


### 设置用户组

默认情况下，`docker` 命令会使用 [Unix socket](https://en.wikipedia.org/wiki/Unix_domain_socket) 与 Docker 引擎通讯。而只有 `root` 用户和 `docker` 组的用户才可以访问 Docker 引擎的 Unix socket。出于安全考虑，一般 Linux 系统上不会直接使用 `root` 用户。因此，更好地做法是将需要使用 `docker` 的用户加入 `docker` 用户组。

建立 `docker` 组：

复制

```
$ sudo groupadd docker
```

将当前用户加入 `docker` 组：

复制

```
$ sudo usermod -aG docker $USER
```


### 启动与测试

我在尝试启动Docker的时候报出了一堆错误，首先尝试关闭防火墙：
```bash
systemctl disable firewalld.service
```

接着重新启动Docker：
```bash
systemctl restart docker
```

仍然没有作用。

检查SELinx:
```bash
/usr/sbin/sestatus -v
```

已经关闭了selinux。

检查用户组;

```bash
cat /etc/group
```

用户组没问题。

无果，重启大法：

```
init 6
...

systemctl restart docker
docker run --rm hello-world
```

成功！！！！

在安装完Docker之后首先启动Docker之后运行`hello-world`容器测试：

```
systemctl start docker

docker run --rm hello-word
```

docker是操作Docker的命令，run表示运行容器，`--rm`指在关闭容器之后就销毁。

### 设置加速器

由于默认的Docker使用官方镜像可能存在下载缓慢的问题（如果是国外的服务器则不考虑这个问题），因此需要设置国内镜像的加速器。

这里使用网易云镜像：`https://hub-mirror.c.163.com`


目前主流 Linux 发行版均已使用 [systemd](https://systemd.io/) 进行服务管理，配合systemd可以很方便的进行docker镜像源的配置。

首先执行：
```bash
systemctl cat docker | grep '\-\-registry\-mirror'
```

如果该命令有输出，执行 `$ systemctl cat docker` 查看 `ExecStart=` 出现的位置，修改对应的文件内容去掉 `--registry-mirror` 参数及其值，并按接下来的步骤进行配置。

这里我测试没有任何输出，默认安装的Docker没有配置其他镜像源。

修改`/etc/docker/daemon.json`写入：
```json
{
  "registry-mirrors": [
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
```

查看一下，测试的服务器中没有此文件，则进行创建并写入上述内容：

```bash
[root@iZj6c7vv738lrw2660ktq6Z 818s.s12k.cc]# cat /etc/docker/daemon.js
cat: /etc/docker/daemon.js: No such file or directory

vim /etc/docker/daemon.json
```
之后重新启动服务。


```
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```


检测加速器是否生效：

```
docker info
```

执行docker info查看docker的基本信息，如果存在以下内容则说明加速器配置成功。

![小杜的个人图床](http://src.xiaodu0.com/2024/03/17/05db65fb9c2fdf7c92a583fb70243dd0.png)


可用docker镜像以及日常的测试：
[Test Registry · docker-practice/docker-registry-cn-mirror-test@83a4dd4 (github.com)](https://github.com/docker-practice/docker-registry-cn-mirror-test/actions/runs/8311801802)



## 使用镜像

### 获取镜像


在使用镜像之前要从Dockerhub中拉取镜像，类似于Git的操作，拉取镜像的命令是：
```
docekr pull [Docker Registry:端口/]仓库名[:标签]
```

其中中括号的部分是可选的，如果不指定Docker Registry的地址，则使用官方的Dockerhub作为镜像源，如果配置了加速器，则优先使用加速器作为源。

之前配置的网易云和百度源尝试pull失败，使用阿里云源;
[容器镜像服务 (aliyun.com)](https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors)

登录之后即可查看镜像源地址。

尝试拉取ubuntu18.04镜像：
```
docker pull ubuntu:18.04
```

**如果不指定标签直接pull则获取最新的latest版本。**

![小杜的个人图床](http://src.xiaodu0.com/2024/03/17/bb3e1e6078009f9e17a1e8089b7f4616.png)


> 具体的选项可以通过 `docker pull --help` 命令看到，这里我们说一下镜像名称的格式。

- Docker 镜像仓库地址：地址的格式一般是 `<域名/IP>[:端口号]`。默认地址是 Docker Hub(`docker.io`)。
    
- 仓库名：如之前所说，这里的仓库名是两段式名称，即 `<用户名>/<软件名>`。对于 Docker Hub，如果不给出用户名，则默认为 `library`，也就是官方镜像。

在获取镜像之后就可以通过镜像创建一个容器来运行：

```
docker run -it --rm centos bash
```

这里的命令是运行容器的命令，其中的
`-it` 是`-i`和`-t`结合的参数，表示应当启动一个交互式（i）终端（t）,并且通过`--rm`表示销毁容器之后删除相关文件。 `bash`表示放在镜像名后的是 **命令**，这里我们希望有个交互式 Shell，因此用的是 `bash`。`centos`通过centos镜像运行容器。

在启动之后终端会进入容器的终端，通过：
```bash
cat /etc/issue
```

查看发行版信息。


由于我使用的是centos系统作为宿主机，因此使用Ubuntu:18.04来体现差异：
```
docker run -it --rm ubuntu:18.04 bash
```

然后执行
```
cat /etc/issue # 查看容器发行版本信息
exit # 退出容器终端
cat /etc/issue # 查看宿主机发型版本信息
```

![小杜的个人图床](http://src.xiaodu0.com/2024/03/17/30eb93e293642aa47c1bbbef28ef438b.png)

由此可以体验容器具有独立的文件系统。


这里有一个疑惑：
![小杜的个人图床](http://src.xiaodu0.com/2024/03/17/68d99f03b97f5e9072bb422d2f97738f.png)

宿主机的一些关于硬件配置的文件和信息会被容器继承，不清楚这个原理是什么，等完成了解Docker以后再深入研究。


### 列出镜像

#### 命令

通过
```
docker image ls
```

列出本地已经下载的镜像。

![小杜的个人图床](http://src.xiaodu0.com/2024/03/17/9c5959731f3f95629cc62a6f597a2a31.png)

列表包含了 `仓库名`、`标签`、`镜像 ID`、`创建时间` 以及 `所占用的空间`。

其中仓库名、标签在之前的基础概念章节已经介绍过了。**镜像 ID** 则是镜像的唯一标识，一个镜像可以对应多个 **标签**。

#### 镜像体积

如果仔细观察，会注意到，这里标识的所占用空间和在 Docker Hub 上看到的镜像大小不同。比如，`ubuntu:18.04` 镜像大小，在这里是 `63.3MB`，但是在 [Docker Hub](https://hub.docker.com/layers/ubuntu/library/ubuntu/bionic/images/sha256-32776cc92b5810ce72e77aca1d949de1f348e1d281d3f00ebcc22a3adcdc9f42?context=explore) 显示的却是 `25.47 MB`。这是因为 Docker Hub 中显示的体积是压缩后的体积。在镜像下载和上传过程中镜像是保持着压缩状态的，因此 Docker Hub 所显示的大小是网络传输中更关心的流量大小。而 `docker image ls` 显示的是镜像下载到本地后，展开的大小，准确说，是展开后的各层所占空间的总和，因为镜像到本地后，查看空间的时候，更关心的是本地磁盘空间占用的大小。

另外一个需要注意的问题是，`docker image ls` 列表中的镜像体积总和并非是所有镜像实际硬盘消耗。由于 Docker 镜像是多层存储结构，并且可以继承、复用，因此不同镜像可能会因为使用相同的基础镜像，从而拥有共同的层。由于 Docker 使用 Union FS，相同的层只需要保存一份即可，因此实际镜像硬盘占用空间很可能要比这个列表镜像大小的总和要小的多。



可以通过：
```
docker system df
```

查看Docker的镜像、容器和数据卷所占用的空间。

![小杜的个人图床](http://src.xiaodu0.com/2024/03/17/968566f4bab8863978bd7b930b6384b3.png)

即使我已经创建了几个容器进行测试，这里的Containers却仍然是0，这就是`--rm`参数的妙用，通过`--rm`运行容器可在容器结束时就释放容器和相关的内存占用。



#### 虚悬镜像


上面的镜像列表中，还可以看到一个特殊的镜像，这个镜像既没有仓库名，也没有标签，均为 `<none>`。

```
<none>               <none>              00285df0df87        5 days ago          342 MB
```

这个镜像原本是有镜像名和标签的，原来为 `mongo:3.2`，随着官方镜像维护，发布了新版本后，重新 `docker pull mongo:3.2` 时，`mongo:3.2` 这个镜像名被转移到了新下载的镜像身上，而旧的镜像上的这个名称则被取消，从而成为了 `<none>`。除了 `docker pull` 可能导致这种情况，`docker build` 也同样可以导致这种现象。由于新旧镜像同名，旧镜像名称被取消，从而出现仓库名、标签均为 `<none>` 的镜像。这类无标签镜像也被称为 **虚悬镜像(dangling image)** ，可以用下面的命令专门显示这类镜像：
```
docker image ls -f dangling=true
```


![小杜的个人图床](http://src.xiaodu0.com/2024/03/17/0fb14b3e1e5982177ae0dd12a2dfd687.png)

一般来说，虚悬镜像已经失去了存在的价值，是可以随意删除的，可以用下面的命令删除。

```bash 
docker image prune
```


![小杜的个人图床](http://src.xiaodu0.com/2024/03/17/46b0ef62ed17aa320e9bb5f655288899.png)

