## 验证器设计

由于thinkphp自带了验证器规则，使用Validate验证器基类进行字段验证，同时在config\\api.php中定义错误码1000为验证器通用错误码（请求字段验证不通过时均返回此错误）。

例如：
```json
{"code":1000,"msg":"域名（Domain）不能为空"}
```

### Token验证器

Token验证器即在请求获取Token的时候验证必要字段，由于程序的授权应当绑定IP和域名，因此要验证请求的IP和Token是否合法：
```php
/**

 * Token验证类

 */

namespace app\api\validate;

use think\Validate;

class Token extends Validate{

    protected $rule=[

        "domain|域名（Domain）" => "require|activeUrl",

        "ip|服务器IP地址"=>"require|ip"

    ];

}
```


在请求获取Token的时候，进行验证：
```php
// 验证参数

        try{

            validate(Token::class)->check($param);

        }catch(ValidateException $e){

            return jsonReturn(1000,$e->getMessage());

        }
```


验证Token和获取Token内容的操作应当只在API基类和其子类中被调用，因此将其写为受保护的方法，并且返回值统一为数组：
```php
/**
     * 验证token
     */
    public function verifyToken()
    {
        try {
            // 获取请求头
            $headers = request()->header();
            // 验证签名
            $token = $headers['authorization'];

            $res = JwtTools::verifyToken($token);
            // 字段验证
            try {
                validate(Token::class)->check($res);
            } catch (ValidateException $e) {
                return dataReturn(1000, $e->getMessage());
            }

            // 其他的验证
            if ($res === false || $res['iss'] !== config("api.jwt.issue")) {
                return dataReturn(1001, config("api.errCode.1001"));
            } else if ($res['exp'] < date("Y-m-d H:i:s")) {
                return dataReturn(1002, config("api.errCode.1002"));
            } else {
                return dataReturn(200, config("api.errCode.200"), $res);
            }
        } catch (Exception $e) {
            return dataReturn(1000, $e->getMessage());
        }

    }
```

由于在验证Token之后可能需要用到生成Token的参数，所以在验证成功之后返回有效负载。


## 中间件设计

由于API模块需要在业务之前对Token进行验证和鉴权，所以在实际执行控制器的业务逻辑之前首先通过中间件对请求参数进行过滤。

### Token验证中间件

例如

## 接口开发

### 授权验证

