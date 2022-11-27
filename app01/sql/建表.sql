
# 注意表在新建的“wuliu”库里面

CREATE TABLE 驿站信息表
(
驿站_编号 char(3)  PRIMARY KEY,
驿站_地址 char(500) NOT NULL,
驿站_电话 char(11) NOT NULL
);


CREATE TABLE 跑腿人员信息表
(
跑腿_工号 char(9)  PRIMARY KEY,
跑腿_姓名 char(40) NOT NULL,
跑腿_身份证号 char(18) NOT NULL,
跑腿_电话 char(11) NOT NULL,
跑腿_驿站编号 char(3),
FOREIGN KEY(跑腿_驿站编号) REFERENCES 驿站信息表(驿站_编号)
);


CREATE TABLE 用户信息表
(
用户_账号 char(9) PRIMARY KEY,
用户_密码 char(9) NOT NULL,
用户_购买账号 char(20),
用户_姓名 char(40) NOT NULL,
用户_电话 char(11) NOT NULL
);

CREATE TABLE 订单表
(
订单_编号 char(10) PRIMARY KEY,
订单_购买账号 char(9)  NOT NULL,
订单_物品名称 char(100) NOT NULL,
订单_物品数量 SMALLINT CHECK (订单_物品数量 > 0),
订单_是否退货 char(1) CHECK (订单_是否退货 IN ('Y', 'N')),
订单_是否签收 char(1) CHECK (订单_是否签收 IN ('Y', 'N')),
订单_驿站编号 char(3) NOT NULL,
订单_收件电话 char(11) NOT NULL,
FOREIGN KEY(订单_驿站编号) REFERENCES 驿站信息表(驿站_编号)
);


CREATE TABLE 配送表
(
配送_订单编号 char(10) PRIMARY KEY,
配送_工号 char(9) NOT NULL,
配送_状态 char(1) CHECK (配送_状态 IN ('N', 'Y', 'P')),
FOREIGN KEY(配送_工号) REFERENCES 跑腿人员信息表(跑腿_工号),
FOREIGN KEY(配送_订单编号) REFERENCES 订单表(订单_编号)
);

#级联删除表
DROP TABLE 驿站信息表 CASCADE;
DROP TABLE 跑腿人员信息表 CASCADE;
DROP TABLE 用户信息表 CASCADE;
DROP TABLE 订单表 CASCADE;
DROP TABLE 配送表 CASCADE;

ALTER TABLE userinfo RENAME TO 用户信息表; #修改表名
ALTER TABLE 用户信息表 RENAME COLUMN use_id TO 用户_账号; #修该列名