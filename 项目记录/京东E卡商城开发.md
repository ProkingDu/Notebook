
## 物流批量发货


在订单量过多时对订单手动发货是一个大量的工作，因此通过快递公司给的单号Excel数据来进行对本地的订单批量发货。

约定物流发货给出的EXCEL格式应该是：

| 订单ID | 物流公司 | 物流单号          |
| ---- | ---- | ------------- |
| 1    | 中通快递 | 1546515189165 |
| ...  | ...  | ...           |

整个业务是在后台选择客户端EXCEL文件，对EXCEL文件进行解析，生成待更新的订单发货数据，然后批量在数据库中更新。

开发之前考虑过解析EXCEL是通过JS实现还是将EXCEL文件上传到服务器在后端实现，最终选择将EXCEL上传到服务器通过`# PhpSpreadsheet` 将Excel转为Sql语句进行更新。因为通过JS来解析Excel再将数据发送到后端请求更新，容易出现由于数据过大而产生`timeout`的错误导致数据丢失或者不正常的更新操作。

首先在项目中安装`PhpSpreadsheet`扩展：
```php
composer require phpoffice/phpspreadsheet
```

由于我使用的是thinkphp框架，通过composer安装依赖之后会自动在`autoload.php`中引入依赖资源。在需要使用phpoffice的类中：
```php
use PhpOffice\PhpSpreadsheet;
```


创建一个excel文件:：

![小杜的个人图床](http://src.xiaodu0.com/2024/03/09/d75c29287a059962056d37759f2dedca.png)

将Excel文件上传到服务器编写测试代码：
```php
    public function test(){
        // 实例化工厂对象
        $reader = PhpSpreadsheet\IOFactory::createReader('Xlsx');

        // 只读模式
        $reader->setReadDataOnly(TRUE);

        // 载入表格文件
        $file = $reader->load(public_path()."/express.xlsx");
        

        // 获取工作表
        $worksheet = $file->getActiveSheet();
        
        // 获取总列数
        $maxColumn = \PhpOffice\PhpSpreadsheet\Cell\Coordinate::columnIndexFromString($worksheet->getHighestColumn());

        // 获取总行数
        $maxRow = $worksheet->getHighestRow();


        print( "表的总列数：" . $maxColumn."  总行数：".$maxRow);
        // 表的总列数：3 总行数：3
    }
```


由于无法确定导入的EXcel是否包含表头，所以对A1单元格内的数据进行正则匹配，匹配规则是订单号的结构：**D+至少20位数字**

如果检测A1是订单号，则认为此时表格没有表头，数据的遍历从第一行开始，如果A1不是订单号，则认为有表头，数据从第二行开始获取。

```
		 /**
         * 验证订单号
         * @param mixed $value 待验证的数据
         */
        $verifyOrderNo=function($v){
            $match = preg_match("/D\d{20,}/",$v);
            return $match;
        };


        // 检测表头
        if(!$verifyOrderNo($worksheet->getCell([1,1])->getValue())){
            // 第一列是表头
            $start = 2;
        }else{
            $start = 1;
        }
```

通过遍历获取Excel内数据，生成一个二维数据储存订单号对应的物流信息：
```php
// 遍历数据

        $data=[];

        for($i=$start;$i <= $maxRow;$i++){

            $orderNo = $worksheet->getCell([1,$i])->getValue();

            $express = $worksheet->getCell([2,$i])->getValue();

            $expressNo = $worksheet->getCell([3,$i])->getValue();

            $data[$orderNo]=[

                'express'=>$express,

                "expressNo"=>$expressNo

            ];

        }

        return jsonReturn(1,"解析成功",$data);
```

![小杜的个人图床](http://src.xiaodu0.com/2024/03/09/4719bdcb1b3bf3914422f3af89466575.png)

修改Excel内容去除表头测试表头检测是否生效：
![小杜的个人图床](http://src.xiaodu0.com/2024/03/09/5a385318d8cba59b6ee5cda09035150a.png)

![小杜的个人图床](http://src.xiaodu0.com/2024/03/09/e5f69029179d9207ceb031b1983d09d2.png)

由于此前已经有封装好的手动的发货的方法，并且在物流信息表中的外键是订单的索引ID，所以在构建数据的时候还要通过order_no查询订单的ID，在这一步同时判断订单状态和其他的一些必要的条件防止由于Excel中错误的数据产生对订单的错误修改。

在这一步过滤的订单数据应当存储到`failed_list`来记录这些订单未能发货的原因，同时写入日志以便查阅和处理错误。

```php
use app\model\order\Order;

//...
$model = new Order();
        $failed_list=[];
        $successed_lsit =[];
        $data=[];
        for($i=$start;$i <= $maxRow;$i++){
            $orderNo = $worksheet->getCell([1,$i])->getValue();
            $express = $worksheet->getCell([2,$i])->getValue();
            $expressNo = $worksheet->getCell([3,$i])->getValue();

            $order = $model ->where('order_no',$orderNo)->field("id,status,delivery_no,create_time,end_time")->find();
            if($order == NULL){
                $failed_list[]=[
                    'order_no'=>$orderNo,
                    'reason'=>"该订单不存在！",
                    "time"=>date("Y-m-d H:i:s")
                ];
                continue;
            }
            if(!empty($order['status']) && $order['status'] != 3){
                $failed_list[]=[
                    "order_no"=>$orderNo,
                    "reason"=>"该订单的状态非待发货",
                    "time"=>date("Y-m-d H:i:s")
                ];
                continue;
            }
            if((!empty($order['end_time']) && $order['status'] != 10 && $order['end_time'] < date("Y-m-d H:i:s")) || $order['status'] == 11){

                $failed_list[]=[
                    "order_no"=>$orderNo,
                    "reason"=>"此订单已过期！",
                    "time"=>date("Y-m-d H:i:s")
                ];
                continue;
            }
            if($order['status'] == 2){
                $failed_list[]=[
                    "order_no"=>$orderNo,
                    "reason"=>"订单未支付！",
                    "time"=>date("Y-m-d H:i:s")
                ];
                continue;
            }

            $data[$orderNo]=[
                'express'=>$express,
                "expressNo"=>$expressNo
            ];
        }
```

完成判断之后通过已有的发货方法进行发货，在此方法中如果仍然会对参数和订单进行检验，因此应当获取发货方法返回的数据判断是否发货成功和是否写入成功列表。

```php
// 进行发货

            $param = [

                "type"=>1,

                "delivery_name" => $express,

                "delivery_no" => $expressNo,

                "order_id" =>$order['id'],

                "delivery_code"=>""

            ];

  

            $res = $orderService->doExpress($param);

            if($res['code'] == 0){

                $successed_list[]=[

                    'order_no'=>$orderNo,

                    "order_id"=>$order['id'],

                    "express_name"=>$express,

                    "express_no"=>$expressNo

                ];

            }else{

                $failed_list[]=[

                    "order_no"=>$orderNo,

                    "reason"=>$res['msg'],

                    "time"=>date("Y-m-d H:i:s")

                ];

            }
```


在完成整个发货流程之后，统计发货成功的数量和发货失败的数量，返回给前端，并将失败与成功的信息存入.log文件中。

```php
		$logName = date("YmdHis").".log";
        $logPath = public_path()."express_log/".$logName;
        $f=fopen($logPath,"a+");
        fwrite($f,date("Y-m-d H:i:s").":\r\n\r\n");
        fwrite($f,"本次共发货成功：".count($successed_list)."条   发货失败：".count($failed_list)."条\r\n\r\n");
        
        fwrite($f,"发货成功：\r\n");
        foreach($successed_list as $v){
            fwrite($f,"订单号：{$v['order_no']}    订单ID：{$v['order_id']}    物流公司:{$v['express_name']}    物流单号：{$v['express_no']}\r\n");
        }
        
        fwrite($f,"\r\n发货失败：\r\n");
        foreach($failed_list as $v){
            fwrite($f,"订单号：{$v['order_no']}   原因：{$v['reason']}  \r\n");
        }
        fclose($f);
        $count = [
            "successed"=>count($successed_list),
            "failed"=>count($failed_list),
            "log_path"=>"public/express_log/".$logName
        ];

        return jsonReturn(1,"处理成功",$count);
```


到此后端基本上完成，下一步需要做的是在前端开发批量发货上传excel文件，并且接受后端返回的文件。


首先在订单管理中添加批量发货按钮：
```html
<el-button type="primary" @click="multiExpress()" icon="el-icon-connection"

                            size="small">批量发货</el-button>
```

![小杜的个人图床](http://src.xiaodu0.com/2024/03/10/87cf3b44c915abb0b12b6bfb48b4225e.png)

由于需要文件上传，首先创建一个`dialog`弹出窗口：

```html
<el-dialog title="批量发货" :visible.sync="multiExpressVisiable" :close-on-click-modal="false" width="40%">

            <input type="file" ref="excelInput" style="display: none;" @change="getFile()">

            <div class="multi-express-box">

                <div class="img-box" @click="chooseFile()">

                    <img src="/static/admin/default/image/upload.png" alt="" style="height: 100px;width:100px">

                    <p>点击此处选择Excel文件</p>

                </div>

                <div class="result-box" style="display: none;">

  

                </div>

                <el-button type="primary" @click="doMultiExpress" :loading="loading" style="float: right;margin-top:10px">立即提交</el-button>

                <div style="clear: both;"></div>

            </div>

        </el-dialog>
```

CSS:
```css
.img-box{

            display: flex;

            flex-direction: column;

            padding:50px;

            background-color: #d6d6d6ed;

            text-align: center;

            align-items: center;

            border-radius: 20px;

        }
```

js:
```JavaScript
multiExpress() {

                    this.multiExpressVisiable = true

                },

                async doMultiExpress() {

                    let fd = new FormData();

                    fd.append("file", this.excelFile)

                    fetch(this.baseIndex + "/order/multiExpress", {

                        mode: "cors",

                        method: "post",

                        body: fd

                    }).then((e) => {

                        return e.json();

                    }).then((e) => {

                        this.$refs.expressResult.style.display = "block";

                        this.expressResult = `批量发货处理结果： 成功：${e.data.successed}条，失败：${e.data.failed}条。<br>日志地址：<a target="_blank" href="">http://${document.domain}/${e.data.log_path}</a>`;

                    });

  

                },

                chooseFile() {

                    this.$refs.excelInput.click()

                },

                getFile() {

                    this.excelFile = this.$refs.excelInput.files[0];

                },
```


![小杜的个人图床](http://src.xiaodu0.com/2024/03/10/f87d5f8402562968e12f6a05af2920a7.png)

前端的逻辑是将选择的Excel添加到FromData中再通过fetch提交到后端处理，这里上传文件起初是打算通过 `showOpenFilePicker()`来实现，看了下文档目前文件系统的API还是实验性的功能某些浏览器比如火狐不受支持，于是使用传统的表单来选择文件。

后端对应修改：
```php
// 获取表单内容

        $uploadFile = request()->file('file');

  

        $ext = $uploadFile->getOriginalExtension();

        if($ext != "xlsx"){

            return jsonReturn(-1,"仅支持xlsx格式文件！");

        }

  

        $pathName=$uploadFile->move(public_path()."express_excel",time().".xlsx")->getBasename();
```

上传文件测试：
![小杜的个人图床]()![小杜的个人图床](http://src.xiaodu0.com/2024/03/10/f10ea6d2805bde1c8548935a32622359.png)



## Github Hook 多站点自动更新



## Git忽略文件的问题

遇到的情况是：

在我将本地仓库的代码push到github时，由于之前已经提交了代码，某些应该被忽略的文件也被提交上去了，然后我再在 `.gitignore` 中添加忽略的文件名却不起作用。

我尝试删除这个文件再添加到.gitignore中，仍然不起作用。

网上查了一下 是因为.gitignore只有对未被追踪的（**Untrackd**）文件有效，而例如`.env`这个文件之前就已经被追踪了，我再想忽略这个文件就要取消对他的追踪。

其实很简单，只需要执行：
```
git rm -r --cached <filename>
```

实际上如果是单文件可以只使用--cached参数而不必使用-r参数。

`-r` 表示递归地删除文件。

`--cached` 则表示仅在暂存区中移除而不改变工作区的文件，即仅仅从跟踪的清单中删除。

例如：
```
git rm --cached index.html
```

此时index.html会从暂存区中删除，如果不使用`--cached` 参数而是直接执行`git rm`则会在暂存区和工作区中都删除index.html。

在执行上述命令之后，执行`git status index.html`：
![小杜的个人图床](http://src.xiaodu0.com/2024/03/13/174678b9e240334cf7de64775ea78dcb.png)

最新的状态是index.html未被跟踪。

此时查看vscode的版本管理：
![小杜的个人图床](http://src.xiaodu0.com/2024/03/13/16b49fd6f680fa6d5d3867db388ad498.png)

暂存的更改中出现了index.html但是被划线了，说明此时删除index.html的操作还未被提交，这只是index.html的一次改动，他仍然会被追踪。

如果这个时候执行：
```
git reset index.html
```

撤销上次将index.html从暂存区删除的暂存的操作（因为在暂存区删除index.html之后，暂存区实际上还是暂存了删除index.html这个状态。），index.html还是会重新回到暂存区。

但是如果在从暂存区删除index.html之后：
```
git commit -m "untrack index.html"
git status index.html
```

此时index.html已经完全中暂存区和本地仓库中移除了。

这时候在.gitignore中加入`index.html`之后，index.html就完全不会被追踪了。并且整个操作不会对工作区的文件产生影响。

总结一下，如果想要取消追踪已经提交的文件，通过：
```
git rm -r --cached <filename>
git commit -m "untrack file"
git push
```

然后在`.gitignore`中加入此文件即可。

同时补充一下关于文件状态：

1. **Untracked**

未跟踪, 此文件在文件夹中, 但并没有加入到git库, 不参与版本控制. 通过git add 状态变为Staged.

2. **Unmodify**

表示文件已经入库，但是没有进行更改，这种文件可以通过 `git rm`从版本库移除，变为 **Untracked**状态，但是注意直接`git rm`会导致工作区的文件也被删除。

如果此类文件内容被修改，则会变为`Modify`状态

3. **Modify** 

**Modify** 表示文件已经被修改，并且会被git追踪，通过`git add`即可将此类文件加入暂存区。

4. **Staged**

**Staged** 表示文件已经被添加到暂存区，但是没有提交到本地仓库，通过 `git commit` 将Staged类型的文件提交到本地仓库。当文件被提交到本地仓库时，工作区的文件和仓库中的文件版本一致，则此时文件又会变为 **Unmodify** 状态。

通过`git reset HEAD <filename>` 将文件移出暂存区，则文件变为`Modify`已修改状态。