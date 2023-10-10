# 2023-10-09 碎片化知识手记

## Linux 自定义命令

### 1. 通过alias别名

通过alisa别名可以对命令进行简化，如果已经编写好了批处理文件，通过就可以通过alias来定义简短的命令执行批处理。
例如：

```shell
alias sync="sh submit"
```
alias的语法格式：

```shell
alias command=value
```
**参数：**
1. command 自定义命令名称
2. value 自定义命令的内容
   

**其中value需要是一个字符串。**
批处理(submit)：
```shell
host=`hostname`
git add .
git commit -m "自动提交，来自："$host
git push --force
echo "提交完成"
```
<br>

* **通过分号分隔多条语句，可以使alias执行多条命令。**

   别名：
   ```
   alias sync="sh submit"
   ```
    等同于:
    ```shell
    alias sync="host=`hostname`;git add .;git commit -m "自动提交，来自："$host;git push --force;echo '提交完成'"
    ```
<br>

* **alias可以携带自定义参数：**
    例如定义`test="echo"`执行`test Hello`会输出Hello相当于执行了echo Hello。  
    <br>

* **alias可以不带任何参数 这时候alias会列出所有已经定义的别名**
  <br>

    ![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231009/0a58d1e1936ede4e43a073db399738e0.png)

<br>

* **取消别名：**
    ```shell
    unalias name
    ```
    <br>

***Note:别名默认临时生效，在重启linux后会消失，如果需要固定使用别名，需要将其写入配置文件***

<br>

配置文件位于：

`~/.bashrc`

在`~/.bashrc`中定义别名即可在全局永久生效。

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231011/2ccdb4c141ca785208da230d7fa943b1.png)

### 2.通过环境变量

环境变量存在`/bin`目录下，这里的所有指令都可以在全局执行。

例如编译安装的nginx就需要设置环境变量来是nginx命令在全局执行，通过：

```shell
cd /bin
echo "/usr/local/nginx/sbin/nginx" > nginx
```

在bin目录下新建一个nginx环境变量，之后：

**踩坑：一定要给与访问权限！！！！！！！！！！！！！**

![小杜的个人图床](http://pic.xiaodu0.com//assets/uploads/20231011/ec1fc862f736bb3e7856a6cc81470e4b.png)

如上图所示，我在添加nginx变量之后，一直无法执行。提示permission denied。

尝试修改nginx配置文件下的user nobody为user root

无法解决。

百度搜一圈发现关于nginx权限不足的方法都尝试了，仍然得不到解决。

最后想到可能是环境变量的问题。

给与权限：
```shell
chmod 777 /bin/nginx
```

成功执行。



