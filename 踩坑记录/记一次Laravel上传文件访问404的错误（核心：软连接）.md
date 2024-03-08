# 记一次Laravel项目迁移出现前端上传图片之后访问404的错误



## 问题复述

![小杜的个人图床](http://src.xiaodu0.com/2024/02/01/cbf5845ee386dc1aac9a8762d595ae86.png)

如图所示，前端是一个外汇交易所的实名认证页面，使用Vue-cli进行开发，此时是通过`npm run dev`启动的调试模式，在提交图片上传时，后端返回了正确的结果，但是却无法访问静态文件，报出404错误。



## 解决复述

### 配置检查

后端使用Laravel进行开发，并且综合thinkphp，检查代码：

```php
 public function uploadImage(Request $request)
    {
        if ($vr = $this->verifyField($request->all(),[
            'image' => 'required|image',
        ])) return $vr;

        $disk_type = 'public';

        $disk = \Illuminate\Support\Facades\Storage::disk($disk_type);
        $re = $disk->put('upload',$request->image);
        $data = ['url' => getFullPath($re)  ,'path' => $re];
        return $this->successWithData($data,'上传成功');
    }
```

使用的是Laravel提供的图片上传接口，于是首先检查项目配置：

> config/filesystems.php：

```PHP
'disks' => [

        'local' => [
            'driver' => 'local',
            'root' => public_path('app'),
        ],

        'public' => [
            'driver' => 'local',
            'root' => storage_path('app/public'),
            'url' => env('APP_URL').'/storage',
            'visibility' => 'public',
        ],

        's3' => [
            'driver' => 's3',
            'key' => env('AWS_ACCESS_KEY_ID'),
            'secret' => env('AWS_SECRET_ACCESS_KEY'),
            'region' => env('AWS_DEFAULT_REGION'),
            'bucket' => env('AWS_BUCKET'),
            'url' => env('AWS_URL'),
        ],

        'admin' => [
            'driver' => 'local',
            'root' => storage_path('app/public'),
            'url' => env('APP_URL').'/storage',
            'visibility' => 'public',
        ],

    ],
```

项目配置中的文件系统配置并没有问题。

前端在上传后接收的结果：

```json
{
    "code": 200,
    "message": "\u4e0a\u4f20\u6210\u529f",
    "data": {
        "url": "https:\/\/domain\/storage\/upload\/JoDty77e9UfmT1dZbrUuipPYKcEgG0ewn7ciFQNI.jpg",
        "path": "upload\/JoDty77e9UfmT1dZbrUuipPYKcEgG0ewn7ciFQNI.jpg"
    }
}
```

后端没有抛出错误，并且返回的路径和url也是正确的。



### 文件检查

首先确认文件是否已经上传成功，由于考虑可能是权限的问题，一把梭将整个项目的权限改为777，尝试重新上传仍然失败。

到上传目录检查发现并没有文件（这时候懵逼了），然后想到Laravel通过软链接的方式处理上传文件，找到源文件路径和软链接路径都存在，并且原路径下有对应的图片文件。

![小杜的个人图床](http://src.xiaodu0.com/2024/02/01/b195329ef1329c71addc456716e6741a.png)



### 重启nginx

百度了一下可能是Nginx启动的权限的问题，然后将Nginx关闭：

```bash
nginx -s stop
sudo nginx
```

重启后仍然不能访问。



### LInux软连接

由于服务器是Linux系统的，考虑可能是系统软连接没有建立，导致Larevel也无法正确通过软连接访问文件，尝试重新建立系统软连接：

```
ln -s  /www/wwwroot/site/storage/app/public/upload /www/wwwroot/site/public/upload
```

重新建立软连接之后仍然无法正确访问静态资源，此时已经懵逼了。



### 重新执行Laravel建立软连接的命令

想了一下，突然意识到之前刚开始迁移项目的时候，已经执行了`php artisan storage:link`

但是提示：

```bash
The "public/storage" directory already exists.
```

意识到由于迁移项目的时候在之前的服务器上已经建立了软连接，所以之前第一次建立的时候是失败的，并且这时候没有正确的对应关系。

所以把原来创建的软连接目录删除，重新执行`php artisan storage:link`这时候重新建立了软连接，再次访问URL可以正确访问静态资源，问题解决！



## 总结

在迁移项目的时候，一定要注意在初期的各种配置和迁移步骤都和原先的项目一样，如果有冲突的部分就像现在遇到的这个软连接的问题，或者是其他一些比如临时文件目录等一定要检查好确保没有问题。

