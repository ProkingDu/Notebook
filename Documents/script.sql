create table admin
(
    id          int          not null
        primary key,
    username    varchar(255) null comment '用户名',
    password    varchar(255) null comment '密码',
    phone       int          null comment '手机号',
    create_time datetime     null comment '创建日期',
    openid      varchar(32)  null comment '微信openid'
)
    comment '管理员表';

create table class
(
    id          int auto_increment comment 'id'
        primary key,
    name        varchar(255)                null comment '类别名称',
    description varchar(500)                null comment '描述',
    price       decimal(10, 2)              null comment '维修价格',
    picture     varchar(255)                null comment '图片URL，可选',
    create_time datetime                    null comment '创建时间',
    status      enum ('0', '1') default '1' null comment '0:暂停,1:可选'
)
    comment '分类表';

create table engineer
(
    id          int auto_increment
        primary key,
    name        varchar(255) null comment '工程师名',
    username    varchar(255) null comment '用户名',
    phone       varchar(11)  null comment '手机号',
    password    varchar(255) null comment '密码',
    openid      varchar(32)  null comment '微信openid',
    info        json         null comment '个人信息
',
    free_time   datetime     null comment '空闲时间',
    create_time datetime     null comment '添加时间',
    status      int          null
)
    comment '工程师表';

create table `order`
(
    id          int auto_increment
        primary key,
    uid         int                             null comment '用户ID
',
    eid         int                             null comment '工程师id为空则未接单',
    cid         int                             null comment '维修类别id
',
    price       float                           null comment '订单金额',
    remarks     varchar(500)                    null comment '订单备注',
    address     varchar(1000)                   null comment '预约地址',
    status      enum ('0', '1', '-1', '2', '3') null comment '0:待接单,1:已接单:2维修中,3:已完成,-1::已取消',
    create_time datetime                        null comment '创建时间',
    plan_time   datetime                        null comment '预约时间'
)
    comment '订单表';

create index cid
    on `order` (cid);

create index eid
    on `order` (eid);

create index uid
    on `order` (uid);

create table user
(
    id          int(10) auto_increment comment '用户编号'
        primary key,
    username    varchar(255)                null comment '用户名',
    password    varchar(255)                null comment '密码（MD5）',
    openid      varchar(32)                 null comment '微信openid',
    phone       int                         null comment '手机号',
    nickname    varchar(255)                null comment '昵称',
    balance     float                       null comment '余额',
    coin        int                         null comment '积分',
    address     varchar(255)                null comment '地区',
    create_time datetime                    null comment '注册时间',
    status      enum ('0', '1') default '1' null comment '用户状态：0-禁用，1-正常'
)
    comment '用户表';


