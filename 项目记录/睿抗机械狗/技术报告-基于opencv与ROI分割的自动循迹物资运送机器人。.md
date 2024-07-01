
# 作品概述

我们的作品实现的核心技术是opencv，基于对图像分割感兴趣的区域（ROI）实现机器人根据路线自动循迹。由于机器人内部使用多个独立的板卡，在实现作品之前我们首先解决了板卡间通信的问题，包括：运控板卡的联网、通过websocket搭建运控服务端、通过http协议传输视频流等准备工作。随后，在机器人内部安装必要环境和软件包，同时由于存在nano板卡无法联网的问题，我们通过基于内网的scp工具来在板卡间传输文件。

在一切准备工作完成之后，开始编写运动相关的程序。我们参考宇树科技提供的开发资料库，主要采用C++与Python进行开发，其中遇到一些困难，最终都已经得到解决，在系统设计上，我们着重考虑算法的稳定性和可用性，旨在通过尽可能少的训练调试适应不同的地图情况。

在物资运送的实现中，我们主要考虑物资识别、物资抓取与物资卸载三大部分。首先是基于Arduino AVR单片机设计的通过串口信号控制的总线结构机械臂，在机械臂组成上，采用六个总线舵机，并通过支持pwm信号的杜邦线串联，同时对舵机的核心程序进行封装，以PWM信号的方式控制舵机转动实现机械臂整体的灵活运动。
# 模块设计

在软件系统设计中，我们考虑到机器人所需要实现的核心功能，其中包括：
1. 通过SDK对机器人控制
2. 通过CameraSDK获取双目鱼眼相机的视频帧
3. 在板卡间传输视频流
4. 对视频流进行处理，分割出图像
5. 对图像进行处理，得出赛道部分并决定移动方式
6. 识别标记点卸载物资
7. 机械臂的运动控制程序设计
8. 机械臂与机器人的串口通信


# Part I 机械臂设计

## 1. 整体设计

我们的机械臂结构图如下所示：
![小杜的个人图床](http://src.xiaodu0.com/2024/05/17/3e776fa8ef75469cb8e070006663739b.png)
其中标记的S0、S1、S2、S3、S4、S5的节点即为总线舵机，通过这六个舵机的转向来实现机械臂整体的运动。

其中舵机000为底部云台舵机，控制机械臂整体旋转，001为云台上方摆动舵机，控制机械臂整体在水平方向的前后移动。编号002为小臂控制舵机，用于控制小臂前后摆动，编号003为爪子摆动舵机，用于控制爪子在水平方向的前后摆动，004为爪子转向舵机，用于控制爪子在水平方向的左右旋转，005为爪子开合舵机，控制爪子开合。

实物图如下所示：
![小杜的个人图床](http://src.xiaodu0.com/2024/05/17/8dc0cc49d543c5e06fe5f6e27736779e.png)

由于我们物料体积的问题，在机械臂组装之后，我们更换了新的爪子来适配物料的抓取。

我们的机械臂是购买了一套组装的套件，自行手动安装完成的，在程序设计上，一部分参考商家提供的出厂示例程序，另一部分根据作品需求进行二次开发。

## 2. 结构组成

这一部分介绍我们设计的机械臂所使用的零件以及其在整体中的功能。

1. 云台与云台舵机和组装螺丝，用于控制机械臂底部旋转与提供支撑
![小杜的个人图床](http://src.xiaodu0.com/2024/06/29/abce0d02c2b347ea908b3593d4864067.png)

![小杜的个人图床](http://src.xiaodu0.com/2024/06/29/bfbf21b6b4740d11f7683abafc270553.png)

2. 云台支撑结构，用于支持云台，提供稳定作用

![小杜的个人图床](http://src.xiaodu0.com/2024/06/29/320303f23c1cb037a5c0e7925f236356.png)

3. U型舵机支架 用于固定伸展舵机，防止过重导致的损坏
![小杜的个人图床](http://src.xiaodu0.com/2024/06/29/ffde83da34c90c81c1bdae110e297000.png)

4. 舵机与牵动盘口 为伸展舵机提供牵动与稳定功能。
![小杜的个人图床](http://src.xiaodu0.com/2024/06/29/7b29cb57750f61143f1026899fd85124.png)

5. 短C型舵机支架 用于连接两个伸展舵机，提高承重。
![小杜的个人图床](http://src.xiaodu0.com/2024/06/29/ad7d3b7acba1c3f6b95d5594ed9d9f57.png)

6. 凹凸直立舵机支架，用于连接爪子舵机与爪子旋转舵机
![小杜的个人图床](http://src.xiaodu0.com/2024/06/29/1e46b69431b9609ef7974623893144c9.png)

7. 金属舵盘，用于为爪子旋转提供牵引和保持稳定。
![小杜的个人图床](http://src.xiaodu0.com/2024/06/29/fbb6b434492f45da6f6eef9e70fee31c.png)
8. 组合后示意图：
![小杜的个人图床](http://src.xiaodu0.com/2024/06/29/a530ca5cebb4993efdb80c6e504f97cb.png)

## 3. 程序开发与烧录

### (1).出厂程序烧录

商家提供了控制板与开发板的基础示例程序用于集成开发，我们通过将示例程序烧录到开发板中作为接口使用来二次开发实现目的的业务控制。
出厂程序使用C语言编写，商家提供了mixly程序进行代码编写，由于其示例程序过于复杂，涉及到蓝牙、wifi模块以及无线控制和遥控机控制这些额外的事件循环和监听，为了优化程序结构，加快执行速度，我们只保留了用于串口指令交互的部分相关的代码。

源代码与说明：
```C++
void parse_action(u8 *uart_receive_buf) {
    static unsigned int index, time1, pwm1, pwm2, i, len;//声明三个变量分别用来存储解析后的舵机序号，舵机执行时间，舵机PWM
    if((uart_receive_buf[0] == '#') && (uart_receive_buf[4] == 'P') && (uart_receive_buf[5] == '!')) {
        delay(500);
    }
    Serial.println((char *)uart_receive_buf);
    if(zx_read_flag) {
  	  //#001P1500! 回读处理
  	  if((uart_receive_buf[0] == '#') && (uart_receive_buf[4] == 'P') && (uart_receive_buf[9] == '!')) {
    	    index = (uart_receive_buf[1]-'0')*100 +  (uart_receive_buf[2]-'0')*10 +  (uart_receive_buf[3]-'0');
			  if(index == zx_read_id) {
 				  zx_read_flag = 0;
      		  zx_read_value = (uart_receive_buf[5]-'0')*1000 + (uart_receive_buf[6]-'0')*100 +  (uart_receive_buf[7]-'0')*10 +  (uart_receive_buf[8]-'0');
			  }
		}
    //#001PSCK+100! 偏差处理
    } else if((uart_receive_buf[0] == '#') && (uart_receive_buf[4] == 'P') && (uart_receive_buf[5] == 'S') && (uart_receive_buf[6] == 'C') && (uart_receive_buf[7] == 'K')) {
        index = (uart_receive_buf[1]-'0')*100 +  (uart_receive_buf[2]-'0')*10 +  (uart_receive_buf[3]-'0');
        if(index < SERVO_NUM) {
            int bias_tmp = (uart_receive_buf[9]-'0')*100 +  (uart_receive_buf[10]-'0')*10 +  (uart_receive_buf[11]-'0');
            if(bias_tmp < 127) {
            myservo[index].attach(servo_pin[index]);
              if(uart_receive_buf[8] == '+') {
                  servo_do[index].cur = servo_do[index].cur-eeprom_info.dj_bias_pwm[index]+bias_tmp;
                  eeprom_info.dj_bias_pwm[index] = bias_tmp;
              } else if(uart_receive_buf[8] == '-') {
                  servo_do[index].cur = servo_do[index].cur-eeprom_info.dj_bias_pwm[index]-bias_tmp;
                  eeprom_info.dj_bias_pwm[index] = -bias_tmp;
              }
              rewrite_eeprom();
				servo_do[index].cur = 1500;
				servo_do[index].aim = 1500+eeprom_info.dj_bias_pwm[index]; //舵机PWM赋值,加上偏差的值
				servo_do[index].time1 = 100;      //舵机执行时间赋值
				servo_do[index].inc = eeprom_info.dj_bias_pwm[index]/5.000; //根据时间计算舵机PWM增量
              //Serial.print("input bias:");
              //Serial.println(eeprom_info.dj_bias_pwm[index]);
           }
        }
    //停止处理
    } else if((uart_receive_buf[0] == '#') && (uart_receive_buf[4] == 'P') && (uart_receive_buf[5] == 'D') && (uart_receive_buf[6] == 'S') && (uart_receive_buf[7] == 'T')) {
        index = (uart_receive_buf[1]-'0')*100 +  (uart_receive_buf[2]-'0')*10 +  (uart_receive_buf[3]-'0');
        if(index < SERVO_NUM) {
              servo_do[index].inc =  0.001;
              servo_do[index].aim = servo_do[index].cur;
        }
    } else if((uart_receive_buf[0] == '#') || (uart_receive_buf[0] == '{')) {   //解析以“#”或者以“{”开头的指令
        len = strlen(uart_receive_buf);     //获取串口接收数据的长度
        index=0; pwm1=0; time1=0;           //3个参数初始化
        for(i = 0; i < len; i++) {          //
            if(uart_receive_buf[i] == '#') {        //判断是否为起始符“#”
                i++;                        //下一个字符
                while((uart_receive_buf[i] != 'P') && (i<len)) {     //判断是否为#之后P之前的数字字符
                    index = index*10 + (uart_receive_buf[i] - '0');  //记录P之前的数字
                    i++;
                }
                i--;                          //因为上面i多自增一次，所以要减去1个
            } else if(uart_receive_buf[i] == 'P') {   //检测是否为“P”
                i++;
                while((uart_receive_buf[i] != 'T') && (i<len)) {  //检测P之后T之前的数字字符并保存
                    pwm1 = pwm1*10 + (uart_receive_buf[i] - '0');
                    i++;
                }
                i--;
            } else if(uart_receive_buf[i] == 'T') {  //判断是否为“T”
                i++;
                while((uart_receive_buf[i] != '!') && (i<len)) {//检测T之后!之前的数字字符并保存
                    time1 = time1*10 + (uart_receive_buf[i] - '0'); //将T后面的数字保存
                    i++;
                }
                if(time1<SERVO_TIME_PERIOD)time1=SERVO_TIME_PERIOD;//很重要，防止被除数为0
                if((index == 255) && (pwm1 >= 500) && (pwm1 <= 2500) && (time1<10000)) {  //如果舵机号和PWM数值超出约定值则跳出不处理
						for(int i=0;i<SERVO_NUM;i++) {
                    		pwm2 = pwm1+eeprom_info.dj_bias_pwm[i];
                    		if(pwm2 > 2500)pwm2 = 2500;
                    		if(pwm2 < 500)pwm2 = 500;
                    		servo_do[i].aim = pwm2; //舵机PWM赋值,加上偏差的值
                    		servo_do[i].time1 = time1;      //舵机执行时间赋值
                    		float pwm_err = servo_do[i].aim - servo_do[i].cur;
                    		servo_do[i].inc = (pwm_err*1.00)/(time1/SERVO_TIME_PERIOD); //根据时间计算舵机PWM增量
						}
                } else if((index >= SERVO_NUM) || (pwm1 > 2500) ||(pwm1 < 500)|| (time1>10000)) {  //如果舵机号和PWM数值超出约定值则跳出不处理
                } else {
                    servo_do[index].aim = pwm1+eeprom_info.dj_bias_pwm[index];; //舵机PWM赋值,加上偏差的值
                    if(servo_do[index].aim > 2500)servo_do[index].aim = 2500;
                    if(servo_do[index].aim < 500)servo_do[index].aim = 500;
                    servo_do[index].time1 = time1;      //舵机执行时间赋值
                    float pwm_err = servo_do[index].aim - servo_do[index].cur;
                    servo_do[index].inc = (pwm_err*1.00)/(time1/SERVO_TIME_PERIOD); //根据时间计算舵机PWM增量
                }
                index = pwm1 = time1 = 0;
            }
        }
    }
}
```

这个函数用于解析串口接收的字符串，其中定义了三个关键变量：index、time1、pwm1、pwm2，他们分别代表舵机索引、执行周期和传入的舵机pwm值，加上偏差之后的pwm值。

参数为unit_8类型的指针，指向指令值存放的地址。

```python
if((uart_receive_buf[0] == '#') && (uart_receive_buf[4] == 'P') && (uart_receive_buf[5] == '!')) {
        delay(500);
    }
```
定义接受到形如`#001P!`的指令会暂停500毫秒再执行。

**回读处理：**

```C
if(zx_read_flag) {
  	  //#001P1500! 回读处理
  	  if((uart_receive_buf[0] == '#') && (uart_receive_buf[4] == 'P') && (uart_receive_buf[9] == '!')) {
    	    index = (uart_receive_buf[1]-'0')*100 +  (uart_receive_buf[2]-'0')*10 +  (uart_receive_buf[3]-'0');
			  if(index == zx_read_id) {
 				  zx_read_flag = 0;
      		  zx_read_value = (uart_receive_buf[5]-'0')*1000 + (uart_receive_buf[6]-'0')*100 +  (uart_receive_buf[7]-'0')*10 +  (uart_receive_buf[8]-'0');
			  }
		}
```

回读操作，如果存在回读标记则进行回读处理，在回读处理中检查指令格式是否正确，如果指令格式正确则通过指令中索引为1、2、3的字符确定舵机的索引号，这里的123字符指舵机的ID。
如果索引等于回读的舵机索引，则将回读标记改为0，将回读的值储存，内容和指令的第5678索引位的字符计算出的值。


变量说明：

| 变量名              | 类型           | 说明                 |
| ---------------- | ------------ | ------------------ |
| zx_read_flag     | int          | 指示是否已读标记，0为已读、1为未读 |
| uart_receive_buf | \*unit8      | 指向串口指令的unit8指针     |
| index            | unsigned int | 舵机索引               |
| zx_read_id       | int          | 回读舵机索引             |
| zx_read_value    | int          | 回读指令PWM 值          |

**偏差处理：**

```c
else if((uart_receive_buf[0] == '#') && (uart_receive_buf[4] == 'P') && (uart_receive_buf[5] == 'S') && (uart_receive_buf[6] == 'C') && (uart_receive_buf[7] == 'K')) {
        index = (uart_receive_buf[1]-'0')*100 +  (uart_receive_buf[2]-'0')*10 +  (uart_receive_buf[3]-'0');
        if(index < SERVO_NUM) {
            int bias_tmp = (uart_receive_buf[9]-'0')*100 +  (uart_receive_buf[10]-'0')*10 +  (uart_receive_buf[11]-'0');
            if(bias_tmp < 127) {
            myservo[index].attach(servo_pin[index]);
              if(uart_receive_buf[8] == '+') {
                  servo_do[index].cur = servo_do[index].cur-eeprom_info.dj_bias_pwm[index]+bias_tmp;
                  eeprom_info.dj_bias_pwm[index] = bias_tmp;
              } else if(uart_receive_buf[8] == '-') {
                  servo_do[index].cur = servo_do[index].cur-eeprom_info.dj_bias_pwm[index]-bias_tmp;
                  eeprom_info.dj_bias_pwm[index] = -bias_tmp;
              }
              rewrite_eeprom();
				servo_do[index].cur = 1500;
				servo_do[index].aim = 1500+eeprom_info.dj_bias_pwm[index]; //舵机PWM赋值,加上偏差的值
				servo_do[index].time1 = 100;      //舵机执行时间赋值
				servo_do[index].inc = eeprom_info.dj_bias_pwm[index]/5.000; //根据时间计算舵机PWM增量
              //Serial.print("input bias:");
              //Serial.println(eeprom_info.dj_bias_pwm[index]);
           }
        }
    //停止处理
    }
```

在偏差处理的片段由一个条件判断开始，这里条件判断的意义是当串口指令满足形如 _!000PSCK+100_或者 _！000PSCK-100_ 格式时执行此动作。  
指令中 000代表舵机编号，+-100指在当前的舵机默认的PWM值上加减的误差值。  
偏差处理用于解决 当舵机安装的初始角度不正确时，可以通过偏差处理来调整默认的舵机角度以达到在舵机启动初始化和调整舵机pwm值时能够使舵机的运动基于舵机角度处于中心时的pwm值调整。

变量说明：

|变量名|类型|说明|
|:-:|:-:|:-:|
|uart_receive_buf|*u8|指向串口接收指令的值的指针|
|bias_tmp|int|临时储存偏差值的变量|
|myservo|Servo|舵机类的对象|
|servo_do|struct duoji_struct|舵机数据结构体：  <br>unsigned int aim-舵机目标值  <br>float cur-舵机当前值  <br>unsigned int time1-舵机执行时间  <br>float inc-舵机值增量|
|eeprom_info|struct eeprom_info_t|储存器结构体：|
|||long myversion-当前版本|
|||long dj_record_num-未引用，无意义  <br>byte pre_cmd-预执行指令  <br>int dj_bias_pwm-舵机当前pwm偏差值|

**停止处理**

```C++
else if((uart_receive_buf[0] == '#') && (uart_receive_buf[4] == 'P') && (uart_receive_buf[5] == 'D') && (uart_receive_buf[6] == 'S') && (uart_receive_buf[7] == 'T')) {
        index = (uart_receive_buf[1]-'0')*100 +  (uart_receive_buf[2]-'0')*10 +  (uart_receive_buf[3]-'0');
        if(index < SERVO_NUM) {
              servo_do[index].inc =  0.001;
              servo_do[index].aim = servo_do[index].cur;
        }
}
```

停止处理对应的舵机指令格式为：

```
#舵机IDPDST
```

例如#001PDST指令使1号舵机停止运动。

逻辑是首先是进行指令判断，然后判断舵机索引，如果计算得出的舵机索引小于舵机数量，则此舵机存在，将他的增量调整为0.001并且把目标pwm值调整为当前值，即停止运动。

**运动处理**：

运动处理是整个指令系统的核心部分，代码片段：

```C++
else if((uart_receive_buf[0] == '#') || (uart_receive_buf[0] == '{')) {   //解析以“#”或者以“{”开头的指令
        len = strlen(uart_receive_buf);     //获取串口接收数据的长度
        index=0; pwm1=0; time1=0;           //3个参数初始化
        for(i = 0; i < len; i++) {          //
            if(uart_receive_buf[i] == '#') {        //判断是否为起始符“#”
                i++;                        //下一个字符
                while((uart_receive_buf[i] != 'P') && (i<len)) {     //判断是否为#之后P之前的数字字符
                    index = index*10 + (uart_receive_buf[i] - '0');  //记录P之前的数字
                    i++;
                }
                i--;                          //因为上面i多自增一次，所以要减去1个
            } else if(uart_receive_buf[i] == 'P') {   //检测是否为“P”
                i++;
                while((uart_receive_buf[i] != 'T') && (i<len)) {  //检测P之后T之前的数字字符并保存
                    pwm1 = pwm1*10 + (uart_receive_buf[i] - '0');
                    i++;
                }
                i--;
            } else if(uart_receive_buf[i] == 'T') {  //判断是否为“T”
                i++;
                while((uart_receive_buf[i] != '!') && (i<len)) {//检测T之后!之前的数字字符并保存
                    time1 = time1*10 + (uart_receive_buf[i] - '0'); //将T后面的数字保存
                    i++;
                }
                if(time1<SERVO_TIME_PERIOD)time1=SERVO_TIME_PERIOD;//很重要，防止被除数为0
                if((index == 255) && (pwm1 >= 500) && (pwm1 <= 2500) && (time1<10000)) {  //如果舵机号和PWM数值超出约定值则跳出不处理
						for(int i=0;i<SERVO_NUM;i++) {
                    		pwm2 = pwm1+eeprom_info.dj_bias_pwm[i];
                    		if(pwm2 > 2500)pwm2 = 2500;
                    		if(pwm2 < 500)pwm2 = 500;
                    		servo_do[i].aim = pwm2; //舵机PWM赋值,加上偏差的值
                    		servo_do[i].time1 = time1;      //舵机执行时间赋值
                    		float pwm_err = servo_do[i].aim - servo_do[i].cur;
                    		servo_do[i].inc = (pwm_err*1.00)/(time1/SERVO_TIME_PERIOD); //根据时间计算舵机PWM增量
						}
                } else if((index >= SERVO_NUM) || (pwm1 > 2500) ||(pwm1 < 500)|| (time1>10000)) {  //如果舵机号和PWM数值超出约定值则跳出不处理
                } else {
                    servo_do[index].aim = pwm1+eeprom_info.dj_bias_pwm[index];; //舵机PWM赋值,加上偏差的值
                    if(servo_do[index].aim > 2500)servo_do[index].aim = 2500;
                    if(servo_do[index].aim < 500)servo_do[index].aim = 500;
                    servo_do[index].time1 = time1;      //舵机执行时间赋值
                    float pwm_err = servo_do[index].aim - servo_do[index].cur;
                    servo_do[index].inc = (pwm_err*1.00)/(time1/SERVO_TIME_PERIOD); //根据时间计算舵机PWM增量
                }
                index = pwm1 = time1 = 0;
            }
        }
    }
```

这里是解析运控指令的部分，整体执行的条件是指令满足以 **#** 或者 **{** 开头，即运动部分的指令应当是由#开头的单个指令或者是由{}包裹的组合指令。

初始化参数解释：

|变量名|类型|说明|
|:-:|:-:|:--|
|len|int|指令长度|
|index|int|舵机索引|
|pwm1|int|指定舵机的pwm值|
|time1|int|动作执行周期|
|i|int|指令的字节索引|

主循环的条件是指令的字节索引小于指令的长度。

**指令解析过程：** 循环体内根据指令的字节索引对应的值来判断执行的指令，首先是在索引中判断到#字符则认为是一段指令的开始，随后的三位是舵机的ID，第四位为固定值P，随后的所有字符直到T之前的字符被认为是要调整的舵机PWM值。当字符为T时，检测T之后!之前的数值，并将其保存到time1变量中，这些字符为舵机从当前的PWM值调整到新的PWM值所消耗的时间。  
最后以!结尾，当检测到!时一条指令结束，随后进行第二条指令的判断，即从上述指令解析过程重新开始。

由此可得，运动控制的指令为：

```
{#舵机IDP舵机PWM值T周期!}
```

其中：  
**舵机ID应为三位，不足三位用0补齐。**  
**PMW值应为四位，不足四位用0补齐。**  
**周期应为四位，不足四位用0补齐，周期最大值为9999即9.99秒。**

**串口动作指令**

除上述指令外，还有其他的常用串口通信指令， 所有的指令如下所示：

![小杜的个人图床](http://src.xiaodu0.com/2024/05/19/cb819682deebca673721e5c25e6f6435.png)

![小杜的个人图床](http://src.xiaodu0.com/2024/05/19/d9026067bcdaac0fe9810ea31d437ece.png)

指令解释：

**1、#000P1500T1000!**

解析：“#”和“!”是固定英文格式。000代表ID（范围0-254），必须为 3位，不足补0。比如3号舵机 为“003”而不能为“3”。1500 代表PWM脉冲宽度调制（P）（范围500-2500）， 必须为4位，不足补 0。比如PWM为800，则必须为“P0800”。1000代表TIME时间(T)（范围0-9999），同样必须为 4 位，不足补0，单位ms。比如TIME为500，则必须为“T0500” 该指令可以叠加同时控制多个舵机。多个指令同时使用时（2个或2个以上叠加）需要在整条指令 前后加“{}”，比如：{G0000#000P1602T1000!#001P2500T0000!#002P1500T1000!}

**2、#000PVER!**

解析：读取舵机版本号，返回格式为：#000PV0.97!

**3、#000PID!**

解析：指定ID检测，该指令时读取000的ID，检测当前舵机是否为000 这个ID号，是返回#000P!。 否则无返回，当不知道舵机ID时，发送#255PID! 可返回舵机ID号。

**4、#000PID001!**

解析：指定修改ID，该指令是把000号ID改为001号，修改成功后返回#001P!。不成功无返回。

**5、#000PULK!**

解析：释放后舵机处于制动状态，此时可以用手扳动舵机旋转。在纠正舵机偏差和手动编程时会用 到此功能，成功返回 [#OK](app://obsidian.md/index.html#OK)!。

**6、#000PULR!**

解析：恢复扭力，以舵机当前的位置恢复扭力，成功返回#OK!。

**7、#000PMOD!**

解析：读取舵机当前的工作模式，返回如下：  
[#000PMOD1](app://obsidian.md/index.html#000PMOD1)! ：舵机模式，角度最大范围270度，方向顺时针  
[#000PMOD2](app://obsidian.md/index.html#000PMOD2)! ：舵机模式，角度最大范围270度，方向逆时针  
[#000PMOD3](app://obsidian.md/index.html#000PMOD3)! ：舵机模式，角度最大范围180度，方向顺时针  
[#000PMOD4](app://obsidian.md/index.html#000PMOD4)! ：舵机模式，角度最大范围180度，方向逆时针  
[#000PMOD5](app://obsidian.md/index.html#000PMOD5)! ：马达模式，角度360度，定圈旋转，方向顺时针  
[#000PMOD6](app://obsidian.md/index.html#000PMOD6)! ：马达模式，角度360度，定圈旋转，方向逆时针  
[#000PMOD7](app://obsidian.md/index.html#000PMOD7)! ：马达模式，角度360度，定时旋转，方向顺时针  
[#000PMOD8](app://obsidian.md/index.html#000PMOD8)! ：马达模式，角度360度，定时旋转，方向逆时针

**8、#000PMOD1!**

解析：设置舵机工作模式，默认工作模式为1  
1：舵机模式 270度顺时针  
2：舵机模式 270度逆时针  
3：舵机模式 180度顺时针  
4：舵机模式 180度逆时针  
5：马达模式 360度定圈顺时针模式  
6：马达模式 360度定圈逆时针模式  
7：马达模式 360度定时顺时针模式  
8：马达模式 360度定时逆时针模式  
**设置成功均返回#OK!**

关于定圈定时问题解释：  
定圈模式：若指令为 [#000P1800T1000](app://obsidian.md/index.html#000P1800T1000)! 表示以300（1800-1500）的速度，运行1000圈后停 止，允许误差存在。若T=0000！ 则表示以300（1800-1500）的速度无限循环执行。  
定时模式：若指令为 [#000P1800T1000](app://obsidian.md/index.html#000P1800T1000)! 表示以300（1800-1500）的速度，运行1000S后停止， 允许误差存在。若T=0000！ 则表示以300（1800-1500）的速度无限循环执行。

**9、#000PRAD!**  
解析：读取舵机当前位置，返回格式为#000P1500!。

**10、#000PDPT!**

解析：暂停，舵机运行过程中接收此指令，会停止当前，再接收继续指令后，会接在当前位置继续 运行，成功返回 [#OK](app://obsidian.md/index.html#OK)!。

**11、#000PDCT!**  
解析：配合暂停指令继续操作，比如#001P2500T5000! 发送给舵机，在2000ms的时候发送了 [#000PDPT](app://obsidian.md/index.html#000PDPT)! 指令给舵机，则舵机暂停，保持力矩在停止的位置，再发送#000PDCT!给舵机，则舵 机继续剩余的3000ms结束，成功返回 [#OK](app://obsidian.md/index.html#OK)!。

**12、#000PDST!**  
解析：停止在当前位置，与暂停指令不同的事，之后无法继续执行，需重新执行，返回#OK!。

**13、#000PBD1!**  
解析：设置舵机通信波特率，默认115200。数字参数对应关系为：1-9600，2-19200，3-38400， 4-57600，5-115200，6-128000，7-256000，8-1000000，该指令设置成功后返回#000PBD9600!。

**14、#000PSCK!**  
解析：用于纠正偏差，将当前位置设置为1500中间值，成功返回 [#OK](app://obsidian.md/index.html#OK)!。

**15、#000PCSD!**  
解析：设置舵机启动位置，默认1500，开机自启动范围为0500~2500，成功返回 [#OK](app://obsidian.md/index.html#OK)!。

**16、#000PCSM!**  
解析：去除初始值，使用该命令后，#000PCSD! 指令失效，舵机启动释力状态。成功返回 [#OK](app://obsidian.md/index.html#OK)!。

17、#000PCSR!  
解析：恢复初始值，使用该命令后，舵机启动恢复力矩，#000PCSD! 指令恢复，转到初始值，成功 返回 [#OK](app://obsidian.md/index.html#OK)!。

18、#000PSMI!  
解析：设置舵机最小值，最小值默认为0500，将舵机调节到合适位置后，发送此命令设置。 成功 返回#OK!。

**19、#000PSMX!**  
解析：设置舵机最大值，最大值默认为2500，将舵机调节到合适位置后，发送此命令设置。成功返 回#OK!。

**20、#000PCLE!**  
解析：全恢复出厂设置，ID号恢复000，舵机模式默认1、波特率默认115200、初始值1500、矫正 值1500、最小值0500、最大值2500，成功返回 [#OK](app://obsidian.md/index.html#OK)!。

**21、#000PRTV!**  
解析：获取温度和电压，成功返回 [#000T25V07](app://obsidian.md/index.html#000T25V07)!

**22、#000PSTB!**  
解析：读取设置温度和电压。

**23、#000PSTB=60!**  
解析：设置释放扭力阈值温度为60


**常用动作指令**：

| 指令                                                             | 说明            |
| -------------------------------------------------------------- | ------------- |
| {#001P1200T1000!#002P1900T1000!#003P1100T1000!#005P1000T2000!} | 向开发板方向抓取      |
| {#001P1200T2000!#002P1900T2000!#003P1100T2000!#005P1500T3000!} | 向开发板方向放置      |
| {#001P1500T1000!#002P1500T1000!#003P1500T1000!}                | 回正为垂直状态（爪子不动） |
| {#001P1500T1000!#002P1500T1000!#003P1500T1000!#005P1500T1000!} | 回正为垂直状态（爪子张开） |


### (2).串口通信程序设计

比赛的流程是机械狗在场地中自动运动到指定的物料存放区，然后操作机械臂抓取物料，再将物料放置在物料卸载区。

运动部分全部由C++实现，在交互上，考虑两种备选方案：

1. 完全通过C++实现运动和串口通信
2. 在C++实现运动的同时，将运动部分封装的动作封装为Python，并结合shell交由C++调用。

由于完全通过C++实现控制需要安装Serial库和编写相关的代码，这个工作比较复杂，为了验证交互设计的猜想，即能够通过串口通信实现机械狗控制机械臂，首先考虑使用较为简单的Python来实现串口通信，并在机械狗上运行测试。

Arduino单片机的上位机串口通讯要首先安装CH340驱动程序：

```bash
sudo apt-get install git 
git clone https://github.com/juliagoda/CH341SER.git 
cd CH341SER 
make 
sudo make load
```

安装完成之后，再安装Python需要的相关依赖：

```
pySerial
time
```

将机械臂连接到机械狗之后，通过Python获取端口信息：

```python
#coding=UTF-8
import serial
import serial.tools.list_ports
import time
def getPorts():
    ports_list = list(serial.tools.list_ports.comports())
    if len(ports_list) <= 0:
        print("无串口设备。")
    else:
        print("可用的串口设备如下：")
        for comport in ports_list:
            print(list(comport)[0], list(comport)[1])
  
getPorts()
```

输出：

```
可用的串口设备如下：
('/dev/ttyUSB4', 'USB Serial')
('/dev/ttyUSB3', 'EG25-G')
('/dev/ttyUSB2', 'EG25-G')
('/dev/ttyUSB1', 'EG25-G')
('/dev/ttyUSB0', 'EG25-G')
('/dev/ttyAMA0', 'ttyAMA0')
```

其中USB Serial即为串口USB端口，也就是机械臂连接的USB端口。

测试发送指令：

```python
ser = serial.Serial(port="/dev/ttyUSB4", baudrate=115200, timeout=1)

ser.write(b"{#000P1000T1000!#001P1200T1000!#002P1900T1000!#003P1100T1000!#005P1000T2000!}")

time.sleep(5)

ser.write(b"{#001P1500T1000!#002P1500T1000!#003P1500T1000!}")
```

运行成功。

### (3).交互程序封装

在主函数中封装了获取端口与发送指令的程序：
```python
import time  
import serial  
import serial.tools.list_ports  
import action  
def getPorts():  
    ports_list = list(serial.tools.list_ports.comports())  
    if len(ports_list) <= 0:  
        print("无串口设备。")  
    else:  
        print("可用的串口设备如下：")  
        for comport in ports_list:  
            print(list(comport)[0], list(comport)[1])  
  
def doAction(actions):  
    for action in actions:  
        ser.write(b"%s"%action['commend'])  
        time.sleep(action['delay'])  
  
ser = serial.Serial(port="COM11", baudrate=115200, timeout=1)  
doAction(action.init)  
doAction(action.craw)  
doAction(action.stand)  
# ser.write(b"#005P1500T1000!")  
getPorts()
```

`doAction`方法根据给定的指令序列执行动作，预定义的指令序列如下：
```python
init=[  
{  
        "commend":b"#000P1600T1000!",  
        "delay":0  
    },  
    {  
        "commend":b"#001P1500T1000!",  
        "delay":0  
    },  
    {  
        "commend":b"#002P1500T1000!",  
        "delay":0.5  
    },  
    {  
        "commend": b"#003P1500T1000!",  
        "delay": 0  
    },  
    {  
        "commend": b"#004P1500T1000!",  
        "delay": 0  
    },  
    {  
        # "time":500,  
        "commend": b"#005P1500T1000!",  
        "delay": 0.5  
    },  
]  
stand=[  
{  
        "commend":b"#000P1500T1000!",  
        "delay":1  
    },  
    {  
        "commend":b"#001P1450T1000!",  
        "delay":1  
    },  
    {  
        "commend":b"#002P1500T1000!",  
        "delay":1  
    },  
    {  
        "commend": b"#003P1500T1000!",  
        "delay": 1  
    },  
    {  
        "commend": b"#004P1500T1000!",  
        "delay":1  
    },  
]  
craw=[  
{  
        "commend":b"#003P1600T1000!",  
        "delay":0.5  
    },  
    {  
        "commend":b"#001P1300T1000!",  
        "delay":1  
    },  
    {  
        "commend":b"#002P1200T1000!",  
        "delay":1  
    },  
    {  
        "commend":b"#003P1800T1000!",  
        "delay":1  
    },  
{  
        "commend":b"#005P0900T1000!",  
        "delay":1  
    }  
  
]
```

每个动作组变量是一个列表类型的数据，每个列表项是一个字典，字典中的`commend`键为对应的串口指令，`delay`键为执行此指令之后暂停的时间。
采用延迟是为了防止当前动作还未执行完就执行下一个动作而产生预料之外的情况。

在机器人的运控板中上传此示例程序，通过python3执行即可实现交互，但是仍然有需要优化的地方，在控制时调用程序执行固定的动作显然不是一个好的方法，于是我们将其通过`argparse`库封装为shell程序，使其可以通过shell 调用并且指定相关参数。

```python
import time
import serial
import serial.tools.list_ports
import argparse
import action

def getPorts():
    """
    列出所有可用的串口设备。
    """
    ports_list = list(serial.tools.list_ports.comports())
    if len(ports_list) <= 0:
        print("无串口设备。")
    else:
        print("可用的串口设备如下：")
        for comport in ports_list:
            print(list(comport)[0], list(comport)[1])

def doAction(actions, ser):
    """
    执行一系列动作命令。
    
    参数:
    actions: 动作列表，每个动作包含 'commend' 和 'delay'。
    ser: 串口对象。
    """
    for action in actions:
        ser.write(b"%s" % action['commend'])
        time.sleep(action['delay'])

def main():
    """
    主函数，解析命令行参数并执行相应动作。
    """
    parser = argparse.ArgumentParser(description="串口动作控制程序")
    parser.add_argument("--port", type=str, required=True, help="串口端口，例如 COM11")
    parser.add_argument("--baudrate", type=int, default=115200, help="波特率，默认 115200")
    parser.add_argument("--timeout", type=int, default=1, help="串口超时时间，默认 1 秒")
    parser.add_argument("--P", type=str, help="P 参数")
    parser.add_argument("--T", type=str, help="T 参数")
    parser.add_argument("--action", type=str, required=True, choices=['init', 'craw', 'stand'], help="要执行的动作")

    args = parser.parse_args()

    try:
        ser = serial.Serial(port=args.port, baudrate=args.baudrate, timeout=args.timeout)
        print(f"已连接到串口 {args.port}，波特率 {args.baudrate}")

        actions = getattr(action, args.action)
        doAction(actions, ser)

        if args.P and args.T:
            command = f"#{args.P}P{args.T}!"
            ser.write(command.encode())
            print(f"发送命令: {command}")

        getPorts()

    except serial.SerialException as e:
        print(f"无法连接到串口 {args.port}: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(f"已关闭串口 {args.port}")

if __name__ == "__main__":
    main()

```

在优化之后，可以通过shell调用此程序来实现执行相关动作、指定端口、波特率、P参数（pwm值）和T值（执行时间）。
相关解释如下：

`getPorts()`
列出所有可用的串口设备。

`doAction(actions, ser)`
执行一系列动作命令。
- **参数**:
    - `actions`: 动作列表，每个动作包含 `commend` 和 `delay`。
    - `ser`: 串口对象。

 `main()`
主函数，解析命令行参数并执行相应动作。
- **参数**:
    - `--port`: 串口端口，例如 `COM11`。
    - `--baudrate`: 波特率，默认 `115200`。
    - `--timeout`: 串口超时时间，默认 `1` 秒。
    - `--P`: P 参数。
    - `--T`: T 参数。
    - `--action`: 要执行的动作（`init`、`craw` 或 `stand`）。

在机器人中，通过深度相机获取点云图数据来计算物体的相对位置，并且将其转换为机械臂的控制参数，调用控制程序来实现物体的抓取。

```python
import subprocess
import cv2
import pcl
import numpy as np

def get_point_cloud(depth_image, camera_intrinsics):
    """
    根据深度图像和相机内参生成点云图。
    
    参数:
    depth_image: 深度图像。
    camera_intrinsics: 相机内参矩阵。
    
    返回:
    point_cloud: 生成的点云图。
    """
    height, width = depth_image.shape
    fx, fy = camera_intrinsics[0, 0], camera_intrinsics[1, 1]
    cx, cy = camera_intrinsics[0, 2], camera_intrinsics[1, 2]
    
    points = []
    for v in range(height):
        for u in range(width):
            z = depth_image[v, u] / 1000.0
            if z == 0:
                continue
            x = (u - cx) * z / fx
            y = (v - cy) * z / fy
            points.append([x, y, z])
    
    point_cloud = pcl.PointCloud(np.array(points, dtype=np.float32))
    return point_cloud

def extract_object_position(point_cloud):
    """
    从点云图中提取物体位置。
    
    参数:
    point_cloud: 点云图。
    
    返回:
    (x, y, z): 物体在相机坐标系中的位置。
    """
    # 假设物体是点云中最大的簇
    seg = point_cloud.make_EuclideanClusterExtraction()
    seg.set_ClusterTolerance(0.02)
    seg.set_MinClusterSize(100)
    seg.set_MaxClusterSize(25000)
    clusters = seg.Extract()
    
    largest_cluster = clusters[0]
    object_points = point_cloud.extract(largest_cluster)
    centroid = np.mean(object_points.to_array(), axis=0)
    return centroid

def calculate_grasp_parameters(position):
    """
    根据物体位置计算机械臂抓取所需的控制参数。
    
    参数:
    position: 物体位置 (x, y, z)。
    
    返回:
    P: 抓取位置参数
    T: 抓取时间参数
    """
    x, y, z = position
    P = f"{x + y:.2f}"
    T = f"{z:.2f}"
    return P, T

def main():
    # 假设已经获取到深度图像和相机内参
    depth_image = cv2.imread('depth_image.png', cv2.IMREAD_UNCHANGED)
    camera_intrinsics = np.array([[525.0, 0.0, 319.5],
                                  [0.0, 525.0, 239.5],
                                  [0.0, 0.0, 1.0]])
    
    point_cloud = get_point_cloud(depth_image, camera_intrinsics)
    position = extract_object_position(point_cloud)
    P, T = calculate_grasp_parameters(position)
    
    port = "COM11"
    baudrate = 115200
    action = "craw"
    
    subprocess.run([
        "python", "serial_control.py",
        "--port", port,
        "--baudrate", str(baudrate),
        "--action", action,
        "--P", P,
        "--T", T
    ])

if __name__ == "__main__":
    main()

```


其中：
- **`get_point_cloud(depth_image, camera_intrinsics)`**：将深度图像和相机内参转换为点云图。
- **`extract_object_position(point_cloud)`**：从点云图中提取物体的位置。假设物体是点云中最大的簇。
- **`calculate_grasp_parameters(position)`**：根据物体位置计算机械臂的控制参数`P`和`T`。
- **`main()`**：
    - 获取深度图像和相机内参。
    - 生成点云图并提取物体位置。
    - 计算抓取参数并调用`serial_control.py`脚本执行抓取动作。

# Part II 机器人设计

## 1. 问题分析 

在设计机器人实现指定任务之前，首先需要明确作品需要解决什么问题。

首先，根据赛程规则，我们主要需要实现的部分是：
1. 自动循迹驾驶走完赛道。
2. 注意环岛和十字路口以及双岔路口，选择合适的路径。
3. 在环岛中心倾倒物资。
4. 在启停区完成启动和停止。
5. 协调机械臂完成物资的识别与抓取。

其中机械臂与机器人交互的部分在title #3 Part I 部分已经说明，这里只做简单的阐述。

### (1). 机械臂与机器人的交互

机器人与机器臂交互部分，涉及的主要问题是机器人与机械臂如何交互？在交互过程中需要传递哪些数据，以及整个交互的流程。

由于物资抓取是在比赛开始之前，所以在机器人上场行走之前就要完成物资的抓取工作，因此设计了机械臂抓取物资动作的程序，通过PC连接到机器人，启动程序机器人即通过串口发送数据来控制机械臂抓取物资，也就是，抓取物资的实现是通过串口通信的方式实现的。

交互过程中，由机器人的深度相机来获取物资的位置信息，通过位置信息计算出相对位置再计算机械臂各个舵机的PWM值，将PWM和对应的执行时间通过串口发送给机械臂的控制板卡。

整个交互流程是：启动机器人、连接到机械人执行识别与抓取程序、机器人通过串口发送数据、机械臂执行动作。

### (2). 物资识别的实现

物资识别仍然是在机器人的系统中实现的，我们通过opencv来实现物资的识别，物资有四种：圆柱体、三棱锥、正方体、半球。

要实现物资识别，首先通过opencv获取图像，然后通过颜色识别和形状识别来确定物体的形状。

我们使用颜色过滤以及形状检测来确定物资，以顶点的数量的划分物体形状：
- **三棱锥**：检测到3个顶点。
- **正方体**：检测到4个顶点，并且长宽比接近1。
- **圆柱体**：检测到4个顶点，但长宽比不接近1。
- **半球**：检测到超过8个顶点的圆形轮廓。


### (3). 启动与停止

启动与停止依赖于运动SDK与颜色识别实现，首先是启动部分，我们的整体程序是多线程实现的，由于启动在整个流程的开始阶段，停止在结束阶段，因此在启动阶段我们通过在主线程中给定一个固定的左右偏移量使机器人运动到赛道中，这一部分在整个程序的启动时，控制线程初始化之前。

停止部分，由于需要识别到标志来确定已经到达启停区，我们通过颜色标记实现，在启停区的后方贴一个黑色标签，此标签代表已经完成任务流程，机器人将关闭获取图像和循迹的线程，并且通过向前向右运动回到启停区，最后关闭运动程序。

### (4). 自动循迹

#### a. ROS与LCM

自动循迹是整个流程中最基础、最重要的阶段，这一部分我们考虑了非常多的方案，首先考虑了通过ROS结合LCM的方式实现，这一想法的具体内容是：
通过在终端与PC之间建立连接，编写键盘控制程序，通过PC键盘来操作机器人完成整个脸赛道流程，将ROS信号利用”convert.h”转换成真正的控制代码，然后结合LCM将转换后的CMD结构体进行保存，并再次复现。

但是在经过多次测试，这种方式实际上仍然是依赖于手动操作，无非是在外在看起来是由自动部分，并且最严重的问题是由于操作手的失误、每一次运行的状况、舵机的转速等等一些列因素，机器人始终无法准确的复现操作流程，于是我们决定放弃这种方式。

随后我们采用计算机视觉的方法进行循迹，根据摄像头实时的处理图像，依据图像数据来确定机器人的位置，并决定接下来如何运动。

#### b. 计算颜色差值运动

首先我们考虑的是通过计算赛道主路线即黄色路线的部分与赛道边缘即白色部分的差值来实现位置控制，首先机器人是恒定速度行走的，然后根据二者的差值水平横移动使图像保持在中间，但是这样做实际上存在很大的风险：机器人总会意料之外的出界，并且导致图像丢失无法继续运动，由于横向移动的误差，机器人无法准确的在赛道中保持在中线位置。

另一方面，这种方式在直道上表现偶尔会良好，但是在遇到弯道时水平移动显然无法解决问题，于是我们又引入了转弯，通过计算白色部分和黄色部分的范围，当白色部分大于黄色部分时，说明机器人即将出界或者到达了转弯处，这时候需要调整角度，这种方法仍然存在一个弊端：当机器人已经出界时再转弯，很容易产生错误的轨迹，进而导致运动无法继续下去。

另一方面，我们考虑计算黄色与白色的中线与整个图像中线的差来纠正位置，但是中线差值转换速度和角度是一个很复杂的过程，并且由于误差的存在，即使我们引入了PID算法也无法完美的解决这个问题，随着多次测试和调试失败，我们最终也决定放弃这个方案。

#### c. 分割图像区域进行计算

分割图像区域是我们的最终方案也是三种方案中效果最好的方案，实际上我们引入了感兴趣的区域的思路，通过将图像分割为三个等份，然后计算每三个图像中黄色部分的中点根据这三个中点的取值，来计算黄色部分的扭曲程度进而确定机器狗需要调整的角度。

这一部分的具体思路是：通过摄像头获取实时视频流，并在图像处理后控制机器人沿着特定路线行驶。感兴趣区域（ROI，Region of Interest）用于在图像中划定特定区域，以便更准确地进行颜色检测和路径规划。

首先，获取视频流并保存到队列中，由于读取和运动控制部分需要分开执行，因此我们通过多线程的方式读取视频帧，将其储存到队列中，并且同时在运动控制线程中读取图像数据。


然后，进行颜色检测与路径规划，我们通过使用颜色阈值（HSV范围）进行颜色检测，识别图像中的黄色区域，并且定义感兴趣的区域，将图像分为上、中、下三个部分，分别检测每个部分的黄色区域，以确定路径方向和转角角度。
最后，根据颜色检测结果和计算的角度，调整机器人速度和转弯角度，实现循迹。

实现分割的结果如图所示：
![小杜的个人图床](http://src.xiaodu0.com/2024/06/30/88c92d6b241524ce8aa69cf5b9de49ef.png)

### (5).环岛和十字路口处理

在完成视觉部分之后，我们考虑确定环岛 的位置，并且执行进入环岛的控制逻辑，在进入环岛之后实现物质的倾倒以及在完成物质倾倒之后驶出环岛。由于我们先前的控制程序包含寻迹的部分，因此在十字路口也能够很妥善的处理，不需要再做额外的代码。

为了对环岛进行识别，我们对每一个环岛的入口处贴下了一个不同颜色的标签，在一号环岛贴绿色的标签，二号环岛贴红色的标签，三号环岛贴蓝色的标签，四号环岛贴紫色的标签。

依据颜色识别对标志进行检测，如果检测到相关的颜色，则进行颜色区域的判断，根据反复检测统计，识别到的标签形状大多在100-120范围内浮动，于是当检测到有上述三种颜色，并且颜色的范围是100\*100到120\*120的时候，则判断其为环岛标签，执行环岛业务的处理流程。

为了防止在驶出环岛的时候再次执行处理环岛的业务，我们定义了记录四个环岛状态的列表，初始状态都是0，当被检测到之后，开始处理业务逻辑则变为1，在进行环岛业务之前同样判断当颜色对应的环岛是否已经被处理。


### (6).双岔路口处理

在使用视觉循迹开始，双岔路口我们遇到一个问题：当机器人选择一个双岔路口走完之后，又回头走另一个分叉路返航了，经过多次展示摄像头实时数据和标注转角的调试测试之后，我们发现是在机器人刚驶出双岔路之后，两条路合并这时候路线被判定为转向，并且转向角度很大，而实际上这时候虽然要进行转弯到直道的操作，但是转角是比较小的，于是我们通过限制转角，当角度超过60度时则不进行任何操作。


## 2.技术方案

### (1).整体设计

在整体的技术实现上，我们采用Python语言进行业务开发，结合Unitree_leddeg_sdkV3,8的pythonSDK来设计整体业务。

我们使用的循迹部分用到了下巴处的摄像头，因此在头部nano上需要设计摄像头视频流发送程序，起初我们使用的是Gstreamer推流，但是在运动控制板卡安装opencv时没有启用Gstreamer扩展，重新编译安装需要花费太多时间，于是我们考虑换个思路，使用ffmpeg进行推流，但是结果是，由于没有Gstreamer支持，opencv仍然无法正确处理图像帧，导致程序一直报错，最后我们采用性能比较低的方法，在头部板卡安装falsk进行推流，首先通过摄像头实时捕获视频，并通过Flask框架提供的Web服务将视频流以HTTP流的形式发送到网页上。

在运动控制板卡上，由于falsk推送的是流数据，通过Request库来获取http数据流，从数据流中组合图像，并且保存到队列中供运动程序读取。
由于运动部分需要通过sdk通信实现，我们将这一部分封装为一个websocket server服务器，在需要与SDK通信时发送ws消息来实现通信。

最后，通过一个主程序将这个部分结合起来，程序启动时实例化ws对象， 创建两个线程用于处理图像帧和运动控制。

### (2).图像发送部分与接收

首先是图像发送部分，通过OpenCV捕获摄像头数据，并进行图像处理，用Flask框架创建Web应用，并通过HTTP流式传输视频数据。然后定义生成器函数 `gen`，将摄像头数据转换为JPEG格式，并以流的形式发送给客户端，实现实时视频流传输。

图像发送之前需要对图像进行处理，这里涉及的处理非常简单，只是通过opencv对图像进行裁剪和缩放以减少流数据，加快传输速率。

在图像接收上，由于头部有两个相机，我们对两个相机开启不同的flask路由，在接收端，封装一个函数，接受一个参数指定获取哪个摄像头的流，并且初始化一个字节串用于保存数据块，在读取视频流数据时找到JPEG图像的起始标志`\xff\xd8`与结束标志`\xff\xd9`以此将字节串组合成一副完成的jpg图像，如果找到一帧完整的JPEG图像则提取完整的JPEG图像，截断已经处理过的数据，最后将图像转码，储存为ndaarray格式存放到队列中，以供opencv进行处理。

具体的步骤是：
定义一个名为`getFrame`的函数，它接收一个参数`n`。根据`n`的值，函数会从不同的流对象（`stream1`或`stream0`）中读取视频流数据。

首先，初始化一个空的字节串`bytes_data`用于存储读取到的数据块。然后，使用`iter_content`方法以每次1024字节的大小迭代读取视频流数据。

在循环中，将每个数据块添加到`bytes_data`中。接着，查找JPEG图像的起始标志（`b'\xff\xd8'`）和结束标志（`b'\xff\xd9'`）。如果找到了一个完整的JPEG图像（即起始标志和结束标志都存在），则提取该图像并将其解码为OpenCV图像格式。最后，将解码后的图像写入队列（通过调用`writeQueue`函数）。

在队列中，我们将新的图像帧存入队列，如果队列已满，则移除最旧的帧，这样做是为了减少队列占用的内存，同时在需要读取时，读取队列中最新的图像帧。

在发送端，由于使用flask开发，我们还可以在浏览器中查看实时的摄像头数据，并且具有非常低的延迟。

### (3).使用ws控制机器人

为了便于使用SDK在内网与主控板通信实现运动控制，我们在运动控制板卡创建了一个websocket服务器，首先导入所需的库：socket、threading和json。其中，socket库用于网络通信，threading库用于多线程处理，json库用于解析JSON格式的数据。然后创建一个名为unitree_robot的Unitree_Robot_High对象，用于控制机器人。
然后定义一个名为client的类，用于表示客户端连接。这个类包含以下方法：
    - **init**：初始化客户端对象，包括地址、端口、用户名和套接字。
    - send：向客户端发送消息。
    - recv：从客户端接收消息，如果接收失败则返回False。
    - close：关闭客户端套接字。
    - id：返回客户端的唯一标识符，即地址和端口的组合。
接着定义一个名为new_client的函数，用于处理客户端连接。这个函数会不断接收客户端发送的命令，并将其解析为JSON格式。然后，根据解析出的命令调用unitree_robot对象的execute方法来控制机器人。如果在处理过程中出现异常，函数会捕获异常并输出错误信息。最后，关闭客户端连接并从客户端列表中移除该客户端。
创建一个socket对象s，绑定到指定的IP地址和端口，并开始监听连接请求。
使用一个无限循环来接受新的客户端连接。每当有新的连接请求时，创建一个新的client对象，并将其添加到客户端列表中。然后，为每个新客户端启动一个新的线程来处理其请求。


我们在运动控制板卡定义了一个名为 `RobotConnector` 的类，用于与服务端建立连接并发送控制指令：
首先，定义一个名为 `RobotConnector` 的类。
在类的构造函数，接收两个参数 `ip_address` 和 `port`，分别表示机器人的 IP 地址和端口号。默认值分别为 `192.168.123.161` 和 `8000`。
然后创建一个元组 `address_server`，包含 IP 地址和端口号。
通过`self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`：创建一个套接字对象 `self.s`，使用 IPv4（`AF_INET`）和 TCP（`SOCK_STREAM`）协议。
使用套接字对象 `self.s` 连接到服务器，服务器地址为 `address_server`。
最重要的方法是`robot_high_control(self, mode=2, gaitType=2, speedLevel=0, footRaiseHeight=0, bodyHeight=0, euler=[0,0,0], velocity=[0,0], yawSpeed=0.0, reverve=0)`：定义一个名为 `robot_high_control` 的方法，用于向机器人发送高级控制指令。该方法接收多个参数，如 `mode`、`gaitType` 等，用于指定机器人的运动模式、步态类型等。
最后，将传入的参数组成一个列表 `data`，使用 `json.dumps()` 方法将列表 `data` 转换为 JSON 格式的字符串。再将 JSON 格式的字符串编码为 UTF-8，转换为字节串并发送到服务器。

### (4). 赛项业务实现

在最终的业务实现中，我们首先导入`asyncio`, `time`, `numpy`, `cv2`, `requests`, `threading` 等库用于异步操作、时间处理、数组操作、图像处理、网络请求和多线程处理。

导入`Camera` 和 `RobotConnector` 类来自自定义模块 `core.Camera` 和 `core.robot_connector`，分别用于处理摄像头图像和机器人连接。

然后在main.py控制程序中定义了各个颜色的范围区间，然后实例化视频流对象用于读取视频流，定义倾倒区列表和运行停止标志用于控制线程的执行。

在程序启动时，首先通过发送ws消息控制机器人移动到赛道上，然后创建图像读取线程和运动控制线程。

在图像读取线程中，循环获取流并截图，将图像储存到队列中。

在业务主线程中，首先开启一个死循环，在循环中第一步从队列读取图像，获取图像的高度和宽度，再执行颜色判断的部分，当有对应的颜色时，判断颜色的区间以及是否为读取，如果没有被读取，则进行环岛业务操作，否则接着执行下面的代码。

在主要的运动部分，通过图像区域分割法来计算角度，同时限制当角度在15和45之间时调整方向，调整的数值是角度/10即舵机线速度，如果需要调整角度，则指定yawspeed 为 angle/10，否则就只执行直行消息，并且在这两个消息发送间隔0.02秒以使机器人的响应更加平滑。

### (5).颜色提取

我们定义一个函数名为`get_color_block`寻找图像中指定颜色范围的区域：使用HSV颜色空间定义颜色范围，通过形态学操作精炼掩膜，然后找到最大的颜色区域。
函数接受的参数：
img: 输入的BGR图像。  
color_lower: 颜色范围的下限，以HSV格式表示。  
color_upper: 颜色范围的上限，以HSV格式表示。  
square: 最小区域面积，用于过滤较小的色块，默认为None（不进行过滤）

首先，将BGR颜色空间转为HSV颜色空间，使用`cv2.cvtColor()`方法，然后创建颜色掩膜，通过`cv2.inRange()`，再创建一个5x5的核，用于进行形态学操作，通过opencv找到颜色掩膜的轮廓，找到面积最大的轮廓来获取最大的轮廓的边界框 (x, y, w, h)，其中，x:颜色区域起始的x坐标，Y为y坐标，w为区域宽度，y为区域高度。

然后检查是否满足最小面积要求，如果满足则返回颜色区域信息，否则，返回None。

### (6).计算转角

这一部分是运动的核心。
代码的主要步骤：
1. 将输入的图像帧调整为640x480像素大小。
2. 将图像从BGR颜色空间转换为HSV颜色空间。
3. 应用颜色阈值以提取黄色道路标记。
4. 初始化方向和角度信息列表。
5. 定义三个感兴趣的区域（ROI），分别位于图像的上部、中部和下部。
6. 对于每个ROI，找到黄色区域的轮廓。
7. 计算每个黄色区域的中心点。
8. 计算转弯角度，即中心点与图像中心的水平距离所对应的角度。
9. 根据计算出的角度判断车辆应该向左转、向右转还是直行。
10. 返回最终的方向和角度以及带有可视化信息的输出帧。

### (7).物料识别

首先导入cv2（OpenCV）和numpy库。cv2用于图像处理，numpy用于数值计算。

然定义辅助函数，包括`nothing`、`create_trackbar_window`、`get_trackbar_values`、`filter_red_objects`和`detect_shapes`。这些函数分别用于创建滑动条窗口、获取滑动条的值、过滤红色物体、检测形状等。

创建滑动条窗口：`create_trackbar_window`函数创建一个名为"Trackbars"的窗口，并在其中添加了一系列滑动条，用于调整HSV颜色空间的阈值。

获取滑动条的值：`get_trackbar_values`函数从滑动条中获取当前设置的阈值，以便在后续的处理中使用。

过滤红色物体：`filter_red_objects`函数接收一个图像和一个HSV颜色空间的阈值范围，然后使用`cv2.inRange`函数根据阈值范围创建一个掩码，该掩码仅保留红色物体的区域。最后，使用`cv2.bitwise_and`函数将原始图像与掩码相结合，得到仅包含红色物体的图像。
检测形状：`detect_shapes`函数接收一个图像和一个掩码，然后使用`cv2.findContours`函数找到掩码中的轮廓。对于每个轮廓，它计算其面积并忽略较小的轮廓。

然后，使用`cv2.approxPolyDP`函数对轮廓进行多边形逼近，并根据多边形的顶点数量判断形状类型（三角形金字塔、立方体、圆柱体或半球）。最后，使用`cv2.drawContours`函数在图像上绘制轮廓，并使用`cv2.putText`函数在图像上标注形状类型。

主函数：`main`函数首先打开摄像头并创建一个滑动条窗口。然后，它进入一个循环，不断从摄像头读取图像，并获取滑动条的值。接着，它调用`filter_red_objects`函数过滤红色物体，并调用`detect_shapes`函数检测形状。显示过滤后的图像和原始图像。


## 3. 比赛程序

### (1).Nano板卡

#### a.图像发送程序

webcamera.py:

```python
  
from flask import Flask, render_template, Response  
import cv2  
from picture_processing import get_img_middle #, undistort  
  
raw_size = [928,800]  
rect_size = [400,300]  
rect_size_ = (640,480)  
vid0 = cv2.VideoCapture("/dev/video0")  
vid1 = cv2.VideoCapture("/dev/video1")  
vid0.set(cv2.CAP_PROP_FRAME_WIDTH, raw_size[0])  
vid0.set(cv2.CAP_PROP_FRAME_HEIGHT, raw_size[1])  
vid1.set(cv2.CAP_PROP_FRAME_WIDTH, raw_size[0])  
vid1.set(cv2.CAP_PROP_FRAME_HEIGHT, raw_size[1])  
  
def get_frame(n):  
    if n==0:  
        frame = vid0.read()[1]  
        # frame = undistort(frame)  
        frame = get_img_middle(frame, rect_size)  
        frame = cv2.resize(frame, rect_size_)  
        return frame  
    if n==1:  
        frame = vid1.read()[1]  
        # frame = undistort(frame)  
        frame = get_img_middle(frame, rect_size)  
        frame = cv2.resize(frame, rect_size_)  
        return frame  
  
def get_frame_byte(n):  
        img = get_frame(n)  
        return cv2.imencode('.jpg', img)[1].tobytes()  
  
  
app = Flask(__name__)  
  
@app.route('/')  
def index():  
    """Video streaming home page."""  
    return render_template('index.html')  
  
  
def gen(n):  
    """Video streaming generator function."""  
    yield b'--frame\r\n'  
    while True:  
        frame = get_frame_byte(n)  
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'  
  
  
@app.route('/video1')  
def video1():  
    """Video streaming route. Put this in the src attribute of an img tag."""  
    return Response(gen(1),  
                    mimetype='multipart/x-mixed-replace; boundary=frame')  
  
@app.route('/video2')  
def video2():  
    """Video streaming route. Put this in the src attribute of an img tag."""  
    return Response(gen(0),  
                    mimetype='multipart/x-mixed-replace; boundary=frame')  
  
  
if __name__ == '__main__':  
    app.run(host='192.168.123.13', port=5000, threaded=True)
```


#### b.图像处理程序

picture_processing.py:

```python
  
from flask import Flask, render_template, Response  
import cv2  
from picture_processing import get_img_middle #, undistort  
  
raw_size = [928,800]  
rect_size = [400,300]  
rect_size_ = (640,480)  
vid0 = cv2.VideoCapture("/dev/video0")  
vid1 = cv2.VideoCapture("/dev/video1")  
vid0.set(cv2.CAP_PROP_FRAME_WIDTH, raw_size[0])  
vid0.set(cv2.CAP_PROP_FRAME_HEIGHT, raw_size[1])  
vid1.set(cv2.CAP_PROP_FRAME_WIDTH, raw_size[0])  
vid1.set(cv2.CAP_PROP_FRAME_HEIGHT, raw_size[1])  
  
def get_frame(n):  
    if n==0:  
        frame = vid0.read()[1]  
        # frame = undistort(frame)  
        frame = get_img_middle(frame, rect_size)  
        frame = cv2.resize(frame, rect_size_)  
        return frame  
    if n==1:  
        frame = vid1.read()[1]  
        # frame = undistort(frame)  
        frame = get_img_middle(frame, rect_size)  
        frame = cv2.resize(frame, rect_size_)  
        return frame  
  
def get_frame_byte(n):  
        img = get_frame(n)  
        return cv2.imencode('.jpg', img)[1].tobytes()  
  
  
app = Flask(__name__)  
  
@app.route('/')  
def index():  
    """Video streaming home page."""  
    return render_template('index.html')  
  
  
def gen(n):  
    """Video streaming generator function."""  
    yield b'--frame\r\n'  
    while True:  
        frame = get_frame_byte(n)  
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'  
  
  
@app.route('/video1')  
def video1():  
    """Video streaming route. Put this in the src attribute of an img tag."""  
    return Response(gen(1),  
                    mimetype='multipart/x-mixed-replace; boundary=frame')  
  
@app.route('/video2')  
def video2():  
    """Video streaming route. Put this in the src attribute of an img tag."""  
    return Response(gen(0),  
                    mimetype='multipart/x-mixed-replace; boundary=frame')  
  
  
if __name__ == '__main__':  
    app.run(host='192.168.123.13', port=5000, threaded=True)
```

#### c.启动程序

start.sh:
```bash
#!/bin/sh  
  
ps -aux | grep point_cloud_node | awk '{print $2}' | xargs kill -9  
ps -aux | grep mqttControlNode | awk '{print $2}' | xargs kill -9  
ps -aux | grep live_human_pose | awk '{print $2}' | xargs kill -9  
ps -aux | grep example_point | awk '{print $2}' | xargs kill -9  
  
python3 webcamera.py  
# ./UnitreecameraSDK/bins/putimagetrans 2
```


### (2).控制服务端

#### a. websocket服务端

server_robotcontrol.py:

```python
import socket  
import threading  
import json  
  
from unitree_python_sdk import Unitree_Robot_High  
unitree_robot = Unitree_Robot_High()  
  
clients = {}  
  
class client(object):  
    def __init__(self, socket, addr, username):  
        self.addr = addr[0]  
        self.port = addr[1]  
        self.username = username  
        self.socket = socket  
      
    def send(self, msg):  
        self.socket.send(msg)  
      
    def recv(self, mtu=1024):  
        try:  
            data = self.socket.recv(mtu)  
            if not data:  
                return False  
            return data  
        except:  
            return False  
    def close(self):  
        try:  
            self.socket.close()  
            return True  
        except:  
            return False  
  
    def id(self):  
        return '{0}:{1}'.format(self.addr, self.port)  
  
  
def new_client(c):  
    try:  
        while True:  
            data = c.recv()  
            if not data:  
                break  
            else:  
                data = json.loads(data)  
                # print(data)  
                unitree_robot.execute(data[0],   # mode  
                                      data[1],   # gaitType  
                                      data[2],   # speedLevel  
                                      data[3],   # footRaiseHeight  
                                      data[4],   # bodyHeight  
                                      data[5],   # euler  
                                      data[6],   # velocity  
                                      data[7],   # yawSpeed  
                                      data[8])   # reserve  
  
    except socket.error as e:  
        print('({0})Socket error: {1}'.format(c.id(), e))  
    except Exception as e:  
        print('({0})Other exception: {1}'.format(c.id(), e))  
    finally:  
        print('({0})Client leave.'.format(c.id()))  
        c.close()  
        clients.pop(c.id())  
  
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
address = ('192.168.123.161', 8000)  
s.bind(address)  
s.listen(16)  
print('Listening...')  
  
while True:  
    conn, addr = s.accept()  
    c = client(conn, addr, '')  
    clients[c.id()] = c  
    t = threading.Thread(target=new_client, args=(c,))  
    t.start()  
    print('({0})Client entry.'.format(c.id()))
```

#### b.sdk文件

unitree_python_sdk.py:
```python
import sys  
# sys.path.append('/home/unitree/go1_guide/raspberrypi/unitree_legged_sdk/lib/python/arm64')  
sys.path.append(r'../core')  
import robot_interface as sdk  
  
import unitree  
  
class Unitree_Robot_High():  
    def __init__(self):  
        self.udp = sdk.UDP(unitree.HIGHLEVEL, 8080, "192.168.123.161", 8082)  
        self.cmd = sdk.HighCmd()  
        self.state = sdk.HighState()  
        self.udp.InitCmdData(self.cmd)  
  
        self.init_cmd()  
  
    def init_cmd(self):  
        self.cmd.mode = 0      # 0:idle, default stand      1:forced stand     2:walk continuously  
        self.cmd.gaitType = 0  
        self.cmd.speedLevel = 0  
        self.cmd.footRaiseHeight = 0  
        self.cmd.bodyHeight = 0  
        self.cmd.euler = [0, 0, 0]  
        self.cmd.velocity = [0, 0]  
        self.cmd.yawSpeed = 0.0  
        self.cmd.reserve = 0  
    def send_UDP(self):  
        self.udp.SetSend(self.cmd)  
        self.udp.Send()  
      
    def execute(self, mode=2, gaitType=0, speedLevel=0,   
                      footRaiseHeight=0, bodyHeight=0,   
                      euler=[0,0,0], velocity=[0,0], yawSpeed=0.0, reverve=0):  
        self.init_cmd()  
        self.cmd.mode = mode  
        self.cmd.gaitType = gaitType  
        self.cmd.speedLevel = speedLevel  
        self.cmd.footRaiseHeight = footRaiseHeight  
        self.cmd.bodyHeight = bodyHeight  
        self.cmd.euler = euler  
        self.cmd.velocity = velocity  
        self.cmd.yawSpeed = yawSpeed  
        self.cmd.reserve = reverve  
        self.send_UDP()  
  
    # def pose(self, roll, pitch, yaw, bodyHeight):  
    #     self.init_cmd()    #     self.cmd.mode = 1    #     self.cmd.bodyHeight = bodyHeight    #     self.cmd.yaw = yaw    #     self.cmd.pitch = pitch    #     self.cmd.roll = roll    #     self.send_UDP()    def getState(self):  
        self.udp.Recv()  
        self.udp.GetRecv(self.state)  
        return self.state
```

### (3).运动控制程序

#### a. 控制服务端连接对象
robot_connect.py:
```python
import socket  
import json  
  
  
class RobotConnector():  
    def __init__(self, ip_address='192.168.123.161', port=8000):  
        address_server = (ip_address, port)  
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.s.connect(address_server)  
  
    def robot_high_control(self, mode=2, gaitType=2, speedLevel=0,   
                      footRaiseHeight=0, bodyHeight=0,   
                      euler=[0,0,0], velocity=[0,0], yawSpeed=0.0, reverve=0):  
        data = [mode, gaitType, speedLevel, footRaiseHeight, bodyHeight, euler, velocity, yawSpeed, reverve]  
        data = json.dumps(data)  
        self.s.send(bytes(data.encode('utf-8')))
```

#### b. 相机处理模块

Camera.py:
```python
import cv2  
import time  
import os  
import numpy as np  
import requests  
from io import BytesIO  
  
class Camera:  
    def __init__(self, source=0):  
        if isinstance(source, str) and source.startswith('http'):  
            self.is_stream = True  
            self.stream_url = source  
            self.stream = requests.get(self.stream_url, stream=True)  
            self.stream_buffer = BytesIO()  
            self.boundary = b'--'  # Typical MJPEG boundary  
        else:  
            self.is_stream = False  
            self.cap = cv2.VideoCapture(source)  
  
    def getframe(self):  
        if self.is_stream:  
            bytes_image = b''  
            while True:  
                chunk = self.stream.raw.read(1024)  
                if not chunk:  
                    break  
                bytes_image += chunk  
                a = bytes_image.find(b'\xff\xd8')  
                b = bytes_image.find(b'\xff\xd9')  
                if a != -1 and b != -1 and b > a:  
                    jpeg_data = bytes_image[a:b+2]  
                    bytes_image = bytes_image[b+2:]  
                    frame = cv2.imdecode(np.frombuffer(jpeg_data, dtype=np.uint8), cv2.IMREAD_COLOR)  
                    if frame is not None:  
                        return frame  
            return None  
        else:  
            ret, frame = self.cap.read()  
            return frame  
  
    def getframe_rgb(self):  
        frame = self.getframe()  
        if frame is not None:  
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        else:  
            return None  
  
    def showframe(self, frame, window_name='result'):  
        cv2.imshow(window_name, frame)  
  
    def close(self):  
        if self.is_stream:  
            self.stream.close()  
        else:  
            self.cap.release()  
  
    def writeframe(self, frame, filename=''):  
        if filename == '':  
            filename = './result' + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) + '.jpg'  
        cv2.imwrite(filename, frame)
```

#### c.PID控制程序

PID.py:
```python
   
class PID():  
    def __init__(self, dt, max, min, Kp, Kd, Ki):  
       self.dt = dt    # 循环时长  
       self.max = max  # 操作变量最大值  
       self.min = min  # 操作变量最小值  
       self.Kp = Kp         # 比例增益  
       self.Kd = Kd         # 微分增益  
       self.Ki = Ki         # 积分增益  
       self.integral = 0    # 直到上一次的误差值  
       self.pre_error = 0   # 上一次的误差值  
 def calculate(self, setPoint, pv):  
       # 其中 pv:process value 即过程值，  
       error = setPoint - pv           # 误差  
       Pout = self.Kp * error          # 比例项  
       self.integral += error * self.dt  
       Iout = self.Ki * self.integral  # 积分项  
       derivative = (error - self.pre_error)/self.dt  
       Dout = self.Kd * derivative     # 微分项  
 output = Pout + Iout + Dout     # 新的目标值  
 if(output > self.max):  
          output = self.max  
       elif(output < self.min):  
          output = self.min  
   
       self.pre_error = error         # 保存本次误差，以供下次计算  
       return output  
  
  
  
if __name__ == '__main__':  
    import matplotlib.pyplot as plt  
    t = range(150)  
    pid = PID(0.1, 100, -100, 0.1, 0.01, 0.5)  
    val = 20  
    z = []  
    for i in t:  
        inc = pid.calculate(0, val)  
        print("val:{} inc:{}".format(val,inc))  
        z.append(20-val)  
        val += inc  
    plt.figure(figsize=(8,6), dpi = 80)  
    plt.plot(t,z,color="blue",linewidth=1.0,linestyle="-")  
    plt.show()
```

#### d. 主运行程序

main.py:
```python
import asyncio  
import time  
import numpy as np  
import cv2  
import requests  
import threading  
from core.Camera import Camera  # 请确保 Camera 类支持异步 getframe 方法  
from core.robot_connector import RobotConnector  
  
# 定义最小速度和最大速度  
min_speed, max_speed = 0.05, 0.2  # 0.31  #0.345  0.333  #0.42  
# 实例化机器人连接对象  
robot = RobotConnector(ip_address='192.168.123.161', port=8000)  
  
# 定义黄色部分的范围，黄色部分是道路颜色识别  
road_yellow_min = np.array([25, 34, 105], np.uint8)  # 25 ,34, 105  
road_yellow_max = np.array([65, 225, 220], np.uint8)  # 45,225,220  
  
# road_yellow_min = np.array([20, 0, 99])  # 调整后的最小值  
# road_yellow_max = np.array([95, 255, 255])  # 调整后的最大值  
  
# 定义蓝色蓝色范围  
blue_color_min = np.array([117, 100, 100], np.uint8)  
blue_color_max = np.array([130, 250, 250], np.uint8)  
  
# 定义红色范围  
red_color_min = np.array([0, 100, 100], np.uint8)  
red_color_max = np.array([10, 255, 255], np.uint8)  
  
# 定义绿色范围  
green_color_min = np.array([30, 70, 50], np.uint8)  
green_color_max = np.array([90, 255, 120], np.uint8)  
  
# 定义白色范围  
white_color_min = np.array([0, 0, 221], np.uint8)  
white_color_max = np.array([180, 30, 255], np.uint8)  
  
# 定义黑色范围  
black_color_min = np.array([0, 0, 0], np.uint8)  
black_color_max = np.array([180, 255, 56], np.uint8)  
  
# 定义紫色范围  
purple_color_min = np.array([125, 20, 0], np.uint8)  
purple_color_max = np.array([255, 255, 100], np.uint8)  
  
# 这两个video指头部的Nano摄像头的Camera对象实例  
# vedio1 = Camera("http://192.168.123.13:5000/video1")  
vedio2 = Camera("http://192.168.123.13:5000/video2")  
  
# 获取视频流  
stream1 = requests.get('http://192.168.123.13:5000/video2', stream=True)  # 下巴相机  
stream0 = requests.get('http://192.168.123.13:5000/video1', stream=True)  # 头部相机  
  
# 定義傾倒區  
area = [0, 0, 0, 0]  
  
# 定义图像队列  
queue = []  
  
running = True  
stop = False  
euler_stop = False  
  
"""  
写入图像队列  
"""  
  
  
def writeQueue(img):  
    if len(queue) == 10:  
        queue.pop(0)  
    queue.append(img)  
  
  
def readQueue():  
    if len(queue) > 0:  
        if queue[len(queue) - 1] is not None:  
            return queue[len(queue) - 1]  
  
  
"""  
获取相机 n=0 头部 n=1 下巴  
"""  
  
  
def getFrame(n):  
    # 根据 n 获取不同的流对象  
    if n == 1:  
        stream = stream1  
    else:  
        stream = stream0  
  
    bytes_data = b''  # 初始化一个字节串用于保存数据块  
  
    # 读取视频流数据  
    for chunk in stream.iter_content(chunk_size=1024):  
        bytes_data += chunk  
        a = bytes_data.find(b'\xff\xd8')  # 找到JPEG图像的起始标志  
        b = bytes_data.find(b'\xff\xd9')  # 找到JPEG图像的结束标志  
  
        # 如果找到一帧完整的JPEG图像  
        if a != -1 and b != -1:  
            jpg = bytes_data[a:b + 2]  # 提取完整的JPEG图像  
            bytes_data = bytes_data[b + 2:]  # 截断已经处理过的数据  
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)  # 解码图像  
            writeQueue(img)  
  
  
def save(img, result, name):  
    """  
    保存图像并标注检测结果。  
    如果检测结果存在，则在图像上画出检测到的物体的边界框，并保存图像。    参数:  
    img: 输入的图像。  
    result: 检测结果，包含物体的左上角坐标(x, y)、宽度(w)和高度(h)。  
    name: 保存的图像文件名。  
    """    # 检查检测结果是否存在  
    if result:  
        # 解析检测结果，并为物体画出红色边界框  
        x, y, w, h = result  
        color_image = cv2.rectangle(img,  
                                    (x, y),  
                                    (x + w, y + h),  
                                    (0, 0, 255), 2)  
    # 保存处理后的图像  
    cv2.imwrite(name + '.jpg', img)  
    # 输出保存成功的提示信息  
    print('saved')  
  
  
def detect_turn_with_angle(frame):  
    frame = cv2.resize(frame, (640, 480))  
    height, width, _ = frame.shape  
  
    # 转换为HSV颜色空间  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
  
    # 应用颜色阈值以检测黄色  
    mask = cv2.inRange(hsv, road_yellow_min, road_yellow_max)  
    #    mask = cv2.inRange(hsv, (20, 0, 99), (95, 255, 255))  
    # 初始化方向和角度信息  
    directions = []  
    angles = []  
  
    # 定义三个感兴趣的区域（ROI）  
    rois = [  
        (height * 2 // 3, height),  # 下部区域  
        (height // 3, height * 2 // 3),  # 中部区域  
        (0, height // 3)  # 上部区域  
    ]  
  
    output_frame = frame.copy()  
  
    for idx, (startY, endY) in enumerate(rois):  
        roi = mask[startY:endY, :]  
  
        # 查找黄色区域的轮廓3656+  
        contours, _ = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
        # cv2.imshow("a",contours)  
        if contours:  
            # 计算所有黄色区域的中心  
            mask_moments = cv2.moments(roi)  
            if mask_moments["m00"] != 0:  
                cX = int(mask_moments["m10"] / mask_moments["m00"])  
            else:  
                cX = width // 2  
  
            # 可视化每个ROI的中心点  
            cv2.circle(output_frame[startY:endY, :], (cX, (endY - startY) // 2), 5, (0, 255, 0), -1)  
            cv2.putText(output_frame, f'ROI-{idx + 1} Center: ({cX},{(endY - startY) // 2})',  
                        (cX - 50, (endY - startY) // 2 - 10 + startY), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)  
  
            # 计算转弯角度  
            angle = -(np.arctan2(cX - (width // 2), height * 0.5) * 180 / np.pi)  
            angles.append(angle)  
  
            # 判断方向  
            if angle < -15:  
                directions.append("Left")  
            elif angle > 15:  
                directions.append("Right")  
            else:  
                directions.append("Straight")  
  
        else:  
            directions.append("No yellow")  
            angles.append(0)  
  
    # 决定最终方向和角度  
    final_direction = "Straight"  
    final_angle = 0.0  
  
    if "Left" in directions:  
        final_direction = "Left"  
        final_angle = min(angles)  # 取最左侧角度  
    elif "Right" in directions:  
        final_direction = "Right"  
        final_angle = max(angles)  # 取最右侧角度  
  
    return True, final_direction, final_angle, output_frame  
  
  
def get_color_block(img, color_lower, color_upper, square=None):  
    """  
    寻找图像中指定颜色范围的区域。  
    使用HSV颜色空间定义颜色范围，通过形态学操作精炼掩膜，然后找到最大的颜色区域。  
    参数:  
    img: 输入的BGR图像。  
    color_lower: 颜色范围的下限，以HSV格式表示。  
    color_upper: 颜色范围的上限，以HSV格式表示。  
    square: 最小区域面积，用于过滤较小的色块，默认为None（不进行过滤）。  
    返回:  
    如果找到符合条件的色块，则返回该色块的左上角坐标、宽度和高度；  
    如果没有找到色块或找到的色块面积小于指定的最小面积，则返回None。  
    """    # 将BGR颜色空间转为HSV颜色空间  
    hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  
    # 创建颜色掩膜  
    color_mask = cv2.inRange(hsvFrame, color_lower, color_upper)  
    # 创建一个5x5的核，用于进行形态学操作  
    kernal = np.ones((5, 5), "uint8")  
  
    # 使用5x5的核进行膨胀操作  
    color_mask = cv2.dilate(color_mask, kernal)  
    # 找到颜色掩膜的轮廓  
    contours, _ = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
  
    if len(contours) == 0:  
        return None  
    else:  
        # 找到面积最大的轮廓  
        area = max(contours, key=cv2.contourArea)  
        # 获取最大的轮廓的边界框 (x, y, w, h)        x, y, w, h = cv2.boundingRect(area)  
        # x:颜色区域起始的x坐标，Y为y坐标，w为区域宽度，y为区域高度  
        # 检查是否满足最小面积要求  
        if square and w * h < square:  
            return None  
        else:  
            # # 在原图上绘制边界框  
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  
            # # 显示原图  
            # cv2.imshow('Detected Color Block', img)  
            # cv2.waitKey(1)  # 1 ms delay to allow for display update            return [x, y, w, h]  
  
  
def detect_balck(img):  
    res = get_color_block(img, black_color_min, black_color_max)  
    return res  
  
  
def detect_white(img):  
    res = get_color_block(img, white_color_min, white_color_max)  
    return res  
  
  
def detect_purple(img):  
    res = get_color_block(img, purple_color_min, purple_color_max)  
    return res  
  
  
def detect_green(img):  
    res = get_color_block(img, green_color_min, green_color_max)  
    return res  
  
  
def pour(n):  
    print("倾倒")  
    for i in range(30):  
        robot.robot_high_control(mode=1, gaitType=0, euler=[-0.2, 0, 0])  
        time.sleep(0.1)  
    area[n] = 1  
    time.sleep(1)  
  
def euler_thread():  
    """子线程发送欧拉角信号"""  
    global euler_stop  
    print("倾倒")  
    while not euler_stop:  
        robot.robot_high_control(mode=2, gaitType=1, yawSpeed=1)  
        time.sleep(0.2)  
        for i in range(50):  
            for j in range(5):  
                robot.robot_high_control(mode=2,gaitType=1,velocity=[0.1, 0])  
                time.sleep(0.05)  
            robot.robot_high_control(mode=2, gaitType=1, yawSpeed=1.5)  
            time.sleep(0.05)  
        time.sleep(1)  
        robot.robot_high_control(mode=1, gaitType=1, bodyHeight=-0.1,euler=[-1, 0, 0])  
        time.sleep(1)  
        euler_stop=True  
    # 左转  
    # while euler_stop == True:  
    #     robot.robot_high_control(mode=2, gaitType=1, yawSpeed=2, velocity=[0, 0])    #     for i in range(30):    #         robot.robot_high_control(velocity=[0.1, 0])    #         time.sleep(0.02)    #         robot.robot_high_control(mode=2, gaitType=1, yawSpeed=1, velocity=[0, 0])    #         time.sleep(0.02)    #     time.sleep(1)    #     robot.robot_high_control(mode=1,euler=[-1, 0, 0])    #     time.sleep(1)    #     euler_stop=True  
  
def through(n):  
    global running,stop,euler_stop  
    key = 0  
    max_speed2 = max_speed  
    velocity = [0, 0]  # 方向  
    while True:  
        while 1:  
            frame = readQueue()  
            if frame is not None:  
                # cv2.imshow("Frame", frame)  
                # cv2.waitKey(1)                break  
        h_frame, w_frame = frame.shape[0:2]  
        x_center = w_frame / 2  
  
        # 绿色判断  
        if 1 in n and area[0] == 0:  
            res = detect_green(frame)  
            if res is not None and res[2] > 80 and res[3] > 80:  
                running = False  
                stop = True  
                area[0] = 1  
                # 进入倾倒区  
                robot.robot_high_control(velocity=[0, 0.6])  
                # 启动子线程发送欧拉角信号  
                t_euler = threading.Thread(target=euler_thread, name="欧拉角发送线程")  
                t_euler.start()  
                # 等待子线程完成  
                t_euler.join()  
                time.sleep(3)  
                running = True  
                stop = False  
                # time.sleep(0.1)  
                # task = threading.Timer(3,pour,args={0})  
                # robot.robot_high_control(velocity=[0.2,0])                # for i in range(30):                #     robot.robot_high_control(velocity=[0.2,0])                #     time.sleep(0.1)                #     robot.robot_high_control(velocity=[0.2,0])                #     time.sleep(0.1)                # time.sleep(2)                # robot.robot_high_control(mode=1,euler=[-1,0,0])                # # 倾倒  
                # # robot.robot_high_control(mode=1,gaitType=2,euler=[-1,0,0])  
                # # # time.sleep(0.1)                # robot.robot_high_control(mode=2,gaitType=2,velocity=[0.1,0])                # 记录  
                # time.sleep(2)  
                continue  
    # 二号红色判断  
        # if 2 in area and n[0] == 0:  
        #     res = detect_green(frame)        #     if res is not None and res[2] > 100 and res[3]>100:        #         # 进入倾倒区  
        #         robot.robot_high_control(yawSpeed=2.5)  
        #         time.sleep(1)        #         # 倾倒  
        #         robot.robot_high_control(mode=1,gaitType=2,euler=[-1,0,0])  
        #         # 记录  
        #         n[0]=1  
        #         continue    # 计算转弯角度  
        if running == True and stop == False:  
            detected, direction, angle, result_frame = detect_turn_with_angle(frame)  
            # if abs(angle) > 10 and abs(angle) < 50:  
            if abs(angle) > 15:  
                # print("angle:",angle)  
                robot.robot_high_control(mode=2, gaitType=1, yawSpeed=angle / 10, velocity=[0, 0])  
                print("angle:", angle)  
                time.sleep(0.02)  
                # continue  
            robot.robot_high_control(mode=2, gaitType=1, velocity=[0.1, 0])  
            time.sleep(0.05)  
    # cv2.imshow("Original Frame", frame)  
    # cv2.imshow("Result Frame", result_frame)    # cv2.waitKey(1)  
  
if __name__ == '__main__':  
    for i in range(20):  
        #         robot.robot_high_control(velocity=[0.6, 0.00], yawSpeed=0)/  
        robot.robot_high_control(mode=2, gaitType=2, velocity=[0, 0.2])  
        time.sleep(0.1)  
    print("开始循迹")  
    # 创建读取线程  
    t1 = threading.Thread(target=getFrame, name="读取视频流", args={1})  
    t2 = threading.Thread(target=through, name="运动", args={(1, 2)})  
    # 倾倒区：1号为绿色，转角环岛、2号为红色，转角环岛，3号为黑色，十字环岛，4号为紫色，十字环岛。  
    t1.start()  
    t2.start()  
    # asyncio.run(through())  
    # through()
```


# 结果感想

在参加这次比赛的过程中，我深刻体会到了技术创新和团队协作的重要性。我们的项目旨在解决实际中的自动导航问题，通过视觉识别和智能控制，实现了对多种道路状况的精确识别和动作响应。

在开发过程中，我们面临了诸多技术挑战，包括图像处理算法的优化、实时数据传输的稳定性和机器人运动控制的精准性。通过团队成员的密切合作和不懈努力，我们成功地克服了这些难题，最终实现了一个稳定、高效的自动导航系统。

项目的创新点在于我们采用了先进的颜色识别和角度计算技术，使机器人能够准确地根据道路颜色和转角角度进行自主导航。这种创新不仅提升了自动导航系统的性能，还为未来智能交通领域的发展提供了新的思路和解决方案。

比赛过程中，我们不仅获得了宝贵的比赛经验，还与其他优秀团队进行了深入的交流和学习。这不仅增强了我们团队的凝聚力，也拓展了我们在技术和创新方面的视野。

最后，虽然比赛结果可能并非完美，但我们获得的经验和成就感是无法用言语表达的。未来，我们将继续优化项目，探索更多先进技术的应用，为实现智能导航和自动化技术在社会生活中的广泛应用做出更大贡献。