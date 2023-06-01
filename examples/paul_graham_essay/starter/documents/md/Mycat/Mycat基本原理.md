# Mycat 基本原理

## 一、是什么

一个分解数据库压力的数据库中间件

## 二、干什么

> 主要通过分库分表、读写分离等操作分解数据库压力

### 1、读写分离

![image-20220211135711624](C:\Users\liudong\AppData\Roaming\Typora\typora-user-images\image-20220211135711624.png)

### 2、数据分片

> 垂直拆分（分库）、水平拆分（分表）、垂直+水平拆分（分库分表）

![image-20220211135811687](C:\Users\liudong\AppData\Roaming\Typora\typora-user-images\image-20220211135811687.png)

### 3、多数据源

![image-20220211135852326](C:\Users\liudong\AppData\Roaming\Typora\typora-user-images\image-20220211135852326.png)

## 三、基本原理

Mycat 的原理中最重要的一个动词是“拦截”，它拦截了用户发送过来的 SQL 语句，首先对 SQL 语句做了一些特定的分析：如分片分析、路由分析、读写分离分析、缓存分析等，然后将此 SQL 发往后端的真实数据库，并将返回的结果做适当的处理，最终再返回给用户。

![image-20220211140043588](C:\Users\liudong\AppData\Roaming\Typora\typora-user-images\image-20220211140043588.png)

这种方式把数据库的分布式从代码中解耦，是我们无需关心具体的分库分表逻辑。

